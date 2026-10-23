# Auditory Intelligence — sound, language and situated interaction

**Status: OPEN RESEARCH + SYNTHETIC ENGINEERING DEV. No deployed listening system.**

Research shared across Harbor Co-Listener and Virtual Farm Manager: can an AI distinguish what was **actually recorded**, what a transcript says, what an acoustic event suggests, what context remains unknown and what action is warranted?

Start with [AUDITORY-DEV-01 synthetic waveform preflight](dev-01/README.md), [Muse Round 01 attributed research digest](MUSE_ROUND01_RELAY_DIGEST.md), [Sol review](SOL_REVIEW_01.md) and [next bounded Muse review prompt](SOL_TO_MUSE_ROUND02.md).

## Evidence ladder

**Level 0:** sensor validity (missing, clipping, interference, sample format).  
**Level 1:** waveform-grounded intervals, activity and acoustic measurements.  
**Level 2:** uncertain classifications of acoustic events (not physical source identity).  
**Level 3:** words/turns/corrections, conditional on actually available speech data.  
**Level 4:** contextual hypotheses about referents or the conversational situation.  
**Level 5:** cautious wait, ask, abstain or verify actions; never automatic physical action on speculative inference.

The current code covers Level 0 and **only a narrow Level 1 timing metric on non-speech tones**. A supplied transcript is an external symbolic label, not speech decoded from WAV.

No microphone, bystander surveillance, speaker identification, emotion diagnosis, field operation, copyrighted audio, human labels or paid API inference. Every source/test case is public **EXPOSED DEV**, not scientific confirmation. 