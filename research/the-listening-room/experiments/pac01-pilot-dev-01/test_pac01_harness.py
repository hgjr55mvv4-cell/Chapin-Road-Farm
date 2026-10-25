"""Adversarial deterministic tests for pac01_harness.

Each test exercises actual source behaviour, not a mock of it.
Run:  python3 -m unittest test_pac01_harness -v
"""

import unittest

from pac01_harness import (
    Catalog, Comparison, DeletedSessionError, InsufficientBalance,
    InvalidTransition, Observation, ObservationState, Pilot,
    Ranking, SnapshotMismatch, SyntheticRecording, ValidationError,
    build_catalog, build_comparison, build_ranking, demo_catalog,
    mock_a1_ranking, mock_b_ranking,
)

A1 = "A1"
B = "B-metadata"


def small_catalog():
    return build_catalog("snap-1", [
        {"recording_id": "X1", "artist": "Alpha", "title": "One",
         "release_category": "single", "genre_tags": ["folk"],
         "key": "C major", "tempo_bpm": 100},
        {"recording_id": "X2", "artist": "Alpha", "title": "Two",
         "release_category": "single", "genre_tags": ["folk"],
         "key": "G major", "tempo_bpm": 90},
        {"recording_id": "X3", "artist": "Beta", "title": "Three",
         "release_category": "single", "genre_tags": ["pop"],
         "key": "D minor", "tempo_bpm": 120},
        {"recording_id": "X4", "artist": "Gamma", "title": "Four",
         "release_category": "single", "genre_tags": ["pop"],
         "key": "C major", "tempo_bpm": 100},
        {"recording_id": "X5", "artist": "Delta", "title": "Five",
         "release_category": "single", "genre_tags": ["folk"],
         "key": "A minor", "tempo_bpm": 80},
        {"recording_id": "X6", "artist": "Epsilon", "title": "Six",
         "release_category": "single", "genre_tags": ["rock"],
         "key": "E major", "tempo_bpm": 130},
    ])


def ranking(condition, ids, snapshot="snap-1"):
    return build_ranking(condition, ids, snapshot, "ctx",
                         ["folk"], "v1", "test")


class TestCatalogValidation(unittest.TestCase):
    def test_duplicate_recording_ids_rejected(self):
        with self.assertRaises(ValidationError):
            build_catalog("s", [
                {"recording_id": "D", "artist": "A", "title": "t",
                 "release_category": "single"},
                {"recording_id": "D", "artist": "B", "title": "u",
                 "release_category": "single"},
            ])

    def test_missing_field_rejected(self):
        with self.assertRaises(ValidationError):
            build_catalog("s", [{"artist": "A", "title": "t",
                                 "release_category": "single"}])

    def test_unknown_field_rejected(self):
        with self.assertRaises(ValidationError):
            build_catalog("s", [{"recording_id": "D", "artist": "A",
                                 "title": "t", "release_category": "single",
                                 "real_audio_path": "/tmp/x.mp3"}])

    def test_bad_tempo_rejected(self):
        with self.assertRaises(ValidationError):
            build_catalog("s", [{"recording_id": "D", "artist": "A",
                                 "title": "t", "release_category": "single",
                                 "tempo_bpm": -5}])

    def test_non_string_id_rejected(self):
        with self.assertRaises(ValidationError):
            build_catalog("s", [{"recording_id": 123, "artist": "A",
                                 "title": "t", "release_category": "single"}])

    def test_empty_catalog_rejected(self):
        with self.assertRaises(ValidationError):
            build_catalog("s", [])


