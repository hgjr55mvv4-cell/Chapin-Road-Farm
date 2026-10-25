# Listening Contribution Contract v0.1 — DESIGN ONLY

A listening contribution describes what **one person** chose to share about **one listening occasion**. It is not proof of a song's objective meaning or an AI's auditory competence.

## Proposed flow
1. Listener chooses a song from a legally accessible service; identify artist/title/version. Unresolved recording identity stays UNKNOWN.
2. Listener may select the moment or whole-song scope, using an optional approximate timestamp.
3. Listener chooses *their own words* to describe why the song or moment matters **now**. No forced mood, trauma or biographical prompts.
4. Listener may assemble a *moment playlist*: a group of songs chosen as connected to them in this situation, regardless of genre.
5. Listener may say what—if anything—connects the playlist, or select 'I can't put it into words' or 'No explanation'.
6. Personal feedback stays session-only unless the listener explicitly enables storage. Separate decisions govern sharing with researchers and publishing any contribution.
7. The AI may suggest tentative connections and record rejections, but no guessed meaning is silently treated as a human report.

## Required separations
- **Human report:** listener's own characterization. No confidence score for its emotional legitimacy.
- **Track identity/metadata:** supplied title, artist, edition/version, stable provider links, source and verification state.
- **Audio observation:** musical attributes anchored to an authorized recording, with observation method, timing uncertainty and validation.
- **System hypothesis:** an explicitly provisional proposal of pattern or relevance, linked to the evidence and correctable.
- **Playlist selection:** a group selected by a person for a particular occasion, not an independent sample per song.

## Privacy tiers — proposals, not an operational consent UI
- LOCAL_SESSION: temporary, no remote transmission.
- LOCAL_SAVED: user-authorized device persistence and removal.
- RESEARCH_PRIVATE: separate, specific opt-in to a reviewed protected research intake, NOT public GitHub.
- PUBLIC_RELEASE: independent, item-level opt-in **after** redaction and clear notice about irreversibility once public.
- MODEL_TRAINING: separate explicit authorization if this use is ever proposed; default **off**.

No tier is automatically implied by an earlier tier. Public repositories are not a safe place for genuine sensitive diaries or unreviewed volunteer submissions. A playlist plus timestamps and context can be identifying even without a name.

## Research cautions
- Distinguish the person, session, playlist and independent recording as separate observational units.
- Same track across many playlists is not a new independent source recording.
- Many excerpts from one song are not independent audio examples.
- Asking 'why does this move you?' can change the reported experience; study prompt effects.
- 'Liked' ≠ 'meaningful', 'replayed' ≠ 'enjoyed', and 'skipped' ≠ 'disliked'.
- Multi-genre similarity can be due to common production conventions, familiarity, artist, tempo, listener description, or selection artifacts. Include controls and counterexamples.
- Audio analysis requires rights to access/process recordings; track metadata and service links alone are not audio.
- Culturally restricted practices should not be solicited or published without appropriate community governance.

## Round 02 gate

Muse should propose the minimum humane input instrument and demonstrate five diverse, synthetic walkthroughs. Grok should try to break it. Do not build an open collection endpoint or populate this branch with actual participant records yet.