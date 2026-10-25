"""
Muse Constellation Lab v0.2.2 -- INDEPENDENT implementation
TLR-R2-MUSE-AGENT-01 (v0.2) + TLR-R2-MUSE-REPAIR-01 (v0.2.1 repairs)
+ final narrow integrity repair (v0.2.2, Sol re-review of PR #72
at commit 5dc1765b)
experiments/muse-agent-01/

v0.2.2 repairs (two cases only, no feature expansion):
  F1. validate_contribution: unhashable rejected_id /
      replacement_id raised TypeError during set membership.
      ID types are now validated as non-empty strings BEFORE
      membership is checked.
  F2. validate_system_claims: unhashable claim type raised
      TypeError during allowlist membership. The type is now
      validated as a non-empty string BEFORE allowlist lookup.
  Also documented: an allowed claim type is NOT necessarily
  a fully evidence-supported claim; stronger provenance
  binding remains a future integration requirement.

v0.2.1 repair summary (Sol review of PR #72, commit a6d08263):
  R1 P0 corrections/associations containers: int/bool/string/dict
     containers crashed or produced misleading per-character
     errors. Now validated as lists first; malformed containers
     return a single structured error.
  R2 P0 unhashable title/artist: title/artist are type-checked
     as strings before any tuple/dict-key use. List/dict
     identity fields return an error, never TypeError.
  R3 P1 veto revocation: unveto() now records an explicit
     revocation event in the ledger, and avoidance_view()
     distinguishes historical events from active restrictions.
  R4 P1 hard exclusion in A1: negative tags remain SOFT
     (score subtraction). Hard exclusion is by recording ID
     (hard_excluded, plus global vetoes) and cannot be
     overridden by a high positive score.
  R5 P1 session/context boundaries: session-scoped corrections
     now REQUIRE a known session_id (None is rejected for
     session scope). Session-local pairs are stored separately
     from global correction-pair evidence and never leak into
     global rankers. Context-conditioned rankers use only
     sessions and correction evidence whose context matches
     (global, session-less evidence counts in both; unknown-
     context evidence counts only in blind ranking).
  R6 P1 Stage 0 allowlist: system claims are limited to
     HUMAN_REPORT / TRACK_METADATA / SYSTEM_HYPOTHESIS /
     UNKNOWN, each with evidence appropriate to its type.
     Disguised field names (waveform, entrance, verified
     acoustic structure, etc.) are rejected, and
     authorized_audio=True never unlocks a measurement claim.
     Listener-authored text ("I love the guitar entrance")
     remains allowed as a human report and is never relabelled
     as a verified acoustic observation.
  Preserved: all 27 v0.2 tests, all v0.2 synthetic comparisons,
  and the negative result for naive context conditioning
  (conditioned 0.411 vs blind 0.412, seeds 1-5).

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
      session. In v0.2, session scope with session_id=None was
      accepted; v0.2.1 repairs that (see R5): session scope
      requires a known session, global scope is the operation
      for session-less general preference evidence.
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
  (kept_together / replaced / not_tonight / never /
  never_revoked) and carry a session context label. A
  context-conditioned ranker uses only sessions from the
  queried context; a context-blind ranker uses all sessions.
  Both receive the same context label (blind ignores it), so
  the comparison is about use, not access. RESULT (v0.2,
  preserved in v0.2.1): naive hard-filter conditioning does
  NOT reliably beat blind (0.411 vs 0.412); on stable
  listeners it is identical. That negative result is kept
  visible, not tuned away.
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
    "mfcc", "chroma", "tempo_", "bpm", "waveform",
    "entrance", "onset", "pitch_", "frequency_",
    "verified_acoustic", "verified_audio",
    "instrument_entrance", "musical_structure",
)
# Stage 0 allowlist for SYSTEM-authored claims (v0.2.1, R6).
# Listener-authored text in listener_report / listener_note is
# NOT a system claim and is not subject to this allowlist.
_SYSTEM_CLAIM_TYPES = {"HUMAN_REPORT", "TRACK_METADATA", "SYSTEM_HYPOTHESIS", "UNKNOWN"}


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


def _validate_system_claims(claims):
    """Stage 0 allowlist for system-authored claims (v0.2.1 R6).

    Returns error list. A claim must be a dict, its type must
    be in the allowlist, it must carry evidence appropriate
    to that type, it must not contain a disguised measurement
    field, and authorized_audio=True must never unlock it.
    Listener text is NOT checked here; only claim structure.

    Allowlist limit, stated explicitly (v0.2.2): passing this
    gate means only that a claim's TYPE is allowed and its
    required evidence field is present. It does NOT mean the
    claim is fully evidence-supported, true, or provenance-
    bound. A HUMAN_REPORT with listener_text passes even
    though this gate cannot verify who actually wrote the
    text; a TRACK_METADATA claim passes even though its
    title/artist are not checked against a source record;
    a SYSTEM_HYPOTHESIS passes as a hypothesis, not as a
    finding. Stronger provenance binding — signed listener
    attestation, source-record linkage, and a verification
    workflow for metadata claims — remains a FUTURE
    integration requirement and is NOT implemented here.
    """
    errors = []
    if claims is None:
        return errors
    if not isinstance(claims, list):
        return ["claims must be a list"]
    for i, claim in enumerate(claims):
        prefix = f"claims[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claim_type = claim.get("type")
        # v0.2.2: validate the type BEFORE allowlist membership.
        # Previously `claim_type not in _SYSTEM_CLAIM_TYPES`
        # raised TypeError (unhashable) for list/dict types.
        if not isinstance(claim_type, str) or not claim_type:
            errors.append(f"{prefix}.type must be a non-empty string")
            claim_type = None
        elif claim_type not in _SYSTEM_CLAIM_TYPES:
            errors.append(
                f"{prefix}.type {claim_type!r} is not in the Stage 0 "
                f"allowlist (HUMAN_REPORT, TRACK_METADATA, "
                f"SYSTEM_HYPOTHESIS, UNKNOWN)"
            )
        if claim.get("authorized_audio") is True:
            errors.append(
                f"{prefix}: authorized_audio=True does not unlock "
                f"any acoustic claim at Stage 0"
            )
        # Disguised measurement fields, whatever the type label.
        for key, value in claim.items():
            if isinstance(key, str) and any(s in key for s in _MEASUREMENT_FIELD_SUBSTRINGS):
                errors.append(f"{prefix}.{key}: measurement field rejected at Stage 0")
            if key in ("verified", "confirmed", "validated") and value is True:
                errors.append(f"{prefix}.{key}: verified/confirmed claims are not permitted at Stage 0")
            if key == "evidence_level" and value in ("verified", "confirmed", "validated"):
                errors.append(f"{prefix}.evidence_level: verified/confirmed claims are not permitted at Stage 0")
        # Evidence appropriate to the type.
        if claim_type == "HUMAN_REPORT":
            if not any(isinstance(claim.get(k), str) and claim[k] for k in ("listener_text", "listener_note", "text")):
                errors.append(f"{prefix}: HUMAN_REPORT requires listener_text, listener_note, or text")
        elif claim_type == "TRACK_METADATA":
            if not any(k in claim for k in ("title", "artist", "metadata", "track")):
                errors.append(f"{prefix}: TRACK_METADATA requires title, artist, metadata, or track")
        elif claim_type == "SYSTEM_HYPOTHESIS":
            if claim.get("hypothesis") is not None and not isinstance(claim.get("hypothesis"), str):
                errors.append(f"{prefix}.hypothesis must be a string")
            if claim.get("uncertainty") is not None and not isinstance(claim.get("uncertainty"), str):
                errors.append(f"{prefix}.uncertainty must be a string")
        elif claim_type == "UNKNOWN":
            # UNKNOWN must assert nothing: no measurement fields
            # (already checked above) and no verified flag.
            pass
    return errors


# Public alias: the Stage 0 gate is part of the public API
# for reviewers, not a private helper.
validate_system_claims = _validate_system_claims


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
            # v0.2.1 R2: only build the title/artist tuple key
            # AFTER confirming both fields are strings. A list
            # or dict title/artist previously raised TypeError
            # (unhashable) when used as a dict key. The
            # type errors above already cover those cases.
            if track.get("identity_status") == "unverified" and isinstance(
                track.get("title"), str
            ) and isinstance(track.get("artist"), str):
                key = (track.get("title"), track.get("artist"))
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
    # v0.2.1 R1: validate the outer container BEFORE iterating.
    # Previously int/bool raised TypeError, and string/dict
    # produced misleading per-character / per-key errors.
    corrections = data.get("corrections", [])
    if corrections is None:
        corrections = []
    if not isinstance(corrections, list):
        errors.append("corrections must be a list")
        corrections = []
    for i, corr in enumerate(corrections):
        if not isinstance(corr, dict):
            errors.append(f"corrections[{i}] must be an object")
            continue
        # v0.2.2: validate ID types BEFORE set membership.
        # Previously `corr.get(fname) not in seen_ids` raised
        # TypeError (unhashable) for list/dict IDs. A non-string
        # ID is a structured error, never a crash, and the
        # differ-check below (equality, not hashing) is safe.
        for fname in ("rejected_id", "replacement_id"):
            val = corr.get(fname)
            if not isinstance(val, str) or not val:
                errors.append(f"corrections[{i}].{fname} must be a non-empty string")
            elif val not in seen_ids:
                errors.append(f"corrections[{i}].{fname} references unknown song_id: {val!r}")
        if corr.get("rejected_id") == corr.get("replacement_id"):
            errors.append(f"corrections[{i}] rejected and replacement must differ")
    associations = data.get("associations", [])
    if associations is None:
        associations = []
    if not isinstance(associations, list):
        errors.append("associations must be a list")
        associations = []
    for i, assoc in enumerate(associations):
        if not isinstance(assoc, dict):
            errors.append(f"associations[{i}] must be an object")
            continue
        ids = _string_ids(assoc.get("song_ids", []), f"associations[{i}].song_ids", errors)
        for sid in ids:
            if sid not in seen_ids:
                errors.append(f"associations[{i}] references unknown song_id: {sid}")
    # Scan everything EXCEPT claims for measurement markers;
    # claims go through the Stage 0 allowlist below, so a
    # disallowed claim is reported once, by its own rule.
    errors.extend(_scan_measurements({k: v for k, v in data.items() if k != "claims"}))
    if "claims" in data:
        errors.extend(_validate_system_claims(data.get("claims")))
    return errors


# ------------------------------------------------------------------
# Listener state with typed edge ledger
# ------------------------------------------------------------------

@dataclass
class Edge:
    kind: str  # kept_together | replaced | not_tonight | never | never_revoked
    a: str
    b: str | None
    session_id: str | None
    context: str | None


@dataclass
class ListenerState:
    catalog: set = field(default_factory=set)
    # sessions: list of (session_id, frozenset, context or None), in order
    sessions: list = field(default_factory=list)
    # Global correction-pair evidence (general preference change).
    # Session-local pairs are NOT stored here (see below).
    corrections: list = field(default_factory=list)  # (rejected, replacement, session_id_or_note)
    # Session-local pairs: session_id -> [(rejected, replacement)].
    # These affect ONLY that session's recommendation, never
    # global rankers, and never another session or context.
    session_corrections: dict = field(default_factory=dict)
    vetoes: set = field(default_factory=set)
    # Ordered veto history: ("veto", song_id) / ("revoke", song_id).
    # The active set (self.vetoes) is the replay of this history;
    # avoidance_view() exposes both, so history never masquerades
    # as a current restriction.
    veto_history: list = field(default_factory=list)
    reports: dict = field(default_factory=dict)
    session_suppressions: dict = field(default_factory=dict)  # session_id -> set(rejected)
    edges: list = field(default_factory=list)
    silence_events: int = 0
    click_out_events: int = 0

    def _require_known(self, song_id):
        if not isinstance(song_id, str) or song_id not in self.catalog:
            raise ValueError(f"unknown song_id: {song_id!r}")

    def _session_context(self, session_id):
        for sid, _, ctx in self.sessions:
            if sid == session_id:
                return ctx
        return None

    def _snapshot(self):
        return (list(self.sessions), list(self.corrections), set(self.vetoes),
                dict(self.reports), {k: set(v) for k, v in self.session_suppressions.items()},
                list(self.edges), list(self.veto_history),
                {k: list(v) for k, v in self.session_corrections.items()})

    def avoidance_view(self):
        """Effective view vs history, unambiguously separated.

        Returns active vetoes (current instruction), the ordered
        veto history (including revocations), active session
        suppressions, and historical edge kinds. A caller that
        only reads edges must NOT infer that a 'never' edge is
        still active if a later 'never_revoked' edge exists.
        """
        return {
            "active_vetoes": sorted(self.vetoes),
            "veto_history": list(self.veto_history),
            "active_session_suppressions": {k: sorted(v) for k, v in self.session_suppressions.items()},
            "historical_edge_kinds_in_order": [e.kind for e in self.edges],
        }

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
        """Four clearly distinguishable operations (v0.2.1 R5):

        * Session-local replacement: scope="session", session_id
          REQUIRED and must be a known session. Stored ONLY in
          session_corrections / session_suppressions for that
          session. Never added to global correction-pair evidence,
          never applied to another session or context.
        * Historical correction-pair evidence / general
          preference change: scope="global" (alias "global_note"
          retained for v0.2 compatibility). Stored in
          self.corrections. session_id, if given, is provenance
          only (e.g. a correction ID in synthetic fixtures); it
          does NOT create a session suppression, and it is NOT
          required to be a known session.
        * Permanent avoidance: veto() / unveto(), not this method.

        Behaviour change from v0.2, explained: v0.2 accepted
        scope="session" with session_id=None and stored it in
        the global list, which is exactly the boundary failure
        Sol identified (a session-scoped correction without a
        session). That combination now raises ValueError.
        """
        self._require_known(rejected_id)
        self._require_known(replacement_id)
        if rejected_id == replacement_id:
            raise ValueError("correction rejected and replacement must differ")
        if scope not in ("session", "global", "global_note"):
            raise ValueError("correction scope must be 'session', 'global', or 'global_note'")
        if scope == "session":
            if session_id is None:
                raise ValueError("session-scoped correction requires a session_id")
            if not any(sid == session_id for sid, _, _ in self.sessions):
                raise ValueError(f"correction references unknown session_id: {session_id!r}")
            # Validate before mutating: only now append.
            self.session_corrections.setdefault(session_id, []).append((rejected_id, replacement_id))
            self.session_suppressions.setdefault(session_id, set()).add(rejected_id)
            self.edges.append(Edge("replaced", rejected_id, replacement_id, session_id,
                                   self._session_context(session_id)))
            self.edges.append(Edge("not_tonight", rejected_id, None, session_id,
                                   self._session_context(session_id)))
        else:
            self.corrections.append((rejected_id, replacement_id, session_id))
            self.edges.append(Edge("replaced", rejected_id, replacement_id, session_id, None))

    # Convenience wrappers, naming the operation explicitly.
    def add_session_correction(self, rejected_id, replacement_id, session_id):
        return self.add_correction(rejected_id, replacement_id, session_id, scope="session")

    def add_global_correction(self, rejected_id, replacement_id, session_id=None):
        return self.add_correction(rejected_id, replacement_id, session_id, scope="global")

    def veto(self, song_id):
        self._require_known(song_id)
        self.vetoes.add(song_id)
        self.veto_history.append(("veto", song_id))
        self.edges.append(Edge("never", song_id, None, None, None))

    def unveto(self, song_id):
        # v0.2.1 R3: revocation is an explicit event, not a
        # silent discard. The historical 'never' edge remains
        # in the ledger, followed by a 'never_revoked' edge,
        # and avoidance_view() shows active vetoes as empty.
        if song_id in self.vetoes:
            self.vetoes.discard(song_id)
            self.veto_history.append(("revoke", song_id))
            self.edges.append(Edge("never_revoked", song_id, None, None, None))
        else:
            # Revoking a non-veto is a no-op for the active set,
            # but record it so the history is not ambiguous.
            self.veto_history.append(("revoke_noop", song_id))

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
        self.session_corrections.clear()
        self.vetoes.clear()
        self.veto_history.clear()
        self.reports.clear()
        self.session_suppressions.clear()
        self.edges.clear()
        self.silence_events = 0
        self.click_out_events = 0

    def derived_counts(self):
        """Counts derived ONLY from current sessions/corrections.

        After delete_all() these must be zero -- there is no
        separate cache or append-only log retaining personal text.
        The ledger itself is in-memory state and is cleared by
        delete_all(); it is not an external append-only log.
        """
        pop = {}
        for _, kept, _ in self.sessions:
            for sid in kept:
                pop[sid] = pop.get(sid, 0) + 1
        n_session_corr = sum(len(v) for v in self.session_corrections.values())
        return {"session_track_counts": pop,
                "n_corrections": len(self.corrections) + n_session_corr,
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


def _pair_scores(state, seed_set, context=None, session_id=None):
    """Correction-pair scores, with context/session boundaries (R5).

    * Global corrections: counted always when context is None.
      When context is given, counted only if the correction is
      session-less (general preference, context-independent)
      or its session_id belongs to a session with that context.
      A global correction whose session_id matches NO known
      session has unknown context and is therefore EXCLUDED
      from conditioned ranking (it still counts in blind ranking).
    * Session-local corrections: counted ONLY when session_id
      matches the queried session. Never counted in global
      rankers, never counted for another session or context.
    """
    pair = {}
    for rej, rep, csid in state.corrections:
        if rej in seed_set:
            if context is None:
                pair[rep] = pair.get(rep, 0) + 1
            elif csid is None:
                pair[rep] = pair.get(rep, 0) + 1
            elif any(sid == csid for sid, _, _ in state.sessions) and state._session_context(csid) == context:
                pair[rep] = pair.get(rep, 0) + 1
            # else: unknown-context or other-context evidence --
            # excluded from conditioned ranking, by design.
    if session_id is not None:
        for rej, rep in state.session_corrections.get(session_id, []):
            if rej in seed_set:
                pair[rep] = pair.get(rep, 0) + 1
    return pair


def provenance_ranker(state, seed, all_ids, context=None, session_id=None):
    """Seed-conditioned co-occurrence, optionally context-restricted.

    If context is given, only sessions with that context are used,
    and only context-matching correction evidence is used (see
    _pair_scores). The caller must pass the context label to
    BOTH rankers in a comparison; the blind ranker simply
    passes context=None. That is equal access, different use.
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
    pair = _pair_scores(state, seed_set, context=context, session_id=session_id)
    counts = _popularity(state, sessions)
    return sorted(_base_candidates(state, seed, all_ids, session_id=session_id),
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
    ranked = provenance_ranker(state, seed, all_ids, context=context, session_id=session_id)
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
    pair = _pair_scores(state, seed_set, context=context, session_id=session_id)
    candidates = _base_candidates(state, seed, all_ids, session_id=session_id)
    recommended = [c for c in ranked if c in candidates and (co.get(c, 0) > 0 or pair.get(c, 0) > 0)]
    not_recommended = [c for c in candidates if c not in recommended]
    return recommended, not_recommended, len(recommended) == 0


def replacement_ranker(state, rejected_id, all_ids):
    """Global replacement ranking. Uses ONLY global correction
    evidence (state.corrections). Session-local pairs are
    deliberately NOT used here, so a session-local rejection
    cannot become a universal replacement rule."""
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


def a1_explicit_ranker(explicit_tokens, negative_tokens, catalogue_tags, all_ids, vetoes, hard_excluded=None):
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

    Negative preferences, distinguished (v0.2.1 R4):
    * SOFT negative (negative_tokens, tag-level): "I'm not
      particularly interested in polished music tonight."
      Subtracts from the score. A track with a high positive
      score can still appear, just lower. Tag-level negatives
      are NOT hard filters, because a tag is not a recording
      identity and a single tag must not veto a whole recording.
    * HARD exclusion (hard_excluded, recording IDs, plus
      global vetoes): "Do not recommend this recording."
      Excludes the recording entirely, regardless of positive
      score. No positive score can reintroduce it.
    """
    explicit = set(explicit_tokens or [])
    negative = set(negative_tokens or [])
    hard = set(hard_excluded or [])
    scored = []
    for cid in all_ids:
        if cid in vetoes or cid in hard:
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
    print("Muse Constellation Lab v0.2.2 -- synthetic only, NOT real listeners")
    print(json.dumps(run_experiments(), indent=2))


if __name__ == "__main__":
    main()