class TestRankings(unittest.TestCase):
    def test_ranking_duplicates_rejected(self):
        with self.assertRaises(ValidationError):
            ranking(A1, ["X1", "X1"])

    def test_ranking_unknown_id_rejected_at_comparison(self):
        cat = small_catalog()
        with self.assertRaises(ValidationError):
            build_comparison(cat, ranking(A1, ["X1", "ZZ"]),
                             ranking(B, ["X1", "X3"]), seed=1)

    def test_ranking_freeze_ignores_later_list_mutation(self):
        ids = ["X1", "X3", "X4"]
        r = build_ranking(A1, ids, "snap-1", "ctx", ["folk"], "v1", "p")
        ids.append("X5")
        ids[0] = "X6"
        self.assertEqual(r.ranked_ids, ("X1", "X3", "X4"))

    def test_unequal_snapshots_rejected(self):
        cat = small_catalog()
        with self.assertRaises(SnapshotMismatch):
            build_comparison(cat, ranking(A1, ["X1", "X3"]),
                             ranking(B, ["X1", "X3"], snapshot="other"), seed=1)

    def test_mock_rankers_share_snapshot_and_differ(self):
        cat = demo_catalog()
        a = mock_a1_ranking(cat, ["synthetic folk"])
        b = mock_b_ranking(cat, ["synthetic folk"])
        self.assertEqual(a.catalog_snapshot_id, b.catalog_snapshot_id)
        self.assertEqual(a.preferences, b.preferences)
        self.assertNotEqual(a.ranked_ids, b.ranked_ids)
        self.assertEqual(a.provenance != b.provenance, True)


class TestComparison(unittest.TestCase):
    def test_shared_song_appears_once_with_both_provenances(self):
        cat = small_catalog()
        comp = build_comparison(
            cat, ranking(A1, ["X1", "X2", "X3"]),
            ranking(B, ["X1", "X4", "X5"]), seed=7)
        self.assertEqual(comp.queue_ids.count("X1"), 1)
        self.assertEqual(comp.provenance_for("X1"), (A1, B))
        self.assertEqual(comp.shared_ids(), ("X1",))
        # Balanced pairs: X2 (A-only) with X4 (B-only); X3/X5 unpaired
        # (zip stops) and reported as remainder, not substituted.
        self.assertIn("X2", comp.queue_ids)
        self.assertIn("X4", comp.queue_ids)

    def test_artist_cap_applied_consistently(self):
        cat = small_catalog()
        # A1 ranking is dominated by Alpha (X1, X2); cap 1 must hold.
        comp = build_comparison(
            cat, ranking(A1, ["X1", "X2", "X3"]),
            ranking(B, ["X4", "X5", "X6"]), seed=3, max_per_artist=1)
        artists = [cat.recordings[r].artist for r in comp.queue_ids]
        for artist in set(artists):
            self.assertLessEqual(artists.count(artist), 1)

    def test_identical_rankings_insufficient_balance(self):
        cat = small_catalog()
        with self.assertRaises(InsufficientBalance):
            build_comparison(cat, ranking(A1, ["X1", "X3"]),
                             ranking(B, ["X1", "X3"]), seed=1)

    def test_one_sided_uniques_insufficient_balance(self):
        cat = small_catalog()
        # B ranking is a subset of A ranking: B has no unique song.
        with self.assertRaises(InsufficientBalance):
            build_comparison(cat, ranking(A1, ["X1", "X3", "X4"]),
                             ranking(B, ["X1", "X3"]), seed=1)

    def test_cap_can_force_insufficient_balance(self):
        cat = small_catalog()
        # Shared X1 (Alpha) consumes the per-artist cap of 1, so the
        # only A-only song X2 (also Alpha) cannot be paired with the
        # only B-only song X4 -- no balanced pair survives, and the
        # harness refuses instead of adding X4 alone.
        with self.assertRaises(InsufficientBalance):
            build_comparison(
                cat, ranking(A1, ["X1", "X2"]),
                ranking(B, ["X1", "X4"]), seed=1, max_per_artist=1)

    def test_listener_view_hides_condition_assignment(self):
        cat = small_catalog()
        comp = build_comparison(
            cat, ranking(A1, ["X1", "X2", "X3"]),
            ranking(B, ["X1", "X4", "X5"]), seed=7)
        view = comp.listener_view()
        self.assertEqual(set(view), set(comp.queue_ids))
        self.assertNotIn(A1, view)
        self.assertNotIn(B, view)

    def test_identical_replay_same_seed_and_inputs(self):
        cat = small_catalog()
        args = (cat, ranking(A1, ["X1", "X2", "X3"]),
                ranking(B, ["X1", "X4", "X5"]))
        c1 = build_comparison(*args, seed=42)
        c2 = build_comparison(*args, seed=42)
        self.assertEqual(c1.queue_ids, c2.queue_ids)
        self.assertEqual(c1.presentation_order, c2.presentation_order)
        self.assertEqual(c1.listener_view(), c2.listener_view())

    def test_different_seed_may_reorder_but_not_change_queue(self):
        cat = small_catalog()
        args = (cat, ranking(A1, ["X1", "X2", "X3"]),
                ranking(B, ["X1", "X4", "X5"]))
        c1 = build_comparison(*args, seed=1)
        c2 = build_comparison(*args, seed=99)
        self.assertEqual(set(c1.queue_ids), set(c2.queue_ids))
        self.assertEqual(set(c1.presentation_order), set(c2.presentation_order))

    def test_demo_catalog_builds_balanced_comparison(self):
        cat = demo_catalog()
        comp = build_comparison(
            cat, mock_a1_ranking(cat, ["synthetic folk"]),
            mock_b_ranking(cat, ["synthetic folk"]), seed=11)
        self.assertGreaterEqual(len(comp.unique_ids(A1)), 1)
        self.assertGreaterEqual(len(comp.unique_ids(B)), 1)
        self.assertEqual(len(comp.unique_ids(A1)), len(comp.unique_ids(B)))


