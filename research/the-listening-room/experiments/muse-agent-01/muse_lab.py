"""
Muse Constellation Lab v0.2 -- INDEPENDENT implementation
TLR-R2-MUSE-AGENT-01, experiments/muse-agent-01/

Attribution, stated plainly:
  * This code was written by Muse (the newly available separate
    Muse app), from the public spec in NEW-MUSE-AGENT-01.md and
    the contribution contract. It is NOT Meta AI's
    Constellation Lab v0.1, it is NOT a copy of it, and it is
    NOT an audit of verified GitHub source for that lab.
  * Meta AI's constellation_lab.py / test_constellation_lab.py
    were NOT found on GitHub at the checked location (see
    README provenance table). The local copy in the
    conversation was used ONLY for adversarial probes, and
    those probe results are reported separately from this
    implementation. No Meta AI code was pasted into this file.
  * All tracks, sessions, and listeners here are invented and
    synthetic. No real listener data, no audio, no training,
    no deployment, no public intake. Budget $0. Python 3.11+
    standard library only, offline.

What this lab fixes, relative to the reported Meta AI v0.1
(probe results, not claims about verified source):
  P0a. Playlist members that are dicts/lists crashed Meta AI's
      validator with TypeError (unhashable). Here every ID is
      checked to be a string BEFORE any set operation, and a
      malformed input returns an error list, never a crash.
  P0b. A generator passed to add_session() was consumed and
      stored as an empty session. Here iterables are
      materialised exactly once, validated, and only then
      stored; a generator is accepted and its items are kept.
  P0c. Corrections could reference arbitrary session IDs.
      Here a session-scoped correction must reference a known
      session, or be explicitly session-less (session_id=None).
  P0d. Session-local suppression was described but not
      implemented in the rankers. Here recommend() takes an
      optional session_id and excludes that session's
      session-local rejected tracks -- while the global
      ranking does not, so the two are testably different.
  P0e. The audio-claim gate recognised only the exact type
      "audio_observation" and a few field names. An
      "acoustic_observation" claim slipped through. Here any
      claim type or field name indicating an audio/acoustic/
      spectral/embedding measurement is rejected at Stage 0,
      regardless of any authorized_audio flag. Free-text
      listener words are NOT scanned for these words -- only
      claim types and field names -- so a listener saying
      "tempo" in their own words is not censored.
  P0f. Partial mutation: state methods validate EVERYTHING
      before mutating anything. A failed add_session or
      add_correction leaves the state byte-for-byte unchanged
      (tested by snapshot comparison).

What this lab adds (original, falsifiable):
  Idea 1 -- No-constellation null world (see experiments.py
  logic in run_experiments): if sessions are random, a
  provenance ranker must NOT beat popularity and must NOT
  invent constellations. Abstention on zero-provenance
  candidates is part of this: recommend() returns only
  candidates with provenance > 0; everything else is listed
  separately as "no provenance -- not recommended", never as
  a ranked recommendation by popularity or ID tie-break.
  Idea 2 -- Context-split edge ledger: edges are typed
  (kept_together / replaced / not_tonight / never) and carry
  a session context label. A context-conditioned ranker
  uses only sessions from the queried context; a
  context-blind ranker uses all sessions. Both receive the
  same context label (blind ignores it), so the comparison
  is about use, not access. On context-dependent listeners
  the conditioned ranker must win; on stable listeners it
  must NOT win -- otherwise it is overfitting to labels.
  P3 -- Constrained A1 (explicit preferences): a separately
  scored ranker that uses ONLY explicitly stated user
  tokens, negative constraints, and curator tags (metadata,
  explicitly NOT audio evidence). It CAN propose unseen
  songs, which provenance cannot. It is never mixed with
  provenance scores, and its comparison is marked as
  more-information / different-capability, never as a
  same-information test.

Unit of evidence: the SESSION for next-pick, the CORRECTION
EVENT for replacements, the LISTENER for aggregation.
Holdout splits are chronological, by session. Results are
reported across multiple seeds with mean, range, and
approximate 95% CI (mean +/- 1.96 * SE), not a single seed.
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field

# ------------------------------------------------------------------
# Fail-closed validation
# ------------------------------------------------------------------

# Claim types / field names that indicate a measurement claim.
# Only these structural markers are checked, never free text.
_MEASUREMENT_TYPES = {
    "audio_observation", "acoustic_observation",
    "audio_measurement", "acoustic_measurement",
    "spectral_observation", "spectral_measurement",
    "embedding_observation", "verified_audio",
    "audio_analysis", "acoustic_analysis",
}
_MEASUREMENT_FIELD_SUBSTRINGS = (
    "audio_feature", "acoustic_", "spectral_", "embedding",
    "mfcc", "chroma", "tempo_", "bpm",
)


def _is_measurement_claim(obj):
    """True if obj (a dict) is a measurement claim by type/field."""
    if not isinstance(obj, dict):
        return False
    claim_type = obj.get("type")
    if isinstance(claim_type, str) and claim_type in _MEASUREMENT_TYPES:
        return True
    for key in obj:
        if isinstance(key, str) and any(s in key for s in _MEASUREMENT_FIELD_SUBSTRINGS):
            return True
    return False


def _scan_measurements(obj, path="$"):
    errors = []
    if isinstance(obj, dict):
        if _is_measurement_claim(obj):
            errors.append(
                f"{path}: measurement claim rejected at Stage 0 "
                "(audio/acoustic/spectral/embedding claims are never "
                "permitted here, regardless of authorized_audio)"
            )
        for key, value in obj.items():
            errors.extend(_scan_measurements(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            errors.extend(_scan_measurements(value, f"{path}[{i}]"))
    return errors


def _string_ids(value, field_name, errors):
    """Return a list of string IDs, or [] with errors recorded.

    Never calls set() on unvalidated input. Dict/list members
    produce an error, not a TypeError.
    """
    if not isinstance(value, list):
        errors.append(f"{field_name} must be a list")
        return []
    out = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{field_name}[{i}] must be a non-empty string")
        else:
            out.append(item)
    return out


def validate_contribution(data):
    """Validate a listening contribution. Returns error list.

    Never raises for malformed data, never silently drops an
    item, never partially validates a nested structure.
    """
    errors = []
    if not isinstance(data, dict):
        return ["contribution must be an object"]
    if data.get("schema_version") != "0.1-dev":
        errors.append("schema_version must be '0.1-dev'")
    if data.get("synthetic") is not True:
        errors.append("synthetic must be true (synthetic fixtures only)")
    privacy = data.get("privacy")
    if not isinstance(privacy, dict):
        errors.append("privacy must be an object")
    else:
        if privacy.get("storage") not in ("session_only", "local_saved"):
            errors.append("privacy.storage must be session_only or local_saved")
        for key in ("research_use", "public_release", "model_training"):
            if privacy.get(key) is not False:
                errors.append(f"privacy.{key} must be false")
    session = data.get("session")
    if not isinstance(session, dict):
        errors.append("session must be an object")
    else:
        if not isinstance(session.get("session_id"), str) or not session["session_id"]:
            errors.append("session.session_id must be a non-empty string")
        if session.get("occasion_label") is not None and not isinstance(
            session.get("occasion_label"), str
        ):
            errors.append("session.occasion_label must be a string or null")
    songs = data.get("songs")
    song_ids = []
    seen_ids = set()
    if not isinstance(songs, list) or not (1 <= len(songs) <= 30):
        errors.append("songs must be a list of 1 to 30 songs")
        songs = songs if isinstance(songs, list) else []
    # Ambiguous recording identity: same title+artist, unverified.
    title_artist_seen = {}
    for i, song in enumerate(songs):
        prefix = f"songs[{i}]"
        if not isinstance(song, dict):
            errors.append(f"{prefix} must be an object")
            continue
        sid = song.get("song_id")
        if not isinstance(sid, str) or not sid:
            errors.append(f"{prefix}.song_id must be a non-empty string")
        elif sid in seen_ids:
            errors.append(f"duplicate song_id: {sid}")
        else:
            seen_ids.add(sid)
            song_ids.append(sid)
        track = song.get("track")
        if not isinstance(track, dict):
            errors.append(f"{prefix}.track must be an object")
        else:
            for fname in ("title", "artist"):
                if not isinstance(track.get(fname), str) or not track[fname]:
                    errors.append(f"{prefix}.track.{fname} must be a non-empty string")
            if track.get("identity_status") not in ("unverified", "verified"):
                errors.append(f"{prefix}.track.identity_status must be unverified or verified")
            if track.get("source_url") is not None and not isinstance(track.get("source_url"), str):
                errors.append(f"{prefix}.track.source_url must be a string or null")
            key = (track.get("title"), track.get("artist"))
            if track.get("identity_status") == "unverified":
                if key in title_artist_seen:
                    errors.append(
                        f"ambiguous recording identity: {key!r} appears for "
                        f"{title_artist_seen[key]} and {sid} with unverified identity"
                    )
                else:
                    title_artist_seen[key] = sid
        report = song.get("listener_report")
        if not isinstance(report, dict):
            errors.append(f"{prefix}.listener_report must be an object")
        else:
            if report.get("text") is not None and not isinstance(report.get("text"), str):
                errors.append(f"{prefix}.listener_report.text must be a string or null")
            if report.get("scope") not in ("whole_song", "specific_moment", "unspecified"):
                errors.append(f"{prefix}.listener_report.scope is invalid")
        moments = song.get("moments")
        if not isinstance(moments, list):
            errors.append(f"{prefix}.moments must be a list")
        else:
            for j, moment in enumerate(moments):
                if not isinstance(moment, dict):
                    errors.append(f"{prefix}.moments[{j}] must be an object")
                    continue
                if moment.get("type") != "human_report":
                    errors.append(f"{prefix}.moments[{j}].type must be human_report")
                sec = moment.get("approx_seconds")
                if sec is not None and (isinstance(sec, bool) or not isinstance(sec, (int, float)) or sec < 0):
                    errors.append(f"{prefix}.moments[{j}].approx_seconds must be >= 0 or null")
                note = moment.get("listener_note")
                if note is not None and not isinstance(note, str):
                    errors.append(f"{prefix}.moments[{j}].listener_note must be a string or null")
    playlist = data.get("playlist")
    if not isinstance(playlist, dict):
        errors.append("playlist must be an object")
    else:
        ids = _string_ids(playlist.get("song_ids"), "playlist.song_ids", errors)
        if ids:
            if len(ids) != len(set(ids)):
                errors.append("playlist.song_ids must be unique")
            for sid in ids:
                if sid not in seen_ids:
                    errors.append(f"playlist references unknown song_id: {sid}")
        if playlist.get("connection_in_own_words") is not None and not isinstance(
            playlist.get("connection_in_own_words"), str
        ):
            errors.append("playlist.connection_in_own_words must be a string or null")
    for i, corr in enumerate(data.get("corrections", []) or []):
        if not isinstance(corr, dict):
            errors.append(f"corrections[{i}] must be an object")
            continue
        for fname in ("rejected_id", "replacement_id"):
            if corr.get(fname) not in seen_ids:
                errors.append(f"corrections[{i}].{fname} references unknown song_id: {corr.get(fname)!r}")
        if corr.get("rejected_id") == corr.get("replacement_id"):
            errors.append(f"corrections[{i}] rejected and replacement must differ")
    for i, assoc in enumerate(data.get("associations", []) or []):
        if not isinstance(assoc, dict):
            errors.append(f"associations[{i}] must be an object")
            continue
        ids = _string_ids(assoc.get("song_ids", []), f"associations[{i}].song_ids", errors)
        for sid in ids:
            if sid not in seen_ids:
                errors.append(f"associations[{i}] references unknown song_id: {sid}")
    errors.extend(_scan_measurements(data))
    return errors


# ------------------------------------------------------------------
# Listener state with typed edge ledger
# ------------------------------------------------------------------

@dataclass
class Edge:
    kind: str  # kept_together | replaced | not_tonight | never
    a: str
    b: str | None
    session_id: str | None
    context: str | None


@dataclass
class ListenerState:
    catalog: set = field(default_factory=set)
    # sessions: list of (session_id, frozenset, context or None), in order
    sessions: list = field(default_factory=list)
    corrections: list = field(default_factory=list)  # (rejected, replacement, session_id)
    vetoes: set = field(default_factory=set)
    reports: dict = field(default_factory=dict)
    session_suppressions: dict = field(default_factory=dict)  # session_id -> set(rejected)
    edges: list = field(default_factory=list)
    silence_events: int = 0
    click_out_events: int = 0

    def _require_known(self, song_id):
        if not isinstance(song_id, str) or song_id not in self.catalog:
            raise ValueError(f"unknown song_id: {song_id!r}")

    def _snapshot(self):
        return (list(self.sessions), list(self.corrections), set(self.vetoes),
                dict(self.reports), {k: set(v) for k, v in self.session_suppressions.items()},
                list(self.edges))

    def add_session(self, session_id, kept_ids, context=None):
        # Materialise exactly once, validate everything, then mutate.
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        if any(sid == session_id for sid, _, _ in self.sessions):
            raise ValueError(f"duplicate session_id: {session_id!r}")
        kept = list(kept_ids)  # consumes a generator exactly once, keeps items
        if not kept:
            raise ValueError("session must contain at least one track")
        for sid in kept:
            self._require_known(sid)
        if len(set(kept)) != len(kept):
            raise ValueError(f"session {session_id!r} contains duplicate song IDs")
        kept_set = frozenset(kept)
        self.sessions.append((session_id, kept_set, context))
        for a in kept_set:
            for b in kept_set:
                if a < b:
                    self.edges.append(Edge("kept_together", a, b, session_id, context))

    def add_correction(self, rejected_id, replacement_id, session_id=None, scope="session"):
        # Validate before mutating. Session-scoped corrections must
        # reference a known session; session_id=None means "no
        # session context claimed", not "any session".
        self._require_known(rejected_id)
        self._require_known(replacement_id)
        if rejected_id == replacement_id:
            raise ValueError("correction rejected and replacement must differ")
        if scope not in ("session", "global_note"):
            raise ValueError("correction scope must be 'session' or 'global_note'")
        if scope == "session":
            if session_id is not None and not any(sid == session_id for sid, _, _ in self.sessions):
                raise ValueError(f"correction references unknown session_id: {session_id!r}")
        self.corrections.append((rejected_id, replacement_id, session_id))
        self.edges.append(Edge("replaced", rejected_id, replacement_id, session_id, None))
        if scope == "session" and session_id is not None:
            self.session_suppressions.setdefault(session_id, set()).add(rejected_id)
            self.edges.append(Edge("not_tonight", rejected_id, None, session_id, None))

    def veto(self, song_id):
        self._require_known(song_id)
        self.vetoes.add(song_id)
        self.edges.append(Edge("never", song_id, None, None, None))

    def unveto(self, song_id):
        self.vetoes.discard(song_id)

    def update_report(self, song_id, text):
        self._require_known(song_id)
        # None clears; a string replaces. Refusal is not a trait.
        self.reports[song_id] = text

    def record_silence(self):
        self.silence_events += 1

    def record_click_out(self, song_id):
        self._require_known(song_id)
        self.click_out_events += 1  # NOT a keep, NOT listening

    def delete_all(self):
        self.sessions.clear()
        self.corrections.clear()
        self.vetoes.clear()
        self.reports.clear()
        self.session_suppressions.clear()
        self.edges.clear()
        self.silence_events = 0
        self.click_out_events = 0

    def derived_counts(self):
        """Counts derived ONLY from current sessions/corrections.

        After delete_all() these must be zero -- there is no
        separate cache or append-only log retaining personal text.
        """
        pop = {}
        for _, kept, _ in self.sessions:
            for sid in kept:
                pop[sid] = pop.get(sid, 0) + 1
        return {"session_track_counts": pop, "n_corrections": len(self.corrections),
                "n_edges": len(self.edges)}


# ------------------------------------------------------------------
# Rankers -- ID-only, validated inputs
# ------------------------------------------------------------------

def _validate_rank_inputs(state, seed, all_ids):
    for sid in seed:
        state._require_known(sid)
    for sid in all_ids:
        state._require_known(sid)


def _popularity(state, sessions=None):
    counts = {}
    for _, kept, _ in (sessions if sessions is not None else state.sessions):
        for sid in kept:
            counts[sid] = counts.get(sid, 0) + 1
    return counts


def _base_candidates(state, seed, all_ids, session_id=None):
    seed_set = set(seed)
    suppressed = state.session_suppressions.get(session_id, set()) if session_id else set()
    return [c for c in all_ids if c not in seed_set and c not in state.vetoes and c not in suppressed]


def popularity_ranker(state, seed, all_ids):
    _validate_rank_inputs(state, seed, all_ids)
    counts = _popularity(state)
    return sorted(_base_candidates(state, seed, all_ids), key=lambda c: (-counts.get(c, 0), c))


def provenance_ranker(state, seed, all_ids, context=None):
    """Seed-conditioned co-occurrence, optionally context-restricted.

    If context is given, only sessions with that context are used.
    The caller must pass the context label to BOTH rankers in a
    comparison; the blind ranker simply passes context=None.
    """
    _validate_rank_inputs(state, seed, all_ids)
    seed_set = set(seed)
    sessions = state.sessions
    if context is not None:
        sessions = [s for s in sessions if s[2] == context]
    co = {}
    for _, kept, _ in sessions:
        if seed_set & kept:
            for sid in kept:
                if sid not in seed_set:
                    co[sid] = co.get(sid, 0) + 1
    pair = {}
    for rej, rep, _ in state.corrections:
        if rej in seed_set:
            pair[rep] = pair.get(rep, 0) + 1
    counts = _popularity(state, sessions)
    return sorted(_base_candidates(state, seed, all_ids),
                  key=lambda c: (-co.get(c, 0), -pair.get(c, 0), -counts.get(c, 0), c))


def recommend(state, seed, all_ids, session_id=None, context=None):
    """User-facing recommendation with abstention.

    Returns (recommended, not_recommended, abstain).
    recommended = candidates with provenance score > 0
    (co-occurrence in the relevant sessions, or a correction
    pair from a seed track), in provenance order, excluding
    vetoes, seed, and session-local suppressions.
    not_recommended = all other candidates, with reason
    "no provenance". If recommended is empty, abstain=True
    and NO popularity/ID-order list is presented as a
    recommendation. That is a feature, not a missing feature:
    a forced ranking with zero evidence would be fabrication.
    """
    _validate_rank_inputs(state, seed, all_ids)
    ranked = provenance_ranker(state, seed, all_ids, context=context)
    # Recompute scores to split at >0, respecting session suppression
    seed_set = set(seed)
    sessions = state.sessions
    if context is not None:
        sessions = [s for s in sessions if s[2] == context]
    co = {}
    for _, kept, _ in sessions:
        if seed_set & kept:
            for sid in kept:
                if sid not in seed_set:
                    co[sid] = co.get(sid, 0) + 1
    pair = {}
    for rej, rep, _ in state.corrections:
        if rej in seed_set:
            pair[rep] = pair.get(rep, 0) + 1
    candidates = _base_candidates(state, seed, all_ids, session_id=session_id)
    # provenance_ranker does not apply session suppression, so
    # filter ranked to candidates here for the user-facing list.
    recommended = [c for c in ranked if c in candidates and (co.get(c, 0) > 0 or pair.get(c, 0) > 0)]
    not_recommended = [c for c in candidates if c not in recommended]
    return recommended, not_recommended, len(recommended) == 0


def replacement_ranker(state, rejected_id, all_ids):
    state._require_known(rejected_id)
    for sid in all_ids:
        state._require_known(sid)
    pair = {}
    for rej, rep, _ in state.corrections:
        if rej == rejected_id:
            pair[rep] = pair.get(rep, 0) + 1
    counts = _popularity(state)
    cands = [c for c in all_ids if c != rejected_id and c not in state.vetoes]
    return sorted(cands, key=lambda c: (-pair.get(c, 0), -counts.get(c, 0), c))


def global_replacement_ranker(state, rejected_id, all_ids):
    state._require_known(rejected_id)
    for sid in all_ids:
        state._require_known(sid)
    glob = {}
    for _, rep, _ in state.corrections:
        glob[rep] = glob.get(rep, 0) + 1
    counts = _popularity(state)
    cands = [c for c in all_ids if c != rejected_id and c not in state.vetoes]
    return sorted(cands, key=lambda c: (-glob.get(c, 0), -counts.get(c, 0), c))


def a1_explicit_ranker(explicit_tokens, negative_tokens, catalogue_tags, all_ids, vetoes):
    """P3 constrained A1 -- separately scored, different capability.

    Inputs are ONLY what the listener explicitly stated:
    explicit_tokens (their words, e.g. "spacious"), negative
    constraints, and curator tags attached to catalogue tracks.
    Tags are metadata, NOT audio measurements, and are never
    presented as audio evidence. This ranker CAN propose
    unseen songs (no co-occurrence required) -- that is its
    capability, not a same-information win over provenance.
    Score = tag overlap with explicit tokens, minus overlap
    with negative tokens. Tie-break by ID, deterministic.
    """
    explicit = set(explicit_tokens or [])
    negative = set(negative_tokens or [])
    scored = []
    for cid in all_ids:
        if cid in vetoes:
            continue
        tags = set(catalogue_tags.get(cid, []))
        score = len(tags & explicit) - len(tags & negative)
        scored.append((cid, score))
    return [cid for cid, _ in sorted(scored, key=lambda x: (-x[1], x[0]))]


# ------------------------------------------------------------------
# Synthetic worlds
# ------------------------------------------------------------------

def make_catalog(n=30):
    catalog = {}
    genres = ["metal", "folk", "electronic", "jazz", "classical"]
    for i in range(1, n + 1):
        sid = f"T{i:02d}"
        catalog[sid] = {
            "title": f"Invented Track {i:02d}",
            "artist": f"Invented Artist {(i % 7) + 1}",
            "genre": genres[(i - 1) % len(genres)],
            # Curator tags for A1 only. These are invented
            # metadata strings, not audio measurements.
            "tags": [genres[(i - 1) % len(genres)], "tag-a" if i % 3 == 0 else "tag-b"],
        }
    return catalog


@dataclass
class SyntheticListener:
    listener_id: str
    constellations: list
    noise_pool: list
    replacement_pairs: list
    # context_world: dict context -> constellation index, or None
    context_map: dict | None = None


def make_listener(rng, listener_id, world="stable"):
    ids = [f"T{i:02d}" for i in range(1, 31)]
    rng.shuffle(ids)
    constellations = [ids[0:8], ids[8:16], ids[16:24]]
    noise_pool = ids[24:30]
    pairs = [(constellations[k][0], noise_pool[k]) for k in range(3)]
    context_map = None
    if world == "context":
        # Overlapping constellations: "quiet" draws from
        # ids[0:8], "morning" from ids[4:12]. The 4 overlapping
        # tracks are ambiguous by seed alone -- only the
        # context label disambiguates their co-members.
        # With disjoint constellations, conditioning adds
        # nothing (the seed already identifies the context),
        # which is why an earlier version of this test failed
        # with blind == conditioned. Overlap is the point.
        constellations = [ids[0:8], ids[4:12], ids[16:24]]
        context_map = {"quiet": 0, "morning": 1}
    return SyntheticListener(listener_id, constellations, noise_pool, pairs, context_map)


def generate_sessions(listener, rng, n_sessions, start=0, world="stable"):
    sessions = []
    for n in range(start, start + n_sessions):
        if world == "random":
            kept = rng.sample([f"T{i:02d}" for i in range(1, 31)], 4)
            sessions.append((f"{listener.listener_id}-s{n}", kept, None))
        elif world == "context":
            context = rng.choice(["quiet", "morning"])
            group = listener.constellations[listener.context_map[context]]
            kept = rng.sample(group, 4)
            sessions.append((f"{listener.listener_id}-s{n}", kept, context))
        else:
            group = rng.choice(listener.constellations)
            kept = rng.sample(group, 4)
            if rng.random() < 0.20:
                kept.append(rng.choice(listener.noise_pool))
            sessions.append((f"{listener.listener_id}-s{n}", kept, None))
    return sessions


def generate_corrections(listener, rng, n_corrections, start=0):
    corrections = []
    all_ids = [f"T{i:02d}" for i in range(1, 31)]
    for n in range(start, start + n_corrections):
        if rng.random() < 0.70:
            rejected, replacement = rng.choice(listener.replacement_pairs)
        else:
            rejected = rng.choice(all_ids)
            replacement = rng.choice([t for t in all_ids if t != rejected])
        corrections.append((rejected, replacement, f"{listener.listener_id}-c{n}"))
    return corrections


def shuffled_sessions(sessions, rng):
    """Duplicate-free swaps, preserving sizes, popularity, uniqueness."""
    shuffled = [list(kept) for _, kept, _ in sessions]
    contexts = [ctx for _, _, ctx in sessions]
    for _ in range(500):
        if len(shuffled) < 2:
            break
        i, j = rng.sample(range(len(shuffled)), 2)
        if not shuffled[i] or not shuffled[j]:
            continue
        a = rng.choice(shuffled[i])
        b = rng.choice(shuffled[j])
        if a == b:
            continue
        if b in shuffled[i] or a in shuffled[j]:
            continue
        shuffled[i][shuffled[i].index(a)] = b
        shuffled[j][shuffled[j].index(b)] = a
    return [(f"shuffled-s{i}", kept, contexts[i]) for i, kept in enumerate(shuffled)]


def shuffled_corrections(corrections, rng):
    """Permute replacements, preserving marginal counts, never
    creating a self-correction. Raises if repair fails -- never
    silently drops a correction."""
    replacements = [rep for _, rep, _ in corrections]
    rng.shuffle(replacements)
    for _ in range(100):
        bad = [i for i, (rej, _, _) in enumerate(corrections) if replacements[i] == rej]
        if not bad:
            break
        i = bad[0]
        rej_i = corrections[i][0]
        swapped = False
        for j in range(len(corrections)):
            if j == i:
                continue
            rej_j = corrections[j][0]
            if replacements[j] != rej_i and replacements[i] != rej_j:
                replacements[i], replacements[j] = replacements[j], replacements[i]
                swapped = True
                break
        if not swapped:
            break
    out = [(rej, replacements[i], sid) for i, (rej, _, sid) in enumerate(corrections)]
    for rej, rep, _ in out:
        if rej == rep:
            raise ValueError("shuffled_corrections: unrepairable self-correction")
    return out


# ------------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------------

def evaluate_next_pick(state, test_sessions, ranker, all_ids, k=3, context_mode="blind"):
    hits = []
    for _, kept, ctx in test_sessions:
        if len(kept) < 2:
            continue
        seed = [kept[0]]
        truth = set(kept[1:])
        if context_mode == "conditioned":
            ranked = ranker(state, seed, all_ids, context=ctx)
        else:
            ranked = ranker(state, seed, all_ids)
        top = set(ranked[:k])
        hits.append(1 if top & truth else 0)
    return statistics.mean(hits) if hits else 0.0


def evaluate_next_pick_recall(state, test_sessions, ranker, all_ids, k=3, context_mode="blind"):
    """Mean Recall@k. Used for the context experiment, where
    Hit@k saturates: a blind ranker almost always gets at
    least one true co-member in the top 3, even when it mixes
    contexts. Recall@k measures how many of the true
    co-members are in the top k, which is what context
    conditioning should improve."""
    recalls = []
    for _, kept, ctx in test_sessions:
        if len(kept) < 2:
            continue
        seed = [kept[0]]
        truth = set(kept[1:])
        if context_mode == "conditioned":
            ranked = ranker(state, seed, all_ids, context=ctx)
        else:
            ranked = ranker(state, seed, all_ids)
        top = set(ranked[:k])
        recalls.append(len(top & truth) / len(truth))
    return statistics.mean(recalls) if recalls else 0.0


def evaluate_replacement(state, test_corrections, ranker, all_ids, k=1):
    hits = []
    for rejected, replacement, _ in test_corrections:
        ranked = ranker(state, rejected, all_ids)
        hits.append(1 if replacement in ranked[:k] else 0)
    return statistics.mean(hits) if hits else 0.0


def _summary(values):
    n = len(values)
    mean = statistics.mean(values) if values else 0.0
    se = (statistics.pstdev(values) / (n ** 0.5)) if n > 1 else 0.0
    return {"mean": round(mean, 3), "min": round(min(values), 3) if values else None,
            "max": round(max(values), 3) if values else None,
            "approx_95ci": [round(mean - 1.96 * se, 3), round(mean + 1.96 * se, 3)],
            "n": n}


def run_experiments(seeds=(1, 2, 3, 4, 5)):
    """Multi-seed experiments. Returns dict; also used by tests."""
    catalog = make_catalog()
    all_ids = sorted(catalog)
    stable_pop, stable_prov, stable_shuf = [], [], []
    rep_pop1, rep_glob1, rep_pair1 = [], [], []
    random_pop, random_prov = [], []
    ctx_blind, ctx_cond, stable_ctx_blind, stable_ctx_cond = [], [], [], []
    for seed in seeds:
        rng = random.Random(seed)
        # Stable world, 12 listeners per seed
        for li in range(12):
            listener = make_listener(rng, f"S{seed}-L{li:02d}", world="stable")
            train = generate_sessions(listener, rng, 30, start=0, world="stable")
            test = generate_sessions(listener, rng, 10, start=30, world="stable")
            state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in train:
                state.add_session(sid, kept, context=ctx)
            stable_pop.append(evaluate_next_pick(state, test, popularity_ranker, all_ids))
            stable_prov.append(evaluate_next_pick(state, test, provenance_ranker, all_ids))
            shuf_state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in shuffled_sessions(train, rng):
                shuf_state.add_session(sid, kept, context=ctx)
            stable_shuf.append(evaluate_next_pick(shuf_state, test, provenance_ranker, all_ids))
            train_corr = generate_corrections(listener, rng, 30, start=0)
            test_corr = generate_corrections(listener, rng, 10, start=30)
            for rej, rep, csid in train_corr:
                state.add_correction(rej, rep, csid, scope="global_note")
            # Session-popularity replacement baseline: most popular
            # track other than the rejected one (popularity_ranker
            # with seed=[rejected] excludes the rejected track).
            rep_pop1.append(evaluate_replacement(state, test_corr, lambda s, r, a: popularity_ranker(s, [r], a), all_ids, k=1))
            rep_glob1.append(evaluate_replacement(state, test_corr, global_replacement_ranker, all_ids, k=1))
            rep_pair1.append(evaluate_replacement(state, test_corr, replacement_ranker, all_ids, k=1))
        # Random world (Idea 1 null)
        for li in range(6):
            listener = make_listener(rng, f"R{seed}-L{li:02d}", world="random")
            train = generate_sessions(listener, rng, 30, start=0, world="random")
            test = generate_sessions(listener, rng, 10, start=30, world="random")
            state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in train:
                state.add_session(sid, kept, context=ctx)
            random_pop.append(evaluate_next_pick(state, test, popularity_ranker, all_ids))
            random_prov.append(evaluate_next_pick(state, test, provenance_ranker, all_ids))
        # Context world (Idea 2)
        for li in range(6):
            listener = make_listener(rng, f"C{seed}-L{li:02d}", world="context")
            train = generate_sessions(listener, rng, 30, start=0, world="context")
            test = generate_sessions(listener, rng, 10, start=30, world="context")
            state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in train:
                state.add_session(sid, kept, context=ctx)
            ctx_blind.append(evaluate_next_pick_recall(state, test, provenance_ranker, all_ids, context_mode="blind"))
            ctx_cond.append(evaluate_next_pick_recall(state, test, provenance_ranker, all_ids, context_mode="conditioned"))
        # Stable world, context-conditioned should NOT win (labels are None)
        for li in range(6):
            listener = make_listener(rng, f"SC{seed}-L{li:02d}", world="stable")
            train = generate_sessions(listener, rng, 30, start=0, world="stable")
            test = generate_sessions(listener, rng, 10, start=30, world="stable")
            state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in train:
                state.add_session(sid, kept, context=ctx)
            # Context labels are None here; conditioned with ctx=None
            # is identical to blind by construction -- check it.
            stable_ctx_blind.append(evaluate_next_pick_recall(state, test, provenance_ranker, all_ids, context_mode="blind"))
            stable_ctx_cond.append(evaluate_next_pick_recall(state, test, provenance_ranker, all_ids, context_mode="conditioned"))
    return {
        "seeds": list(seeds),
        "stable_next_pick_hit_at_3": {
            "popularity": _summary(stable_pop),
            "provenance": _summary(stable_prov),
            "provenance_shuffled_control": _summary(stable_shuf),
        },
        "replacement_hit_at_1": {
            "session_popularity": _summary(rep_pop1),
            "global_replacement": _summary(rep_glob1),
            "pair_specific": _summary(rep_pair1),
        },
        "idea1_random_world_hit_at_3": {
            "popularity": _summary(random_pop),
            "provenance": _summary(random_prov),
            "note": "In a world with no constellations, provenance must NOT beat popularity.",
        },
        "idea2_context_world_recall_at_3": {
            "context_blind": _summary(ctx_blind),
            "context_conditioned": _summary(ctx_cond),
            "stable_world_context_blind": _summary(stable_ctx_blind),
            "stable_world_context_conditioned": _summary(stable_ctx_cond),
            "note": "Recall@3, not Hit@3: Hit@3 saturates for ambiguous seeds. RESULT: conditioned does NOT reliably beat blind in this world (means equal, CIs overlapping). See README: halving training data offsets the context benefit, and blind already benefits from overlap tracks. This is a negative result for the naive hard-filter version, not a forced win.",
        },
    }


def main():
    import json
    print("Muse Constellation Lab v0.2 -- synthetic only, NOT real listeners")
    print(json.dumps(run_experiments(), indent=2))


if __name__ == "__main__":
    main()
