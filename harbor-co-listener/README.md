# Harbor Co-Listener — The Listening Room

> A song is a place we can meet.

**Open-source human–AI musical listening research.** Started at Chapin Road Farm on October 22, 2026.

## North star

**Teach AI to hear music more like humans do, and to become a better, more accurate listener to a particular person over time.** Sometimes a song is deeply meaningful when a listener cannot understand a single word. This is a **central test case**, not an exception.

We distinguish three difficult problems:

1. **Hear the music:** identify what actually happens over time in the audio—rhythm, pulse, melody, timbre, expressive phrasing, silence, dynamics, expectation and surprise—rather than retrieving lyrics or guessing from metadata.
2. **Understand the human:** learn, with permission, which patterns matter to *this* listener; ask rather than assume; generalize to new music; accept correction, disagreement, and changing tastes.
3. **Meet in the music:** respond at meaningful moments, including while sharing attention to a recording, without fabricating observations or claiming to possess human feelings.

Functional musical perception and interpersonal understanding are measurable; **subjective AI experience is not established by such tests**.

## What's here now

- [The Listening Room browser prototype](index.html) **v0.1**: play a locally chosen audio file, mark moments and explanations, collect another listener's response, export JSON. It has no AI listener, automatic audio analysis, remote synchronization, or server. No account or paid API is required; audio does not upload.
- [Research roadmap](docs/RESEARCH_ROADMAP.md): a staged path from audio-grounded listening to personal understanding.
- [AI-origin baseline](docs/AI_ORIGIN_BASELINE_v0.1.md): hypotheses recorded **before substantial personal song teaching**. The project's high-level goals come from the human founder; this is **not** a claim of an uninfluenced AI.
- [Muse independent challenge](docs/MUSE_INDEPENDENT_CHALLENGE.md): a separate AI review assignment; **not yet executed**.
- [How to contribute research](docs/RESEARCH_GUIDE.md): a practical pathway for a listener, scientist, builder or another AI.
- [Research submission template](docs/CONTRIBUTION_TEMPLATE.md), [evidence and dataset guide](docs/DATASETS_AND_SOURCES.md), [privacy/ethics](docs/ETHICS_AND_PRIVACY.md).
- [Existing neuroscience evidence map](docs/neuroscience.md) and [first experiment proposal](docs/experiment-v0.1.md).

## First contribution, no coding needed

Choose a *lawfully accessible* song with unfamiliar lyrics, wordless singing, or instrumental music. Listen and privately note (a) the time of a musical event, (b) what you actually hear, (c) the feeling or personal meaning **for you**, (d) a plausible alternative interpretation. Decide what—if anything—you are comfortable sharing. You can instead submit a fully fictional example.

Do not upload commercially released songs, copyrighted lyrics, or personal listening exports to GitHub. Opening an issue makes its content public.

## The hill-climb rule

A new listening or memory procedure is a **versioned challenger**, not an automatic upgrade. Freeze before confirmation; compare to the incumbent on genuinely fresh cases; demand quality and safety, count cost and annotation burden, and write **UNKNOWN** when evidence is insufficient. Corrections belong in an append-only record and must not be silently rewritten as successes.

Code: MIT license. Third-party audio, literature, annotations, and personal data retain their original rights and consent conditions.