class TestObservations(unittest.TestCase):
    def setUp(self):
        cat = small_catalog()
        comp = build_comparison(
            cat, ranking(A1, ["X1", "X2", "X3"]),
            ranking(B, ["X1", "X4", "X5"]), seed=7)
        self.pilot = Pilot(cat)
        self.session = self.pilot.new_session("s1", comp)
        # Queue: X1 (shared), X2 (A-only), X4 (B-only).

    def test_queue_membership_is_not_hearing(self):
        self.assertEqual(
            self.session.observation_for("X2"), ObservationState.UNKNOWN)
        self.assertEqual(self.session.binary_summary()[A1]["binary_n"], 0)

    def test_keep_without_heard_enough_rejected(self):
        with self.assertRaises(ValidationError):
            self.session.record(
                "X2", ObservationState.KEPT_AFTER_LISTENING, heard_enough=False)

    def test_pass_without_heard_enough_rejected(self):
        with self.assertRaises(ValidationError):
            self.session.record(
                "X2", ObservationState.PASSED_AFTER_LISTENING, heard_enough=False)

    def test_unheard_maybe_unknown_excluded_from_binary(self):
        self.session.record("X2", ObservationState.NOT_HEARD_ENOUGH)
        self.session.record("X4", ObservationState.MAYBE)
        summary = self.session.binary_summary()
        self.assertEqual(summary[A1]["binary_n"], 0)
        self.assertEqual(summary[B]["binary_n"], 0)

    def test_familiar_excluded_from_binary(self):
        self.session.record("X2", ObservationState.ALREADY_FAMILIAR)
        summary = self.session.binary_summary()
        self.assertEqual(summary[A1]["binary_n"], 0)
        self.assertIsNone(summary[A1]["keep_rate"])

    def test_shared_songs_do_not_drive_condition_rates(self):
        self.session.record("X1", ObservationState.KEPT_AFTER_LISTENING,
                            heard_enough=True)
        summary = self.session.binary_summary()
        self.assertEqual(summary[A1]["binary_n"], 0)
        self.assertEqual(summary[B]["binary_n"], 0)
        self.assertEqual(summary["shared"]["kept"], 1)

    def test_binary_counts_only_unique_heard(self):
        self.session.record("X2", ObservationState.KEPT_AFTER_LISTENING,
                            heard_enough=True)
        self.session.record("X4", ObservationState.PASSED_AFTER_LISTENING,
                            heard_enough=True)
        summary = self.session.binary_summary()
        self.assertEqual(summary[A1], {"kept": 1, "passed": 0,
                                       "keep_rate": 1.0, "binary_n": 1})
        self.assertEqual(summary[B], {"kept": 0, "passed": 1,
                                      "keep_rate": 0.0, "binary_n": 1})

    def test_invalid_transition_after_keep(self):
        self.session.record("X2", ObservationState.KEPT_AFTER_LISTENING,
                            heard_enough=True)
        with self.assertRaises(InvalidTransition):
            self.session.record("X2", ObservationState.PASSED_AFTER_LISTENING,
                                heard_enough=True)

    def test_invalid_transition_after_familiar(self):
        self.session.record("X2", ObservationState.ALREADY_FAMILIAR)
        with self.assertRaises(InvalidTransition):
            self.session.record("X2", ObservationState.KEPT_AFTER_LISTENING,
                                heard_enough=True)

    def test_explicit_correction_allowed_and_audited(self):
        self.session.record("X2", ObservationState.KEPT_AFTER_LISTENING,
                            heard_enough=True)
        self.session.correct("X2", ObservationState.PASSED_AFTER_LISTENING,
                             heard_enough=True)
        self.assertEqual(self.session.observation_for("X2"),
                         ObservationState.PASSED_AFTER_LISTENING)
        self.assertEqual(len(self.session.history()), 2)

    def test_observation_outside_queue_rejected(self):
        with self.assertRaises(ValidationError):
            self.session.record("X6", ObservationState.MAYBE)

    def test_unknown_state_rejected(self):
        with self.assertRaises(ValidationError):
            Observation("X2", "LOVED_IT")  # type: ignore[arg-type]

    def test_extension_fields_stored_not_scored(self):
        self.session.record(
            "X2", ObservationState.KEPT_AFTER_LISTENING, heard_enough=True,
            passage_note="bridge", replay_desire=True,
            free_text_reason="listener's own words",
            preference_change="liked more on second hearing")
        obs = self.session._observations["X2"]
        self.assertEqual(obs.passage_note, "bridge")
        self.assertTrue(obs.replay_desire)
        # No score is derived from extension fields: binary math is
        # still exactly one kept song for A1.
        self.assertEqual(self.session.binary_summary()[A1]["kept"], 1)

    def test_outcomes_do_not_leak_into_frozen_rankings(self):
        self.session.record("X2", ObservationState.KEPT_AFTER_LISTENING,
                            heard_enough=True)
        cat = small_catalog()
        comp2 = build_comparison(
            cat, ranking(A1, ["X1", "X2", "X3"]),
            ranking(B, ["X1", "X4", "X5"]), seed=7)
        self.assertEqual(comp2.queue_ids, self.session.comparison.queue_ids)
        self.assertEqual(comp2.presentation_order,
                         self.session.comparison.presentation_order)
        self.assertEqual(comp2.ranking_a, self.session.comparison.ranking_a)


