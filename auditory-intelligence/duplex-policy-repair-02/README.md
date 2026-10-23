# DUPLEX-POLICY-REPAIR-02 — event-ledger only

**Status:** versioned deterministic mock, no microphones, actual audio or AI inference. Distinct from earlier immutable [15-session incumbent](../duplex-situation-dev-01/CONTRACT.md). The prior Astra user-relayed review reproduced mock defects; source ZIP for Astra's new checks was not available to this run. [Acceptance contract](CONTRACT.md) · [Design-only separate acoustic next experiment](PLAYBACK_REFERENCE_01_DESIGN.md).

The change is **not a speech model**. Each input already supplies mock origin, confidence, addressee, independently authorized session role, playback-match state, text and timing. The repair processes a **transaction ledger** rather than returning the same earliest request forever. An actual playback echo incorrectly tagged as task user and incorrectly tagged as *non-echo* can still produce an erroneous **proposal**. No proposal commits without a separate UI confirmation of the exact content. That confirmation control is mocked and not itself a real user-authentication system.

From this directory:

```sh
python -m unittest discover -s tests -v
python demo.py > receipts/demo.json
```

[28 deterministic regression tests](tests/test_policy_repair.py) include deliberate negative cases: invalid NaN/Inf confidence, stale/malformed revisions, quote handling from **supplied metadata**, echo-match suppressions, uncertain-source approvals via explicit UI, independent later corrections after prior ASK, cancellation and exact-prefix causality. The demo displays toy actions, unresolved states and logical task values. Neither test counts nor an action name establishes correct physical-source recognition, task authorization, natural speech semantics or permission to act on a farm.

**Known design risks:** The toy grammar accepts only a few exact corrections; transcript quote and speaker/addressee/echo fields are not sourced from audio; a forged UI-authorized boolean in a mock is not authentication; confirmed task values have no physical actuation; event IDs/revisions must come from an independently trusted integration; correction threads require independently established conversational context; replay of past action traces is descriptive and not a replay of real audible interventions. Complex policy performance and human interaction costs remain untested.

Published in the same public research repository. Source/test CI on Python 3.11 and 3.13 is a **separate verification** step from the local developer test run.
