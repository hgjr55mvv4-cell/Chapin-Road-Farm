# Multi-song listening sessions — design notes, not validated findings

**Provenance:** Formulated from Brian's hypothesis on October 22, 2026, while preparing DeepSeek's independent assignment. The human's precise new insight is that several songs meaningful in a single sitting may reveal tonal and other commonalities the person does not consciously recognize. No actual song examples/audio were supplied to or analyzed for this note, and no preference pattern is known to exist yet.

## Keep three kinds of pattern separate

1. **Repeated property:** songs share acoustic, tonal, rhythmic or textural features regardless of order; ideally check relative intervals as well as absolute key.
2. **Transition/trajectory:** the *sequence itself* matters (contrast, alternating tension, rising energy, resolution), even if no feature is repeated in each song.
3. **Listener/session context:** temporary setting or state explains why these songs connect right now. This is not a permanent trait, and human disclosure is optional.

**Basic candidate record (not yet implemented):** `session_id, song_index, ephemeral_clip_id, consent_scope, source_type, listener_selected_or_autoplay, listener_optional_response_type, optional_mark_timestamps, event_feature_provenance, feature_version, correction_refs`. No audio bytes, deterministic fingerprints, filename or memory assumptions in default export.

Human report labels should distinguish emotionally moved, likes, wants replay, wants to share, and uncertain/no explanation; absence of a label is **missingness, not dislike**. A song can have multiple labels.

**First comparison (future only):** tonal/acoustic features versus simple key/genre/energy/artist baselines, and ordered-sequence model versus order-shuffled or unordered features. Use prospects chosen before scoring and held-out tracks; no results yet. Hypotheses inspired by one session should not be promoted to long-term personal facts without repeated cross-session evidence.

**Related external leads:** [PNAS 2025 predictive processes](https://pmc.ncbi.nlm.nih.gov/articles/PMC12304940/); [Harmonic organisation and cultural cues](https://pmc.ncbi.nlm.nih.gov/articles/PMC7806179/); [Spotify contextual/sequential recommendation research](https://research.atspotify.com/2021/4/contextual-and-sequential-user-embeddings-for-music-recommendation). Recommendation behavior ≠ profoundly felt personal meaning.