class TestDeletion(unittest.TestCase):
    def test_delete_session_removes_data_and_blocks_use(self):
        cat = small_catalog()
        comp = build_comparison(
            cat, ranking(A1, ["X1", "X2", "X3"]),
            ranking(B, ["X1", "X4", "X5"]), seed=7)
        pilot = Pilot(cat)
        session = pilot.new_session("s1", comp)
        session.record("X2", ObservationState.KEPT_AFTER_LISTENING,
                       heard_enough=True)
        pilot.delete_session("s1")
        self.assertNotIn("s1", pilot.sessions)
        with self.assertRaises(DeletedSessionError):
            session.record("X4", ObservationState.MAYBE)
        with self.assertRaises(DeletedSessionError):
            session.binary_summary()

    def test_delete_all_clears_sessions_but_not_catalog(self):
        cat = demo_catalog()
        pilot = Pilot(cat)
        comp = build_comparison(
            cat, mock_a1_ranking(cat, ["synthetic folk"]),
            mock_b_ranking(cat, ["synthetic folk"]), seed=11)
        pilot.new_session("s1", comp)
        pilot.new_session("s2", comp)
        pilot.delete_all()
        self.assertEqual(pilot.sessions, {})
        self.assertEqual(len(pilot.catalog), 12)


if __name__ == "__main__":
    unittest.main()
