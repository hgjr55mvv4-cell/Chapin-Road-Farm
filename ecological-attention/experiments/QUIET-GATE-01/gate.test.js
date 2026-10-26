/* QUIET-GATE-01 adversarial tests.
 *
 * Run: node --test gate.test.js
 * These are unit tests for the state machine only. They do NOT prove
 * real-device accessibility, VoiceOver behaviour, iPad touch behaviour,
 * or that any human's attention is improved. Those checks are labelled
 * NOT RUN in README.md.
 */

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const { createGate } = require("./gate.js");
const { SCENARIOS } = require("./fixtures.js");

function fakeClock() {
  let ms = 0;
  return {
    now: () => ms,
    advance: (delta) => {
      ms += delta;
    },
  };
}

function gateWithClock() {
  const clock = fakeClock();
  const gate = createGate({ now: clock.now, scenarios: SCENARIOS });
  return { gate, clock };
}

test("fresh start is OFF, with nothing pending and nothing delivered", () => {
  const { gate } = gateWithClock();
  const state = gate.getState();
  assert.equal(state.mode, "OFF");
  assert.equal(state.pendingCount, 0);
  assert.equal(state.deliveredCount, 0);
  assert.equal(state.proactiveOptIn, false);
  assert.equal(state.suppressed, false);
});

test("a newly created gate is OFF: reload-equivalent, since no state persists", () => {
  const { gate } = gateWithClock();
  gate.setMode("PROACTIVE", { optIn: true });
  gate.queuePrompt(SCENARIOS[0]);
  // A reload discards the old object entirely; the replacement is OFF.
  const fresh = createGate({ scenarios: SCENARIOS });
  assert.equal(fresh.getState().mode, "OFF");
  assert.equal(fresh.getState().pendingCount, 0);
  assert.deepEqual(fresh.deliverNext(), {
    delivered: false,
    reason: "NOT_PROACTIVE",
  });
});

test("PROACTIVE without a deliberate opt-in fails and leaves mode unchanged", () => {
  const { gate } = gateWithClock();
  assert.throws(() => gate.setMode("PROACTIVE"), (err) => {
    assert.equal(err.code, "PROACTIVE_OPT_IN_REQUIRED");
    return true;
  });
  assert.equal(gate.getState().mode, "OFF");
  gate.setMode("PROACTIVE", { optIn: true });
  assert.equal(gate.getState().mode, "PROACTIVE");
});

test("switching to OFF from every state clears pending prompts", () => {
  for (const from of ["ON_REQUEST", "PROACTIVE"]) {
    const { gate } = gateWithClock();
    gate.setMode(from, { optIn: true });
    if (from === "PROACTIVE") {
      gate.queuePrompt(SCENARIOS[0]);
      gate.queuePrompt(SCENARIOS[1]);
      assert.equal(gate.getState().pendingCount, 2);
    }
    gate.setMode("OFF");
    const state = gate.getState();
    assert.equal(state.mode, "OFF");
    assert.equal(state.pendingCount, 0);
    assert.equal(state.deliveredCount, 0);
    assert.equal(state.proactiveOptIn, false);
    assert.deepEqual(gate.deliverNext(), {
      delivered: false,
      reason: "NOT_PROACTIVE",
    });
  }
});

test("ON_REQUEST never generates an unsolicited prompt", () => {
  const { gate } = gateWithClock();
  gate.setMode("ON_REQUEST");
  assert.throws(() => gate.queuePrompt(SCENARIOS[0]), (err) => {
    assert.equal(err.code, "INVALID_TRANSITION");
    return true;
  });
  assert.deepEqual(gate.deliverNext(), {
    delivered: false,
    reason: "NOT_PROACTIVE",
  });
  // An explicit request is answered, and is not counted as a prompt.
  const answer = gate.requestAssistance();
  assert.equal(answer.kind, "RESPONSE_TO_REQUEST");
  assert.equal(answer.fictional, true);
  assert.equal(gate.getState().promptsInWindow, 0);
});

test("rate limit is enforced exactly at its boundary and recovers after the window", () => {
  const { gate, clock } = gateWithClock();
  gate.setMode("PROACTIVE", { optIn: true });
  for (let i = 0; i < 4; i++) gate.queuePrompt(SCENARIOS[i % SCENARIOS.length]);
  assert.equal(gate.deliverNext().delivered, true);
  assert.equal(gate.deliverNext().delivered, true);
  assert.equal(gate.deliverNext().delivered, true);
  const blocked = gate.deliverNext();
  assert.equal(blocked.delivered, false);
  assert.equal(blocked.reason, "RATE_LIMIT");
  // One minute past the hour window: the earliest prompts expire.
  clock.advance(61 * 60 * 1000);
  assert.equal(gate.deliverNext().delivered, true);
});

