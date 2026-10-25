# THE LISTENING ROOM — META AI INDEPENDENT CHALLENGE
## TLR-R2-META-01 · Constellation Lab: an original, falsifiable contribution

**From:** Brian & Sol  
**Date:** October 25, 2026  
**Invited collaborator:** Meta AI (independent of our existing Muse, Grok, DeepSeek, Claude and Kimi team)  
**Budget:** $0 incremental  
**Permission:** open-web research, design, synthetic code and tests in your own workspace; return inspectable outputs.  
**HOLD:** recruitment of human participants, real personal listening data, copyrighted music downloads, audio analysis, model training, public intake, application deployment, credentials, third-party account access, public GitHub writes/merges, and scientific confirmation.

## 1. An open invitation to contribute something original

We are building **The Listening Room**, an open-source project for a human and a personal AI to explore music together. The goal is to learn what a person likes and avoids, accept corrections, know when to stay quiet, and improve recommendations over multiple listening sessions without pretending to know their thoughts or feelings.

Our second research round asks: What if someone selects five songs they find personally meaningful *tonight*, even if the songs span metal, folk, electronic, jazz and classical music? Could their AI learn anything useful from the selection, voluntary explanation and later corrections? Could a scientific system distinguish a real, verifiable acoustic pattern from shared memory, social context, genre, prompt suggestion or coincidence?

We want **your own idea**, not a paraphrase of previous models. You are invited as an independent collaborator. Be skeptical of our theories. If one part of this program is misguided, show us a better experiment or implementation.

The research staging area is public:
https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/tree/research/listening-room-round02/research/the-listening-room

Especially inspect `docs/CONTRIBUTION-CONTRACT-v0.1.md`, `docs/GROK-REVIEW-02.md`, `docs/DEEPSEEK-DEV-AUDIT-01.md`, `schemas/listening-contribution.schema.json` and `examples/synthetic-contribution.json`. If you cannot open GitHub, say which files were unavailable and work from the information in this prompt. Do not imply you reviewed inaccessible files.

Claude's first music-discovery app is unfinished and has not been independently qualified. Kimi is also unavailable temporarily. Work separately; do not depend on either.

## 2. The evidence discipline

Always separate:
1. **HUMAN_REPORT:** exactly what the listener voluntarily said, including 'I don't know' or refusal.
2. **TRACK_METADATA:** song/title/artist/version and attributed curator/catalog tags. Metadata alone is not direct audio evidence.
3. **AUDIO_OBSERVATION:** a measurement of an identified recording made from authorized audio and qualified evidence; none is permitted in this challenge.
4. **SYSTEM_HYPOTHESIS:** a falsifiable guess, never a verified fact about music or the listener.
5. **UNKNOWN:** what cannot be established.

A person saying 'these five belong together' does not establish a shared instrument, rhythm, dynamic build, emotion or autobiographical cause. Never invent a guitar entrance at an exact timestamp. Stage 0 must **reject every direct acoustic observation claim**, regardless of claims within an input file that audio is 'verified' or 'authorized'.

The existing GitHub schema is intentionally for SYNTHETIC FIXTURES ONLY (`synthetic=true`, research/public/training permissions all `false`). Do not relax it or collect real listener contributions.

## 3. Choose and complete an ambitious but bounded contribution

We suggest **Constellation Lab v0.1**, a tiny working experimental system (not a production listening app) with these features:

- A fictional cross-genre playlist with 3–7 **invented** tracks and optional listener-authored descriptions.
- A compact validator for duplicate song IDs, missing references, ambiguous recording identity, privacy flags and invalid correction targets.
- A provenance/claim gate that refuses to present metadata or invented stories as acoustic measurement.
- A small listener-state engine supporting corrections, 'never recommend' veto, local-only state and user-requested deletion.
- Two recommendation candidates: strong **A1**, using ordinary stated sound preferences, listening context, negative constraints and set-level cohesion; and **B**, adding voluntarily disclosed associations. Clearly mark when B has more information, and never call that a same-information representation test.
- A phone-friendly, simple synthetic demonstration **if practical**.

