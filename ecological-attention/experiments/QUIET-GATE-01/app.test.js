/* QUIET-GATE-01.1 UI-wiring tests.
 *
 * Run: node --test app.test.js
 * The page script is executed in a stub DOM (no browser, no device).
 * These tests prove the wiring between the checkbox / Clear button
 * and the state machine; they do NOT prove real-browser, VoiceOver,
 * or touch behaviour, which remain NOT RUN (see README.md).
 */

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const IDS = [
  "mode-status",
  "output",
  "pending-count",
  "rate-count",
  "proactive-optin",
  "suppress-btn",
  "mode-off",
  "mode-request",
  "mode-proactive",
  "ask-btn",
  "simulate-btn",
  "advance-time-btn",
  "clear-btn",
];

function makeElement(id) {
  const el = {
    id,
    textContent: "",
    disabled: false,
    checked: false,
    attributes: {},
    listeners: {},
    setAttribute(k, v) {
      this.attributes[k] = v;
    },
    getAttribute(k) {
      return this.attributes[k];
    },
    addEventListener(type, fn) {
      (this.listeners[type] = this.listeners[type] || []).push(fn);
    },
    click() {
      for (const fn of this.listeners.click || []) fn();
    },
    change() {
      for (const fn of this.listeners.change || []) fn();
    },
  };
  return el;
}

function loadPage() {
  const elements = {};
  for (const id of IDS) elements[id] = makeElement(id);
  const document = {
    getElementById: (id) => elements[id],
  };
  const sandbox = { document, console };
  sandbox.self = sandbox;
  vm.createContext(sandbox);
  for (const file of ["gate.js", "fixtures.js", "app.js"]) {
    vm.runInContext(fs.readFileSync(path.join(__dirname, file), "utf8"), sandbox, {
      filename: file,
    });
  }
  return elements;
}

function enterProactive(el) {
  el["proactive-optin"].checked = true;
  el["proactive-optin"].change();
  el["mode-proactive"].click();
  assert.match(el["mode-status"].textContent, /PROACTIVE/);
}

test("UI: fresh page is OFF with prompting controls disabled", () => {
  const el = loadPage();
  assert.match(el["mode-status"].textContent, /OFF/);
  assert.equal(el["simulate-btn"].disabled, true);
  assert.equal(el["ask-btn"].disabled, true);
  assert.equal(el["mode-proactive"].disabled, true);
});

test("UI defect B: unchecking opt-in while PROACTIVE switches to OFF immediately", () => {
  const el = loadPage();
  enterProactive(el);
  el["simulate-btn"].click();
  assert.match(el["pending-count"].textContent, /0/); // delivered, none pending
  el["simulate-btn"].click();
  el["simulate-btn"].click();
  el["proactive-optin"].checked = false;
  el["proactive-optin"].change();
  assert.match(el["mode-status"].textContent, /OFF/);
  assert.match(el["pending-count"].textContent, /0/);
  assert.equal(el["simulate-btn"].disabled, true);
  // A further Simulate press cannot produce a fictional prompt.
  el["simulate-btn"].click();
  assert.doesNotMatch(el["output"].textContent, /Fictional scenario/);
});

test("UI defect B: queued prompts do not survive consent withdrawal and re-entry", () => {
  const el = loadPage();
  enterProactive(el);
  // Queue three prompts but deliver only via the Simulate button's
  // queue+deliver path; instead force a pending state through the
  // rate cap: deliver 3, then queue a 4th that is rate-blocked.
  el["simulate-btn"].click();
  el["simulate-btn"].click();
  el["simulate-btn"].click();
  el["simulate-btn"].click(); // rate-limited, still queued
  assert.match(el["output"].textContent, /Rate limit/);
  el["proactive-optin"].checked = false;
  el["proactive-optin"].change();
  assert.match(el["mode-status"].textContent, /OFF/);
  assert.match(el["pending-count"].textContent, /0/);
  // Fresh opt-in and re-entry: no stale prompt appears on its own,
  // and the rate window was reset by the revocation.
  enterProactive(el);
  assert.match(el["pending-count"].textContent, /0/);
  el["simulate-btn"].click();
  assert.match(el["output"].textContent, /Fictional scenario/);
});

test("UI defect A: Clear button returns to OFF and revokes consent", () => {
  const el = loadPage();
  enterProactive(el);
  el["simulate-btn"].click();
  el["clear-btn"].click();
  assert.match(el["mode-status"].textContent, /OFF/);
  assert.equal(el["proactive-optin"].checked, false);
  assert.match(el["pending-count"].textContent, /0/);
  assert.equal(el["simulate-btn"].disabled, true);
  // Re-entering without re-checking is refused by the handler.
  el["mode-proactive"].click();
  assert.match(el["mode-status"].textContent, /OFF/);
});

test("UI: leaving PROACTIVE for ON_REQUEST requires a fresh opt-in to return", () => {
  const el = loadPage();
  enterProactive(el);
  el["mode-request"].click();
  assert.match(el["mode-status"].textContent, /ON_REQUEST/);
  assert.equal(el["proactive-optin"].checked, false);
  el["mode-proactive"].click();
  assert.match(el["mode-status"].textContent, /ON_REQUEST/);
  enterProactive(el);
  assert.match(el["mode-status"].textContent, /PROACTIVE/);
});

test("UI: checking the box alone does not enter PROACTIVE, and rate/suppression still work", () => {
  const el = loadPage();
  el["proactive-optin"].checked = true;
  el["proactive-optin"].change();
  assert.match(el["mode-status"].textContent, /OFF/);
  assert.equal(el["mode-proactive"].disabled, false);
  el["mode-proactive"].click();
  el["simulate-btn"].click();
  el["simulate-btn"].click();
  el["simulate-btn"].click();
  el["simulate-btn"].click();
  assert.match(el["output"].textContent, /Rate limit/);
  el["suppress-btn"].click();
  assert.match(el["suppress-btn"].textContent, /Unsuppress/);
});