test("invalid state transitions fail safely and leave state unchanged", () => {
  const { gate } = gateWithClock();
  assert.throws(() => gate.setMode("WHISPER"), (err) => {
    assert.equal(err.code, "INVALID_MODE");
    return true;
  });
  assert.throws(() => gate.requestAssistance(), (err) => {
    assert.equal(err.code, "INVALID_TRANSITION");
    return true;
  });
  assert.throws(() => gate.suppress(), (err) => {
    assert.equal(err.code, "INVALID_TRANSITION");
    return true;
  });
  assert.throws(() => gate.queuePrompt(SCENARIOS[0]), (err) => {
    assert.equal(err.code, "INVALID_TRANSITION");
    return true;
  });
  assert.equal(gate.getState().mode, "OFF");
  gate.setMode("ON_REQUEST");
  assert.throws(() => gate.suppress(), (err) => {
    assert.equal(err.code, "INVALID_TRANSITION");
    return true;
  });
  assert.equal(gate.getState().mode, "ON_REQUEST");
});

test("in-memory synthetic state is cleared on OFF and by explicit clear", () => {
  const { gate } = gateWithClock();
  gate.setMode("PROACTIVE", { optIn: true });
  gate.queuePrompt(SCENARIOS[0]);
  gate.deliverNext();
  assert.equal(gate.getState().deliveredCount, 1);
  gate.setMode("OFF");
  assert.deepEqual(gate.getState(), {
    mode: "OFF",
    proactiveOptIn: false,
    suppressed: false,
    pendingCount: 0,
    promptsInWindow: 0,
    maxPromptsPerWindow: 3,
    deliveredCount: 0,
    droppedCount: 0,
  });
  gate.setMode("PROACTIVE", { optIn: true });
  gate.queuePrompt(SCENARIOS[0]);
  gate.deliverNext();
  gate.clearSyntheticState();
  assert.equal(gate.getState().mode, "PROACTIVE");
  assert.equal(gate.getState().pendingCount, 0);
  assert.equal(gate.getState().deliveredCount, 0);
});

test("suppression blocks delivery and unsuppression restores it", () => {
  const { gate } = gateWithClock();
  gate.setMode("PROACTIVE", { optIn: true });
  gate.queuePrompt(SCENARIOS[0]);
  gate.suppress();
  assert.deepEqual(gate.deliverNext(), {
    delivered: false,
    reason: "SUPPRESSED",
  });
  assert.equal(gate.getState().pendingCount, 1);
  gate.unsuppress();
  assert.equal(gate.deliverNext().delivered, true);
});

test("pending prompts deliver in first-in, first-out order", () => {
  const { gate } = gateWithClock();
  gate.setMode("PROACTIVE", { optIn: true });
  gate.queuePrompt(SCENARIOS[0]);
  gate.queuePrompt(SCENARIOS[1]);
  assert.equal(gate.deliverNext().title, SCENARIOS[0].title);
  assert.equal(gate.deliverNext().title, SCENARIOS[1].title);
});

test("a full prompt queue drops further prompts instead of overflowing", () => {
  const { gate } = gateWithClock();
  gate.setMode("PROACTIVE", { optIn: true });
  for (let i = 0; i < 5; i++) gate.queuePrompt(SCENARIOS[0]);
  const sixth = gate.queuePrompt(SCENARIOS[0]);
  assert.equal(sixth.queued, false);
  assert.equal(sixth.reason, "QUEUE_FULL");
  assert.equal(gate.getState().droppedCount, 1);
});

test("explicit requests are deterministic and cycle through fictional scenarios", () => {
  const { gate } = gateWithClock();
  gate.setMode("ON_REQUEST");
  const titles = [];
  for (let i = 0; i < SCENARIOS.length + 1; i++) {
    titles.push(gate.requestAssistance().title);
  }
  assert.equal(titles[0], SCENARIOS[0].title);
  assert.equal(titles[SCENARIOS.length], SCENARIOS[0].title);
});

test("every fixture is labelled fictional", () => {
  assert.ok(SCENARIOS.length >= 3);
  for (const item of SCENARIOS) {
    const combined = (item.title + " " + item.text).toLowerCase();
    assert.ok(combined.includes("fictional"), item.id);
    assert.ok(combined.includes("invented"), item.id);
  }
});

test("production source contains no persistent-storage, network, or device-sensing calls", () => {
  // Source-level assertion only. It proves the shipped code does not
  // call these capabilities; it does not prove a browser behaves.
  const forbidden = [
    "localStorage",
    "sessionStorage",
    "IndexedDB",
    "XMLHttpRequest",
    "geolocation",
    "getUserMedia",
    "analytics",
  ];
  const productionFiles = [
    "gate.js",
    "fixtures.js",
    "app.js",
    "index.html",
    "style.css",
  ];
  for (const file of productionFiles) {
    const source = fs.readFileSync(path.join(__dirname, file), "utf8");
    for (const token of forbidden) {
      assert.ok(!source.includes(token), `${file} must not contain ${token}`);
    }
  }
  // The page loads no external resource: no http(s) reference at all.
  const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
  assert.ok(!html.includes("http://") && !html.includes("https://"));
});
