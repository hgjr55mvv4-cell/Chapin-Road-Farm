"""PAC-01-DEV-01: synthetic-only listening experiment harness.

A small, reproducible instrument for comparing two recommendation
conditions fairly. It is NOT a theory of musical meaning, emotion, or
reward, and it contains no inferred emotional states, neural variables,
or psychological profiles.

What it does:
  * holds a synthetic catalog of fictional recordings (all musical
    descriptors are fabricated and labelled synthetic);
  * freezes two rankings (A1 conversational baseline, B-metadata) before
    any queue is built;
  * builds a balanced, seeded, condition-blind listening queue, or
    refuses with INSUFFICIENT_BALANCE instead of fabricating one;
  * records observations only in the states the assignment defines, and
    keeps unheard / uncertain / familiar items out of binary math.

What it never does:
  * claim that a mock ranking result shows acoustic intelligence,
    preference learning, or that one condition is better;
  * treat queue membership, or opening a link, as evidence of hearing;
  * treat absence from a historical playlist as a negative label;
  * let evaluation outcomes modify frozen rankings or queues.

Python 3 standard library only. No network, no audio, no real data.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

__version__ = "0.1.0"


# ---------------------------------------------------------------- errors

class HarnessError(ValueError):
    """Base class for all harness validation / fairness errors."""


class ValidationError(HarnessError):
    """Corrupt, malformed, or unknown synthetic input."""


class SnapshotMismatch(HarnessError):
    """The two conditions were not ranked over the same catalog snapshot."""


class InsufficientBalance(HarnessError):
    """A fair, balanced comparison cannot be constructed from these inputs.

    Raised instead of silently substituting unrelated songs.
    """


class InvalidTransition(HarnessError):
    """An observation-state transition the schema does not allow."""


class DeletedSessionError(HarnessError):
    """Operation attempted on a deleted listener session."""


# ------------------------------------------------------------- validation

def _require_str(value, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string")
    return value


def _require_str_tuple(values, field_name: str) -> Tuple[str, ...]:
    if isinstance(values, str) or not isinstance(values, (list, tuple)):
        raise ValidationError(f"{field_name} must be a list or tuple of strings")
    out = []
    for item in values:
        out.append(_require_str(item, f"{field_name} item"))
    return tuple(out)


# ------------------------------------------------------------ observations

class ObservationState(str, Enum):
    """The only observation states the harness recognises.

    KEPT_AFTER_LISTENING / PASSED_AFTER_LISTENING require an explicit
    report of sufficient exposure (heard_enough=True). Nothing else
    counts as hearing: queue membership does not, opening a link does
    not, and absence from a historical playlist does not.
    """

    KEPT_AFTER_LISTENING = "KEPT_AFTER_LISTENING"
    PASSED_AFTER_LISTENING = "PASSED_AFTER_LISTENING"
    MAYBE = "MAYBE"
    NOT_HEARD_ENOUGH = "NOT_HEARD_ENOUGH"
    ALREADY_FAMILIAR = "ALREADY_FAMILIAR"
    UNKNOWN = "UNKNOWN"


# States that may enter a binary keep/pass calculation.
_BINARY_STATES = {
    ObservationState.KEPT_AFTER_LISTENING,
    ObservationState.PASSED_AFTER_LISTENING,
}
# States that are terminal for record(): changing them requires an
# explicit correction (see Session.correct), so a keep/pass cannot be
# silently overwritten by a later casual report.
_TERMINAL_STATES = _BINARY_STATES | {ObservationState.ALREADY_FAMILIAR}


@dataclass(frozen=True)
class Observation:
    """One explicitly reported observation.

    Extension fields (all optional, all explicitly reported, none scored):
      passage_note:      a listener-identified passage, e.g. "bridge".
      replay_desire:     True/False only if the listener stated a desire
                         to hear the song again; None means not stated.
      free_text_reason:  a freely supplied description of why a song
                         matters, in the listener's own words.
      preference_change: an explicitly stated change in preference over
                         time, e.g. "liked more on second hearing".
    The harness stores these verbatim and never converts them into an
    emotion score, a meaning score, or any inferred state.
    """

    song_id: str
    state: ObservationState
    heard_enough: bool = False
    passage_note: Optional[str] = None
    replay_desire: Optional[bool] = None
    free_text_reason: Optional[str] = None
    preference_change: Optional[str] = None

    def __post_init__(self):
        _require_str(self.song_id, "song_id")
        if not isinstance(self.state, ObservationState):
            raise ValidationError(f"unknown observation state: {self.state!r}")
        if self.state in _BINARY_STATES and not self.heard_enough:
            raise ValidationError(
                f"{self.state.value} requires heard_enough=True; "
                "unheard or partially heard items must not be labelled "
                "keep/pass"
            )
        if self.replay_desire is not None and not isinstance(
            self.replay_desire, bool
        ):
            raise ValidationError("replay_desire must be True, False, or None")
        for name in ("passage_note", "free_text_reason", "preference_change"):
            value = getattr(self, name)
            if value is not None:
                _require_str(value, name)


# ---------------------------------------------------------------- catalog

@dataclass(frozen=True)
class SyntheticRecording:
    """One fictional recording. Every musical descriptor is synthetic.

    `key`, `tempo_bpm`, `vocal_style`, `rhythm`, and `timbre` are
    fabricated values used only to exercise the comparison machinery.
    They are not measurements of any real recording.
    """

    recording_id: str
    artist: str
    title: str
    release_category: str  # e.g. "single", "album track", "ep track"
    genre_tags: Tuple[str, ...] = ()
    key: str = "UNKNOWN"
    tempo_bpm: int = 0
    vocal_style: str = "UNKNOWN"
    rhythm: str = "UNKNOWN"
    timbre: str = "UNKNOWN"
    passage_annotations: Tuple[str, ...] = ()

    def __post_init__(self):
        _require_str(self.recording_id, "recording_id")
        _require_str(self.artist, "artist")
        _require_str(self.title, "title")
        _require_str(self.release_category, "release_category")
        if not isinstance(self.tempo_bpm, int) or isinstance(
            self.tempo_bpm, bool
        ) or self.tempo_bpm < 0:
            raise ValidationError("tempo_bpm must be a non-negative integer")


@dataclass
class Catalog:
    """A frozen snapshot of synthetic recordings."""

    snapshot_id: str
    recordings: Dict[str, SyntheticRecording] = field(default_factory=dict)

    def __post_init__(self):
        _require_str(self.snapshot_id, "snapshot_id")

    def __contains__(self, recording_id: str) -> bool:
        return recording_id in self.recordings

    def __len__(self) -> int:
        return len(self.recordings)


def build_catalog(snapshot_id: str, items: Iterable) -> Catalog:
    """Build a catalog from SyntheticRecording objects or plain dicts.

    Raises ValidationError on duplicate IDs, missing fields, wrong
    types, or unknown keys. A dict item must carry exactly the fields
    of SyntheticRecording (genre_tags / passage_annotations may be
    lists; they are normalised to tuples).
    """
    _require_str(snapshot_id, "snapshot_id")
    recordings: Dict[str, SyntheticRecording] = {}
    for raw in items:
        if isinstance(raw, SyntheticRecording):
            rec = raw
        elif isinstance(raw, Mapping):
            data = dict(raw)
            if "recording_id" not in data:
                raise ValidationError("recording item missing recording_id")
            unknown = set(data) - set(SyntheticRecording.__dataclass_fields__)
            if unknown:
                raise ValidationError(f"unknown recording fields: {sorted(unknown)}")
            for key in ("genre_tags", "passage_annotations"):
                if key in data:
                    data[key] = _require_str_tuple(data[key], key)
            try:
                rec = SyntheticRecording(**data)
            except TypeError as exc:
                raise ValidationError(f"malformed recording: {exc}") from exc
        else:
            raise ValidationError(
                f"catalog items must be recordings or dicts, got {type(raw).__name__}"
            )
        if rec.recording_id in recordings:
            raise ValidationError(f"duplicate recording_id: {rec.recording_id}")
        recordings[rec.recording_id] = rec
    if not recordings:
        raise ValidationError("catalog must contain at least one recording")
    return Catalog(snapshot_id=snapshot_id, recordings=recordings)


def demo_catalog() -> Catalog:
    """Twelve fictional recordings by six fictional artists.

    Designed so the two mock rankers (below) overlap only partially:
    they share some titles and each contributes unique titles, which
    is what a balanced comparison needs. Artist counts are kept low
    so the default per-artist cap (2) does not force a refusal.
    """
    rows = [
        ("SYN-001", "The Paper Lanterns", "Harbor Light Study", "album track",
         ("synthetic folk",), "C major", 96, "sung", "steady", "warm"),
        ("SYN-002", "The Paper Lanterns", "Winter Ledger", "album track",
         ("synthetic folk", "ballad"), "G major", 72, "sung", "steady", "warm"),
        ("SYN-003", "Juno Field", "Static Garden", "single",
         ("synthetic pop",), "D minor", 120, "sung", "driving", "bright"),
        ("SYN-004", "Juno Field", "Paper Compass", "single",
         ("synthetic pop", "synthetic folk"), "A minor", 104, "sung", "steady", "bright"),
        ("SYN-005", "Marlowe Vale", "Low Tide Answer", "ep track",
         ("synthetic folk",), "E minor", 88, "spoken-sung", "sparse", "dry"),
        ("SYN-006", "Marlowe Vale", "Gravel Road Hymn", "ep track",
         ("synthetic folk",), "C major", 100, "sung", "steady", "warm"),
        ("SYN-007", "Kite & Anchor", "Signal Fire", "single",
         ("synthetic rock",), "E major", 132, "sung", "driving", "bright"),
        ("SYN-008", "Kite & Anchor", "North Field", "single",
         ("synthetic rock", "synthetic folk"), "D major", 112, "sung", "steady", "warm"),
        ("SYN-009", "Sable Reed", "Quiet Arithmetic", "album track",
         ("synthetic folk",), "A minor", 92, "sung", "sparse", "dry"),
        ("SYN-010", "Sable Reed", "Blue Hour Cartography", "album track",
         ("synthetic pop",), "F major", 108, "sung", "steady", "bright"),
        ("SYN-011", "Northlight Trio", "Second Winter", "album track",
         ("synthetic folk",), "G major", 84, "sung", "steady", "warm"),
        ("SYN-012", "Northlight Trio", "Map of Small Rooms", "album track",
         ("synthetic folk", "ballad"), "C major", 98, "spoken-sung", "sparse", "dry"),
    ]
    items = [
        SyntheticRecording(
            recording_id=r[0], artist=r[1], title=r[2], release_category=r[3],
            genre_tags=r[4], key=r[5], tempo_bpm=r[6], vocal_style=r[7],
            rhythm=r[8], timbre=r[9],
        )
        for r in rows
    ]
    return build_catalog("demo-snapshot-001", items)


# ---------------------------------------------------------------- rankings

@dataclass(frozen=True)
class Ranking:
    """A frozen ranking from one condition.

    The harness does not implement the conversational preference system
    behind A1; it only preserves that system's ranking, eligibility,
    stated preferences, version, and provenance exactly as supplied.
    Rankings are tuples, so freezing is structural: later mutation of
    a caller's list cannot change a Ranking already built.
    """

    condition: str  # "A1" or "B-metadata"
    ranked_ids: Tuple[str, ...]
    catalog_snapshot_id: str
    context_id: str
    preferences: Tuple[str, ...]
    ranker_version: str
    provenance: str

    def __post_init__(self):
        if self.condition not in ("A1", "B-metadata"):
            raise ValidationError(f"unknown condition: {self.condition!r}")
        if not self.ranked_ids:
            raise ValidationError("ranking must contain at least one id")
        object.__setattr__(
            self, "ranked_ids", _require_str_tuple(self.ranked_ids, "ranked_ids")
        )
        if len(set(self.ranked_ids)) != len(self.ranked_ids):
            raise ValidationError("ranking contains duplicate ids")
        _require_str(self.catalog_snapshot_id, "catalog_snapshot_id")
        _require_str(self.context_id, "context_id")
        _require_str(self.ranker_version, "ranker_version")
        _require_str(self.provenance, "provenance")
        object.__setattr__(
            self, "preferences", _require_str_tuple(self.preferences, "preferences")
        )


def build_ranking(condition: str, ranked_ids: Sequence[str],
                  catalog_snapshot_id: str, context_id: str,
                  preferences: Sequence[str], ranker_version: str,
                  provenance: str) -> Ranking:
    """Freeze a ranking supplied by an external (mock) ranker."""
    return Ranking(
        condition=condition,
        ranked_ids=tuple(ranked_ids),
        catalog_snapshot_id=catalog_snapshot_id,
        context_id=context_id,
        preferences=tuple(preferences),
        ranker_version=ranker_version,
        provenance=provenance,
    )


def mock_a1_ranking(catalog: Catalog, preferences: Sequence[str],
                    context_id: str = "demo-context", top_n: int = 8) -> Ranking:
    """Mock conversational-preference baseline (A1).

    Ranks by number of stated-preference genre tags matched, ties by
    recording id, and returns the top `top_n` recommendations (a
    recommendation list, not a permutation of the whole catalog).
    Uses NO synthetic musical descriptors (key/tempo) -- that is
    precisely the experimental difference from B-metadata.
    """
    prefs = set(preferences)
    scored = sorted(
        catalog.recordings.values(),
        key=lambda r: (-len(set(r.genre_tags) & prefs), r.recording_id),
    )
    return build_ranking(
        "A1", [r.recording_id for r in scored[:top_n]], catalog.snapshot_id,
        context_id, preferences, "mock-a1-v0.1",
        "mock conversational preference system (simulated ranking only)",
    )


def mock_b_ranking(catalog: Catalog, preferences: Sequence[str],
                   preferred_tempo: int = 100, preferred_key: str = "C major",
                   context_id: str = "demo-context", top_n: int = 8) -> Ranking:
    """Mock B-metadata ranking: same preferences PLUS synthetic descriptors.

    Same genre-match score as A1, plus one point for a tempo within
    12 BPM of the preferred tempo and one point for the preferred key,
    returning the top `top_n` recommendations. The extra points are
    the entire, auditable experimental difference.
    """
    prefs = set(preferences)

    def score(rec: SyntheticRecording) -> int:
        value = len(set(rec.genre_tags) & prefs)
        if abs(rec.tempo_bpm - preferred_tempo) <= 12:
            value += 1
        if rec.key == preferred_key:
            value += 1
        return value

    scored = sorted(
        catalog.recordings.values(),
        key=lambda r: (-score(r), r.recording_id),
    )
    return build_ranking(
        "B-metadata", [r.recording_id for r in scored[:top_n]],
        catalog.snapshot_id,
        context_id, preferences, "mock-b-v0.1",
        "mock ranking: A1 preferences + synthetic key/tempo descriptors",
    )


# -------------------------------------------------------------- comparison

@dataclass(frozen=True)
class Comparison:
    """A frozen, balanced comparison between two conditions.

    `provenance` maps each queued song to the condition(s) that
    recommended it, so shared recommendations are stored once with
    both provenances -- never duplicated in the queue. `listener_view`
    is the presentation order with NO condition labels: the simulated
    listener view must not reveal which condition recommended a song.
    """

    session_seed: int
    ranking_a: Ranking
    ranking_b: Ranking
    queue_ids: Tuple[str, ...]
    presentation_order: Tuple[str, ...]
    provenance: Tuple[Tuple[str, Tuple[str, ...]], ...]
    dropped_due_to_cap: Tuple[str, ...]
    unbalanced_remainder: Tuple[str, ...]

    def provenance_for(self, song_id: str) -> Tuple[str, ...]:
        for sid, conds in self.provenance:
            if sid == song_id:
                return conds
        raise ValidationError(f"song not in comparison queue: {song_id}")

    def shared_ids(self) -> Tuple[str, ...]:
        return tuple(s for s, c in self.provenance if len(c) == 2)

    def unique_ids(self, condition: str) -> Tuple[str, ...]:
        return tuple(
            s for s, c in self.provenance if c == (condition,)
        )

    def listener_view(self) -> Tuple[str, ...]:
        """Presentation order only. No condition assignment is exposed."""
        return self.presentation_order


def build_comparison(catalog: Catalog, ranking_a: Ranking,
                     ranking_b: Ranking, seed: int,
                     max_per_artist: int = 2) -> Comparison:
    """Freeze both rankings, then build a balanced queue -- or refuse.

    Order of checks (each failure is explicit, none is papered over):
      1. both rankings must reference this catalog snapshot;
      2. every ranked id must exist in the catalog;
      3. the same artist/eligibility cap is applied to both conditions;
      4. at least one condition-unique song per condition must survive
         the cap, otherwise INSUFFICIENT_BALANCE.
    Shared songs come first (in A1 rank order), then balanced pairs
    (one A1-unique, one B-unique, in rank order) until one side runs
    out. Leftover unique songs are reported, not substituted.
    Presentation order is a seeded shuffle of the queue, so the same
    seed + inputs always replay identically.
    """
    if ranking_a.condition != "A1" or ranking_b.condition != "B-metadata":
        raise ValidationError(
            "build_comparison expects ranking_a=A1 and ranking_b=B-metadata"
        )
    for ranking in (ranking_a, ranking_b):
        if ranking.catalog_snapshot_id != catalog.snapshot_id:
            raise SnapshotMismatch(
                f"{ranking.condition} snapshot "
                f"{ranking.catalog_snapshot_id!r} != catalog snapshot "
                f"{catalog.snapshot_id!r}"
            )
        for rid in ranking.ranked_ids:
            if rid not in catalog:
                raise ValidationError(
                    f"{ranking.condition} ranks unknown recording {rid!r}"
                )
    if max_per_artist < 1:
        raise ValidationError("max_per_artist must be at least 1")

    set_a, set_b = set(ranking_a.ranked_ids), set(ranking_b.ranked_ids)
    shared = [rid for rid in ranking_a.ranked_ids if rid in set_b]
    a_only = [rid for rid in ranking_a.ranked_ids if rid not in set_b]
    b_only = [rid for rid in ranking_b.ranked_ids if rid not in set_a]

    # Artist cap, applied identically: shared first, then paired uniques.
    artist_count: Dict[str, int] = {}
    dropped: List[str] = []

    def admit(rid: str) -> bool:
        artist = catalog.recordings[rid].artist
        if artist_count.get(artist, 0) >= max_per_artist:
            dropped.append(rid)
            return False
        artist_count[artist] = artist_count.get(artist, 0) + 1
        return True

    queue: List[str] = []
    provenance: Dict[str, Tuple[str, ...]] = {}
    for rid in shared:
        if admit(rid):
            queue.append(rid)
            provenance[rid] = ("A1", "B-metadata")
    pairs = 0
    for a_rid, b_rid in zip(a_only, b_only):
        # A pair is admitted atomically: if either side fails the cap,
        # neither side is added and neither artist count is consumed,
        # because adding one side alone would unbalance the comparison
        # silently. Both songs are reported in dropped_due_to_cap.
        can_a = artist_count.get(catalog.recordings[a_rid].artist, 0) < max_per_artist
        can_b = artist_count.get(catalog.recordings[b_rid].artist, 0) < max_per_artist
        if can_a and can_b:
            admit(a_rid)
            admit(b_rid)
            queue.extend([a_rid, b_rid])
            provenance[a_rid] = ("A1",)
            provenance[b_rid] = ("B-metadata",)
            pairs += 1
        else:
            if not can_a:
                dropped.append(a_rid)
            if not can_b:
                dropped.append(b_rid)
    if pairs == 0:
        raise InsufficientBalance(
            "no balanced pair survives: at least one condition-unique "
            "song per condition is required, and none was admitted "
            f"(shared={len([r for r in shared if r in queue])}, "
            f"dropped_due_to_cap={dropped})"
        )
    remainder = tuple(
        rid for rid in a_only + b_only
        if rid not in provenance and rid not in dropped
    )
    presentation = list(queue)
    random.Random(seed).shuffle(presentation)
    return Comparison(
        session_seed=seed,
        ranking_a=ranking_a,
        ranking_b=ranking_b,
        queue_ids=tuple(queue),
        presentation_order=tuple(presentation),
        provenance=tuple((sid, provenance[sid]) for sid in queue),
        dropped_due_to_cap=tuple(dropped),
        unbalanced_remainder=remainder,
    )


# ---------------------------------------------------------------- sessions

@dataclass
class Session:
    """A simulated listener session over one frozen comparison.

    Observations are stored per song; the current state is the latest
    explicitly recorded (or corrected) observation. History is kept so
    a correction is auditable, never silent.
    """

    session_id: str
    comparison: Comparison
    _observations: Dict[str, Observation] = field(default_factory=dict)
    _history: List[Observation] = field(default_factory=list)
    _deleted: bool = False

    def _check_live(self):
        if self._deleted:
            raise DeletedSessionError(f"session {self.session_id} is deleted")

    def record(self, song_id: str, state: ObservationState,
               heard_enough: bool = False, **extensions) -> Observation:
        self._check_live()
        _require_str(song_id, "song_id")
        if song_id not in self.comparison.queue_ids:
            raise ValidationError(f"song not in queue: {song_id!r}")
        current = self._observations.get(song_id)
        if current is not None and current.state in _TERMINAL_STATES:
            raise InvalidTransition(
                f"{song_id} is already {current.state.value}; use correct() "
                "to change a terminal observation explicitly"
            )
        obs = Observation(song_id, state, heard_enough, **extensions)
        self._observations[song_id] = obs
        self._history.append(obs)
        return obs

    def correct(self, song_id: str, state: ObservationState,
                heard_enough: bool = False, **extensions) -> Observation:
        """Explicitly replace an observation. The old value stays in history."""
        self._check_live()
        _require_str(song_id, "song_id")
        if song_id not in self.comparison.queue_ids:
            raise ValidationError(f"song not in queue: {song_id!r}")
        obs = Observation(song_id, state, heard_enough, **extensions)
        self._observations[song_id] = obs
        self._history.append(obs)
        return obs

    def observation_for(self, song_id: str) -> ObservationState:
        self._check_live()
        obs = self._observations.get(song_id)
        return obs.state if obs is not None else ObservationState.UNKNOWN

    def binary_summary(self) -> Dict[str, Dict[str, Optional[float]]]:
        """Keep/pass counts using ONLY condition-unique, heard songs.

        Shared songs are reported separately: they cannot discriminate
        between conditions. MAYBE / NOT_HEARD_ENOUGH / ALREADY_FAMILIAR
        / UNKNOWN are excluded, never counted as negatives. A rate is
        None (not zero) when there is no binary evidence for a condition.
        """
        self._check_live()
        out: Dict[str, Dict[str, Optional[float]]] = {}
        for condition in ("A1", "B-metadata"):
            kept = passed = 0
            for rid in self.comparison.unique_ids(condition):
                state = self.observation_for(rid)
                if state == ObservationState.KEPT_AFTER_LISTENING:
                    kept += 1
                elif state == ObservationState.PASSED_AFTER_LISTENING:
                    passed += 1
            total = kept + passed
            out[condition] = {
                "kept": kept,
                "passed": passed,
                "keep_rate": (kept / total) if total else None,
                "binary_n": total,
            }
        shared_kept = sum(
            1 for rid in self.comparison.shared_ids()
            if self.observation_for(rid) == ObservationState.KEPT_AFTER_LISTENING
        )
        shared_passed = sum(
            1 for rid in self.comparison.shared_ids()
            if self.observation_for(rid) == ObservationState.PASSED_AFTER_LISTENING
        )
        out["shared"] = {
            "kept": shared_kept,
            "passed": shared_passed,
            "keep_rate": None,
            "binary_n": shared_kept + shared_passed,
        }
        return out

    def history(self) -> Tuple[Observation, ...]:
        self._check_live()
        return tuple(self._history)

    def delete(self) -> None:
        """Complete deletion of this session's data and derived state."""
        self._observations.clear()
        self._history.clear()
        self._deleted = True


class Pilot:
    """Container for sessions over one catalog. Owns deletion."""

    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self.sessions: Dict[str, Session] = {}

    def new_session(self, session_id: str, comparison: Comparison) -> Session:
        _require_str(session_id, "session_id")
        if session_id in self.sessions and not self.sessions[session_id]._deleted:
            raise ValidationError(f"session already exists: {session_id}")
        session = Session(session_id=session_id, comparison=comparison)
        self.sessions[session_id] = session
        return session

    def delete_session(self, session_id: str) -> None:
        session = self.sessions.pop(session_id, None)
        if session is not None:
            session.delete()

    def delete_all(self) -> None:
        """Delete every session and its derived state. The synthetic
        catalog itself is not listener data and is retained."""
        for session in list(self.sessions.values()):
            session.delete()
        self.sessions.clear()
