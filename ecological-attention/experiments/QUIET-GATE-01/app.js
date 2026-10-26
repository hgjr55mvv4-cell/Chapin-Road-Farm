/* QUIET-GATE-01 demo wiring: connects the page controls to gate.js.
 *
 * This file keeps no records of its own, sends nothing anywhere, and
 * reads no device capability. The only clock is a simulated one that
 * starts at zero and moves only when the user presses the
 * "Advance simulated time" button, so a page reload always restarts
 * in OFF with a fresh gate. There is deliberately no code here that
 * runs on its own: every prompt in the demo is caused by a button
 * the user pressed in this session.
 */

(function () {
  "use strict";

  var simulatedMs = 0;
  var scenarioIndex = 0;

  var gate = QuietGate.createGate({
    now: function () {
      return simulatedMs;
    },
    scenarios: QuietGateFixtures.SCENARIOS,
  });

  function $(id) {
    return document.getElementById(id);
  }

  var statusEl = $("mode-status");
  var outputEl = $("output");
  var pendingEl = $("pending-count");
  var rateEl = $("rate-count");
  var optInEl = $("proactive-optin");
  var suppressBtn = $("suppress-btn");

  function say(text) {
    outputEl.textContent = text;
  }

  function render() {
    var state = gate.getState();
    statusEl.textContent =
      "Current mode: " + state.mode + ". " +
      (state.mode === "OFF"
        ? "Nothing is being monitored, recorded, or prompted."
        : state.mode === "ON_REQUEST"
          ? "Nothing will appear unless you ask for it."
          : "Simulated prompts are opted in, capped, and can be suppressed or stopped at any time.");
    pendingEl.textContent = "Pending simulated prompts: " + state.pendingCount + ".";
    rateEl.textContent =
      "Simulated prompts delivered in the current hour: " +
      state.promptsInWindow + " of " + state.maxPromptsPerWindow + ".";

    var buttons = {
      "mode-off": state.mode === "OFF",
      "mode-request": state.mode === "ON_REQUEST",
      "mode-proactive": state.mode === "PROACTIVE",
    };
    Object.keys(buttons).forEach(function (id) {
      $(id).setAttribute("aria-pressed", buttons[id] ? "true" : "false");
    });

    $("mode-proactive").disabled = !optInEl.checked && state.mode !== "PROACTIVE";
    $("ask-btn").disabled = state.mode === "OFF";
    $("simulate-btn").disabled = state.mode !== "PROACTIVE";
    suppressBtn.disabled = state.mode !== "PROACTIVE";
    suppressBtn.textContent = state.suppressed
      ? "Unsuppress simulated prompts"
      : "Suppress simulated prompts";
    if (state.mode !== "PROACTIVE") {
      optInEl.checked = false;
    }
  }

  function showResult(result) {
    if (result.delivered) {
      say(result.title + " — " + result.text);
    } else if (result.kind === "RESPONSE_TO_REQUEST") {
      say(result.title + " — " + result.text);
    } else {
      var reason = result.reason || "not delivered";
      if (reason === "RATE_LIMIT") {
        say("Rate limit reached: no simulated prompt was shown. Advance simulated time, or switch mode.");
      } else if (reason === "SUPPRESSED") {
        say("Simulated prompts are suppressed: nothing was shown.");
      } else if (reason === "NOTHING_PENDING") {
        say("No simulated prompt is pending.");
      } else {
        say("No simulated prompt was shown (" + reason + ").");
      }
    }
    render();
  }

  $("mode-off").addEventListener("click", function () {
    gate.setMode("OFF");
    optInEl.checked = false;
    say("Off. Nothing is being monitored, recorded, or prompted, and any pending simulated prompts were cleared.");
    render();
  });

  $("mode-request").addEventListener("click", function () {
    gate.setMode("ON_REQUEST");
    say("On request. Nothing will appear unless you press Ask for a reflection.");
    render();
  });

  $("mode-proactive").addEventListener("click", function () {
    if (!optInEl.checked) {
      say("Proactive demo needs a deliberate opt-in: check the opt-in box first.");
      render();
      return;
    }
    gate.setMode("PROACTIVE", { optIn: true });
    say("Proactive demo on, by your opt-in. Simulated prompts are capped and can be suppressed or stopped at any time.");
    render();
  });

  $("ask-btn").addEventListener("click", function () {
    try {
      showResult(gate.requestAssistance());
    } catch (err) {
      say("Could not answer that request: " + err.message);
      render();
    }
  });

  $("simulate-btn").addEventListener("click", function () {
    try {
      var scenario =
        QuietGateFixtures.SCENARIOS[scenarioIndex % QuietGateFixtures.SCENARIOS.length];
      scenarioIndex += 1;
      var queued = gate.queuePrompt(scenario);
      if (!queued.queued) {
        say("Simulated prompt queue is full: nothing was added.");
        render();
        return;
      }
      showResult(gate.deliverNext());
    } catch (err) {
      say("Could not simulate that event: " + err.message);
      render();
    }
  });

  suppressBtn.addEventListener("click", function () {
    try {
      var state = gate.getState();
      if (state.suppressed) {
        gate.unsuppress();
        say("Simulated prompts are unsuppressed.");
      } else {
        gate.suppress();
        say("Simulated prompts are suppressed: nothing will appear until you unsuppress or switch mode.");
      }
      render();
    } catch (err) {
      say("Could not change suppression: " + err.message);
      render();
    }
  });

  $("advance-time-btn").addEventListener("click", function () {
    simulatedMs += 15 * 60 * 1000;
    say("Simulated time advanced by 15 minutes. This affects only the demo rate limit, not real time.");
    render();
  });

  $("clear-btn").addEventListener("click", function () {
    gate.clearSyntheticState();
    say("Demo state cleared. Mode is unchanged; pending prompts and counts were reset.");
    render();
  });

  render();
})();