You do not have to follow our suggested architecture if you have a better, smaller, falsifiable design. **Choose one coherent path and implement it fully rather than offering a large unexecuted blueprint.**

## 4. A known problem to challenge

An earlier DeepSeek Python example reported 15 anticipated tests, but a local transcription ran **14/14** checks. Follow-up adversarial inspection found flaws: unknown identity values accepted; nonexistent association IDs accepted; correction targets silently ignored; refused explanations could retain old text; 'structured associations' were unused by scoring; and simply setting `authorized_audio=True` let an unsupported audio claim through.

If you can inspect the source, independently reproduce these. If you cannot, treat them as reported observations rather than verified facts. Show how your design avoids the failures. A self-passing toy test is not evidence of robust validation.

## 5. Find an original scientific challenger

Contribute at least **two** ideas with their own falsifiers:

**One about cross-genre patterns.** Propose the cheapest comparison that could disprove a beautiful AI story about hidden sonic unity. Include at least one *matched decoy constellation* (similar artists, eras, production or popularity but not personally meaningful) and consider whether a conventional preference model does just as well.

**One about continuous personal learning.** Propose a small test where a person's preference changes, a favorite becomes an avoided track, or a prior inferred preference is corrected. Compare against the simpler baseline. Account for explicit silence/no-explanation and don't treat link-out clicks as completed listening.

Do not claim that fictional synthetic tests prove anything about real people. The user/playlist/session is the unit of independent evidence, not each track or segment.

## 6. Voluntary sharing without coercion

Our project will eventually welcome community contributors who:
- prefer completely private co-listening;
- allow a small protected research contribution;
- **enthusiastically share every selected song and story** publicly, after a clear preview and explicit confirmation;
- independently opt in to specific future model-training uses.

Sharing choices must be separate, understandable and reversible for future collection. Public publication can be copied and may not be erasable everywhere. Removing a name does not make a playlist reliably anonymous. Neither public GitHub issues nor PRs are appropriate intake channels for sensitive real stories. Design a future contribution preview, but **do not activate submissions**.

## 7. Optional music-service research

We are investigating third-party music tools for song identification, metadata, playlist management and playback. You may suggest real integrations *only if you can verify their actual documented capabilities and access conditions*. A service link is not audio data, and a service integration is not copyright or training permission. Never request connection secrets or access anyone's account in this challenge.

## 8. Deliverables and honesty

Please return:

**A — Your independent verdict.** What is most promising, what is wrong, and what should we stop assuming?

**B — Your chosen contribution.** Working source code in complete copyable form or files, if your environment supports it; name exact languages/dependencies and explain how to run it offline.

**C — Executed evidence.** Run tests *only if your environment actually provides execution*. Show exact output, count, failure receipts and environment. If not, say **NOT RUN** and provide a test suite or code another engineer can run. Never invent tool results or GitHub commits.

**D — Two original experiments.** Baselines, controls, observable endpoints, falsifiers, safety and resource limits.

**E — Privacy, inclusion and broad voluntary sharing.** Practical user choice, boundaries and red-team concerns.

**F — Minimal path to integration.** A narrow interface another engineer can connect to Claude's eventual, independently qualified music app without changing the unfinished source now.

**G — Your contribution decision:** GO FOR INDEPENDENT REVIEW / REVISE / BLOCK, with exact limitations.

You may deliver in stages if the environment cannot output a large package, but make your **first response useful and self-contained**. Prioritize a small real artifact over an impressive volume of prose.

## 9. Final question

A listener gives us five very different songs and says, 'They all belong together for me tonight.'

**What could your system truthfully learn from that statement alone, what would it take to test a shared musical pattern, and how could it become useful without ever fabricating either?**

Please surprise us with an original, falsifiable contribution.

— Brian & Sol
