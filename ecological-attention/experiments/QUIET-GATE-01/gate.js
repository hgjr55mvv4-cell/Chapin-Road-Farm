/* QUIET-GATE-01 interaction state machine.
 *
 * Small, deterministic, dependency-free. No network, no persistent
 * storage, no device sensing, no background timers, no tracking.
 * All state lives in memory in a single object created by createGate()
 * and is lost when the page is reloaded or the object is discarded.
 * That loss is a feature: a fresh start is always OFF.
 *
 * Modes:
 *   OFF         - nothing is sensed, processed, recorded, or prompted.
 *                 The OFF choice is not logged per person. There is no
 *                 per-person log anywhere in this file.
 *   ON_REQUEST  - the user may explicitly ask for a fictional
 *                 reflection. Nothing is ever offered unprompted.
 *   PROACTIVE   - simulated prompts only, and only after a deliberate
 *                 opt-in (setMode("PROACTIVE", { optIn: true })).
 *
 * Safety properties enforced here, not just in the user interface:
 *   - A fresh gate is OFF.
 *   - Switching to OFF clears pending prompts, prompt timestamps,
 *     suppression, and the proactive opt-in.
 *   - ON_REQUEST can never queue or deliver a spontaneous prompt.
 *   - PROACTIVE prompts are rate-limited (default 3 per 60 simulated
 *     minutes) and blocked while suppressed.
 *   - Invalid transitions throw an Error with a `code` property and
 *     leave the state unchanged.
 *
 * The clock is injectable so tests are deterministic: pass
 * { now: () => ms } and advance it in tests. In the demo, the
 * "advance simulated time" control moves this clock; it never reads
 * a device clock for prompting decisions beyond the injected value.
 */

(function (root, factory) {
  if (typeof module !== "undefined" && module.exports) {
    module.exports = factory();
  } else {
    root.QuietGate = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var MODES = ["OFF", "ON_REQUEST", "PROACTIVE"];

  function GateError(code, message) {
    var err = new Error(message);
    err.code = code;
    return err;
  }

  function createGate(options) {
    options = options || {};
    var nowFn = typeof options.now === "function" ? options.now : Date.now;
    var maxPrompts = options.maxPromptsPerWindow || 3;
    var windowMs = options.windowMs || 60 * 60 * 1000;
    var maxPending = options.maxPending || 5;
    var scenarios = options.scenarios || [];

    var mode = "OFF";
    var proactiveOptIn = false;
    var suppressed = false;
    var pending = []; // queued fictional prompts, in order
    var promptTimes = []; // timestamps of delivered prompts, rate-limit only
    var requestIndex = 0; // round-robin over fictional reflections
    var deliveredCount = 0;
    var droppedCount = 0;

    function snapshot() {
      return {
        mode: mode,
        proactiveOptIn: proactiveOptIn,
        suppressed: suppressed,
        pendingCount: pending.length,
        promptsInWindow: promptTimes.filter(function (t) {
          return nowFn() - t < windowMs;
        }).length,
        maxPromptsPerWindow: maxPrompts,
        deliveredCount: deliveredCount,
        droppedCount: droppedCount,
      };
    }

    function clearSyntheticState() {
      pending = [];
      promptTimes = [];
      suppressed = false;
      proactiveOptIn = false;
      deliveredCount = 0;
      droppedCount = 0;
    }

    function setMode(next, opts) {
      opts = opts || {};
      if (MODES.indexOf(next) === -1) {
        throw GateError("INVALID_MODE", "Unknown mode: " + String(next));
      }
      if (next === "PROACTIVE" && opts.optIn !== true) {
        throw GateError(
          "PROACTIVE_OPT_IN_REQUIRED",
          "PROACTIVE requires a deliberate opt-in: setMode('PROACTIVE', { optIn: true })"
        );
      }
      if (next === "OFF") {
        // OFF overrides everything: pending prompts are discarded,
        // not deferred, and all synthetic state is cleared.
        mode = "OFF";
        clearSyntheticState();
        return snapshot();
      }
      mode = next;
      proactiveOptIn = next === "PROACTIVE";
      if (next !== "PROACTIVE") {
        suppressed = false;
      }
      return snapshot();
    }

    function requestAssistance() {
      if (mode === "OFF") {
        throw GateError(
          "INVALID_TRANSITION",
          "Cannot request assistance while OFF. Choose ON_REQUEST first."
        );
      }
      if (scenarios.length === 0) {
        throw GateError("NO_SCENARIOS", "No fictional scenarios configured.");
      }
      var item = scenarios[requestIndex % scenarios.length];
      requestIndex += 1;
      // A response to an explicit request is not a prompt: it is not
      // counted against the proactive rate limit.
      return {
        kind: "RESPONSE_TO_REQUEST",
        fictional: true,
        title: item.title,
        text: item.text,
      };
    }

    function queuePrompt(scenario) {
      if (mode !== "PROACTIVE") {
        throw GateError(
          "INVALID_TRANSITION",
          "Spontaneous prompts exist only in PROACTIVE mode, never in " + mode + "."
        );
      }
      if (!scenario || typeof scenario.title !== "string") {
        throw GateError("INVALID_SCENARIO", "A prompt needs a scenario with a title.");
      }
      if (pending.length >= maxPending) {
        droppedCount += 1;
        return { queued: false, reason: "QUEUE_FULL" };
      }
      pending.push(scenario);
      return { queued: true, pendingCount: pending.length };
    }

    function deliverNext() {
      if (mode !== "PROACTIVE") {
        return { delivered: false, reason: "NOT_PROACTIVE" };
      }
      if (suppressed) {
        return { delivered: false, reason: "SUPPRESSED" };
      }
      if (pending.length === 0) {
        return { delivered: false, reason: "NOTHING_PENDING" };
      }
      var now = nowFn();
      promptTimes = promptTimes.filter(function (t) {
        return now - t < windowMs;
      });
      if (promptTimes.length >= maxPrompts) {
        droppedCount += 1;
        return { delivered: false, reason: "RATE_LIMIT" };
      }
      var item = pending.shift();
      promptTimes.push(now);
      deliveredCount += 1;
      return {
        delivered: true,
        kind: "SIMULATED_PROMPT",
        fictional: true,
        title: item.title,
        text: item.text,
      };
    }

    function suppress() {
      if (mode !== "PROACTIVE") {
        throw GateError(
          "INVALID_TRANSITION",
          "Suppression applies in PROACTIVE mode only."
        );
      }
      suppressed = true;
      return snapshot();
    }

    function unsuppress() {
      suppressed = false;
      return snapshot();
    }

    return {
      MODES: MODES,
      getState: snapshot,
      setMode: setMode,
      requestAssistance: requestAssistance,
      queuePrompt: queuePrompt,
      deliverNext: deliverNext,
      suppress: suppress,
      unsuppress: unsuppress,
      clearSyntheticState: function () {
        clearSyntheticState();
        return snapshot();
      },
    };
  }

  return { createGate: createGate };
});
