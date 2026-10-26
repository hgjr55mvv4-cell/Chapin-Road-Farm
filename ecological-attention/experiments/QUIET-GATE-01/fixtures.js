/* QUIET-GATE-01 offline synthetic fixtures.
 *
 * Every scenario is invented. None describes a real place, a real
 * sighting, a real species identification, or a real safety situation.
 * Every title and text is labelled fictional so that no demo output
 * can be mistaken for an ecological observation or a safety warning.
 * No scenario is ever presented without its fictional label.
 */

(function (root, factory) {
  if (typeof module !== "undefined" && module.exports) {
    module.exports = factory();
  } else {
    root.QuietGateFixtures = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var SCENARIOS = [
    {
      id: "fictional-dusk-insects",
      title: "Fictional scenario: insects at dusk (invented)",
      text: "In this invented scene, tiny insects move together in the evening light. Nothing here was observed, identified, or recorded. It is a prompt for reflection only.",
    },
    {
      id: "fictional-hedgerow-wind",
      title: "Fictional scenario: wind in an imagined hedgerow (invented)",
      text: "In this invented scene, wind moves through an imagined hedgerow and the light changes. Nothing here was observed or measured. It is a prompt for reflection only.",
    },
    {
      id: "fictional-quiet-field",
      title: "Fictional scenario: a quiet imagined field (invented)",
      text: "In this invented scene, a field is quiet for a long stretch and nothing in particular happens. Nothing here was observed or measured. It is a prompt for reflection only.",
    },
    {
      id: "fictional-returning-birds",
      title: "Fictional scenario: birds returning in an imagined evening (invented)",
      text: "In this invented scene, birds return to an imagined roost as the light fades. Nothing here was observed, counted, or identified. It is a prompt for reflection only.",
    },
  ];

  return { SCENARIOS: SCENARIOS };
});
