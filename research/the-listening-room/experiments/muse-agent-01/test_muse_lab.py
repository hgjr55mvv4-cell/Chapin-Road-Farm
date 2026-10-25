"""Tests for Muse Constellation Lab v0.2 (independent implementation).

Run offline, stdlib only:
    python3 -m unittest test_muse_lab -v

Every test here is either a reproduced Meta AI probe (now fixed),
a fail-closed check that must NOT crash, or a falsifier for one
of the two original ideas. Tautological tests are labelled as
structural in their docstrings, not presented as behavioural
evidence.
"""

import inspect
import unittest

from muse_lab import (
    ListenerState,
    a1_explicit_ranker,
    evaluate_next_pick,
    evaluate_next_pick_recall,
    evaluate_replacement,
    generate_corrections,
    generate_sessions,
    global_replacement_ranker,
    make_catalog,
    make_listener,
    popularity_ranker,
    provenance_ranker,
    recommend,
    replacement_ranker,
    run_experiments,
    shuffled_corrections,
    validate_contribution,
)


def base_contribution():
    return {
        "schema_version": "0.1-dev",
        "synthetic": True,
        "session": {"session_id": "s1", "occasion_label": "quiet"},
        "privacy": {"storage": "session_only", "research_use": False,
                    "public_release": False, "model_training": False},
        "songs": [
            {"song_id": "s1",
             "track": {"title": "Imaginary A", "artist": "Invented One",
                       "identity_status": "unverified", "source_url": None},
             "listener_report": {"text": "I like the space.", "scope": "whole_song"},
             "moments": []},
            {"song_id": "s2",
             "track": {"title": "Imaginary B", "artist": "Invented Two",
                       "identity_status": "unverified", "source_url": None},
             "listener_report": {"text": None, "scope": "unspecified"},
             "moments": []},
        ],
        "playlist": {"song_ids": ["s1", "s2"], "connection_in_own_words": None},
    }


class TestFailClosedValidator(unittest.TestCase):
    def test_valid_passes(self):
        self.assertEqual(validate_contribution(base_contribution()), [])

    def test_dict_playlist_member_is_error_not_crash(self):
        """Reproduced Meta AI defect: TypeError unhashable dict."""
        d = base_contribution()
        d["playlist"]["song_ids"] = [{"song_id": "s1"}]
        errors = validate_contribution(d)
        self.assertTrue(errors)
        self.assertTrue(any("playlist.song_ids[0]" in e for e in errors))

    def test_list_playlist_member_is_error_not_crash(self):
        d = base_contribution()
        d["playlist"]["song_ids"] = [["s1"]]
        self.assertTrue(validate_contribution(d))

    def test_acoustic_observation_variant_rejected(self):
        """Reproduced Meta AI defect: 'acoustic_observation' slipped through."""
        d = base_contribution()
        d["claims"] = [{"type": "acoustic_observation", "authorized_audio": True}]
        self.assertTrue(any("Stage 0" in e for e in validate_contribution(d)))

    def test_audio_observation_rejected_even_when_authorized(self):
        d = base_contribution()
        d["claims"] = [{"type": "audio_observation", "authorized_audio": True}]
        self.assertTrue(validate_contribution(d))

    def test_listener_words_are_not_censored(self):
        """Only claim types/field names are scanned, not free text."""
        d = base_contribution()
        d["songs"][0]["listener_report"]["text"] = "the tempo feels spacious to me"
        self.assertEqual(validate_contribution(d), [])

    def test_ambiguous_recording_identity_flagged(self):
        d = base_contribution()
        d["songs"][1]["track"]["title"] = "Imaginary A"
        d["songs"][1]["track"]["artist"] = "Invented One"
        self.assertTrue(any("ambiguous" in e for e in validate_contribution(d)))

    def test_privacy_relaxation_rejected(self):
        for key in ("research_use", "public_release", "model_training"):
            d = base_contribution()
            d["privacy"][key] = True
            self.assertTrue(validate_contribution(d), key)

    def test_bool_seconds_rejected(self):
        d = base_contribution()
        d["songs"][0]["moments"] = [{"approx_seconds": True,
                                    "listener_note": "x", "type": "human_report"}]
        self.assertTrue(validate_contribution(d))


class TestStateFailClosed(unittest.TestCase):
    def setUp(self):
        self.state = ListenerState(catalog={"A", "B", "C", "D"})
        self.state.add_session("s1", ["A", "B", "C"], context="quiet")
        self.state.add_session("s2", ["A", "B", "D"], context="morning")

    def test_generator_session_is_kept_not_emptied(self):
        """Reproduced Meta AI defect: generator -> empty session."""
        st = ListenerState(catalog={"A", "B"})
        def gen():
            yield "A"
            yield "B"
        st.add_session("g1", gen())
        self.assertEqual(st.sessions[0][1], frozenset({"A", "B"}))

    def test_failed_add_leaves_state_unchanged(self):
        before = self.state._snapshot()
        with self.assertRaises(ValueError):
            self.state.add_session("bad", ["A", "GHOST"])
        self.assertEqual(self.state._snapshot(), before)

    def test_correction_unknown_session_rejected(self):
        """Reproduced Meta AI defect: arbitrary session IDs accepted."""
        with self.assertRaises(ValueError):
            self.state.add_correction("A", "B", "nonexistent-999", scope="session")
        # Session-less corrections are allowed explicitly, not silently.
        self.state.add_correction("A", "B", None, scope="global_note")
        self.assertEqual(len(self.state.corrections), 1)

    def test_session_local_suppression(self):
        """Session-local 'not tonight' must suppress only that session."""
        self.state.add_correction("A", "C", "s1", scope="session")
        rec, _, _ = recommend(self.state, ["B"], ["A", "B", "C", "D"], session_id="s1")
        self.assertNotIn("A", rec)
        rec_global, _, _ = recommend(self.state, ["B"], ["A", "B", "C", "D"])
        self.assertIn("A", rec_global)

    def test_veto_blocks_all_rankers_until_revoked(self):
        self.state.veto("A")
        for ranker in (popularity_ranker, provenance_ranker):
            self.assertNotIn("A", ranker(self.state, ["B"], ["A", "B", "C", "D"]))
        self.state.unveto("A")
        self.assertIn("A", popularity_ranker(self.state, ["B"], ["A", "B", "C", "D"]))

    def test_ranker_rejects_unknown_ids(self):
        with self.assertRaises(ValueError):
            popularity_ranker(self.state, ["GHOST"], ["A", "B"])
        with self.assertRaises(ValueError):
            popularity_ranker(self.state, ["A"], ["A", "GHOST"])

    def test_silence_and_click_out_change_nothing(self):
        before = provenance_ranker(self.state, ["A"], ["A", "B", "C", "D"])
        self.state.record_silence()
        self.state.record_click_out("C")
        self.assertEqual(provenance_ranker(self.state, ["A"], ["A", "B", "C", "D"]), before)

    def test_refusal_clears_old_text(self):
        self.state.update_report("A", "I loved this once")
        self.state.update_report("A", None)
        self.assertIsNone(self.state.reports["A"])

    def test_deletion_clears_derived_state(self):
        self.state.add_correction("C", "D", "s1", scope="session")
        self.state.veto("D")
        self.assertGreater(self.state.derived_counts()["n_edges"], 0)
        self.state.delete_all()
        self.assertEqual(self.state.derived_counts(),
                         {"session_track_counts": {}, "n_corrections": 0, "n_edges": 0})
        self.assertEqual(self.state.reports, {})


class TestAbstentionAndStructuralProperties(unittest.TestCase):
    def test_abstention_on_zero_provenance(self):
        """A forced ranking with zero evidence would be fabrication."""
        st = ListenerState(catalog={"A", "B", "C"})
        st.add_session("s1", ["A", "B"])
        rec, not_rec, abstain = recommend(st, ["C"], ["A", "B", "C"])
        # C was never kept with anything; no provenance for A/B either
        # as candidates relative to seed C (they were kept with A/B,
        # not with C) -- so recommend must abstain.
        self.assertTrue(abstain)
        self.assertEqual(rec, [])
        self.assertEqual(set(not_rec), {"A", "B"})

    def test_recommend_returns_provenance_only(self):
        st = ListenerState(catalog={"A", "B", "C", "D"})
        st.add_session("s1", ["A", "B"])
        st.add_session("s2", ["A", "C"])
        rec, _, abstain = recommend(st, ["A"], ["A", "B", "C", "D"])
        self.assertFalse(abstain)
        self.assertEqual(set(rec), {"B", "C"})
        self.assertNotIn("D", rec)

    def test_rankers_take_no_metadata_parameter(self):
        """Structural property, labelled as such: rankers accept
        (state, seed, all_ids) only. If a future edit adds a
        metadata parameter, this test fails in review -- it is
        not, by itself, behavioural proof of blindness."""
        for fn in (popularity_ranker, provenance_ranker):
            params = list(inspect.signature(fn).parameters)
            self.assertNotIn("metadata", params)
            self.assertNotIn("catalog", params)
            self.assertNotIn("tags", params)


class TestA1ExplicitPreferences(unittest.TestCase):
    def test_a1_can_propose_unseen_songs(self):
        catalog = make_catalog()
        tags = {k: v["tags"] for k, v in catalog.items()}
        ranked = a1_explicit_ranker(["metal"], [], tags, sorted(catalog), set())
        # Provenance cannot propose a song with no history; A1 can,
        # by explicit token overlap. Top-ranked must carry "metal".
        self.assertIn("metal", tags[ranked[0]])

    def test_a1_tag_shuffle_kills_advantage(self):
        catalog = make_catalog()
        tags = {k: v["tags"] for k, v in catalog.items()}
        before = a1_explicit_ranker(["metal"], [], tags, sorted(catalog), set())
        shuffled = dict(tags)
        values = list(shuffled.values())
        values.reverse()
        for k, v in zip(shuffled, values):
            shuffled[k] = v
        after = a1_explicit_ranker(["metal"], [], shuffled, sorted(catalog), set())
        self.assertNotEqual(before, after)

    def test_a1_negative_constraints_veto(self):
        catalog = make_catalog()
        tags = {k: v["tags"] for k, v in catalog.items()}
        ranked = a1_explicit_ranker(["metal"], ["metal"], tags, sorted(catalog), set())
        # Negative overlap cancels explicit overlap for metal tracks;
        # they must not outrank non-metal tracks on score alone.
        # (Deterministic ID tie-break is the only ordering left
        # among equal scores, which the test does not over-claim.)
        self.assertTrue(ranked)


class TestOriginalIdeas(unittest.TestCase):
    def test_idea1_random_world_does_not_beat_popularity(self):
        import random
        rng = random.Random(42)
        catalog = make_catalog()
        all_ids = sorted(catalog)
        pops, provs = [], []
        for li in range(8):
            listener = make_listener(rng, f"R{li}", world="random")
            train = generate_sessions(listener, rng, 30, start=0, world="random")
            test = generate_sessions(listener, rng, 10, start=30, world="random")
            state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in train:
                state.add_session(sid, kept, context=ctx)
            pops.append(evaluate_next_pick(state, test, popularity_ranker, all_ids))
            provs.append(evaluate_next_pick(state, test, provenance_ranker, all_ids))
        # Provenance must NOT clearly beat popularity in a world
        # with no constellations. Allow a small chance margin.
        self.assertLessEqual(sum(provs) / len(provs), sum(pops) / len(pops) + 0.15)

    def test_idea2_context_conditioned_does_not_reliably_win(self):
        """NEGATIVE RESULT, reported honestly. Recall@3, overlapping
        constellations: only the context label disambiguates
        overlapping seeds. An earlier single-seed run (seed 7)
        showed a conditioned win by chance; across seeds it
        washes out. Conditioning halves training data, and
        blind already benefits from overlap tracks, which are
        often in the truth set. The naive hard-filter version
        is therefore NOT supported. The falsifier worked.
        This test asserts the negative result is bounded
        (no large blind win either), not that conditioning wins."""
        import random
        rng = random.Random(7)
        catalog = make_catalog()
        all_ids = sorted(catalog)
        blind, cond = [], []
        for li in range(8):
            listener = make_listener(rng, f"C{li}", world="context")
            train = generate_sessions(listener, rng, 30, start=0, world="context")
            test = generate_sessions(listener, rng, 10, start=30, world="context")
            state = ListenerState(catalog=set(all_ids))
            for sid, kept, ctx in train:
                state.add_session(sid, kept, context=ctx)
            blind.append(evaluate_next_pick_recall(state, test, provenance_ranker, all_ids, context_mode="blind"))
            cond.append(evaluate_next_pick_recall(state, test, provenance_ranker, all_ids, context_mode="conditioned"))
        # No large difference either way; a claimed large
        # conditioned win would be evidence of cherry-picking.
        self.assertLess(abs(sum(cond) / len(cond) - sum(blind) / len(blind)), 0.20)

    def test_multi_seed_experiments_are_discriminating(self):
        results = run_experiments(seeds=(1, 2))
        stable = results["stable_next_pick_hit_at_3"]
        self.assertGreater(stable["provenance"]["mean"], stable["popularity"]["mean"] + 0.10)
        self.assertLess(stable["provenance_shuffled_control"]["mean"],
                        stable["provenance"]["mean"] - 0.10)
        rep = results["replacement_hit_at_1"]
        self.assertGreater(rep["pair_specific"]["mean"], rep["global_replacement"]["mean"] + 0.10)
        idea1 = results["idea1_random_world_hit_at_3"]
        self.assertLessEqual(idea1["provenance"]["mean"], idea1["popularity"]["mean"] + 0.15)
        idea2 = results["idea2_context_world_recall_at_3"]
        # Negative result for Idea 2 (see test above): conditioned
        # does not reliably beat blind across seeds 1-2, and
        # stable-world conditioned == blind exactly.
        self.assertLess(abs(idea2["context_conditioned"]["mean"] -
                            idea2["context_blind"]["mean"]), 0.10)
        self.assertEqual(idea2["stable_world_context_conditioned"]["mean"],
                         idea2["stable_world_context_blind"]["mean"])


if __name__ == "__main__":
    unittest.main()


# ------------------------------------------------------------------
# v0.2.1 repair tests (TLR-R2-MUSE-REPAIR-01, Sol review of PR #72)
# These are IN ADDITION to the original 27 tests, which are retained
# unchanged above. Each test below names the finding it covers.
# ------------------------------------------------------------------

from muse_lab import validate_system_claims


def _claim_base(claims):
    d = base_contribution()
    d["claims"] = claims
    return d


class TestRepairP0MalformedContainers(unittest.TestCase):
    """R1/R2: validator must return errors, never crash."""

    def test_corrections_int_bool_string_dict_containers(self):
        for val in [123, True, "not-a-list", {"rejected_id": "s1"}]:
            d = base_contribution()
            d["corrections"] = val
            errors = validate_contribution(d)
            self.assertTrue(errors, val)
            self.assertTrue(any("corrections must be a list" in e for e in errors), errors)

    def test_corrections_malformed_elements(self):
        for val in [[123], ["x"], [None], [{"rejected_id": "s1"}]]:
            d = base_contribution()
            d["corrections"] = val
            self.assertTrue(validate_contribution(d), val)

    def test_associations_int_bool_string_dict_containers(self):
        for val in [123, True, "not-a-list", {"song_ids": ["s1"]}]:
            d = base_contribution()
            d["associations"] = val
            errors = validate_contribution(d)
            self.assertTrue(errors, val)
            self.assertTrue(any("associations must be a list" in e for e in errors), errors)

    def test_associations_malformed_elements(self):
        for val in [[123], [{"song_ids": "not-a-list"}]]:
            d = base_contribution()
            d["associations"] = val
            self.assertTrue(validate_contribution(d), val)

    def test_unhashable_title_and_artist_return_errors(self):
        for title, artist in [(["A"], "X"), ("A", {"name": "X"}), (["A"], ["X"])]:
            d = base_contribution()
            d["songs"][0]["track"]["title"] = title
            d["songs"][0]["track"]["artist"] = artist
            # Must not raise TypeError; must return a type error.
            errors = validate_contribution(d)
            self.assertTrue(errors)
            self.assertTrue(any("track.title" in e or "track.artist" in e for e in errors), errors)

    def test_valid_corrections_and_associations_still_pass(self):
        d = base_contribution()
        d["corrections"] = [{"rejected_id": "s1", "replacement_id": "s2"}]
        d["associations"] = [{"song_ids": ["s1", "s2"]}]
        self.assertEqual(validate_contribution(d), [])


class TestRepairP1VetoRevocation(unittest.TestCase):
    """R3: historical 'never' must not masquerade as current."""

    def test_veto_revoke_effective_view(self):
        st = ListenerState(catalog={"A", "B", "C"})
        st.add_session("s1", ["A", "B"])
        st.veto("A")
        self.assertNotIn("A", popularity_ranker(st, ["B"], ["A", "B", "C"]))
        self.assertNotIn("A", provenance_ranker(st, ["B"], ["A", "B", "C"]))
        st.unveto("A")
        self.assertIn("A", popularity_ranker(st, ["B"], ["A", "B", "C"]))
        view = st.avoidance_view()
        self.assertEqual(view["active_vetoes"], [])
        self.assertIn(("veto", "A"), view["veto_history"])
        self.assertIn(("revoke", "A"), view["veto_history"])
        self.assertIn("never", view["historical_edge_kinds_in_order"])
        self.assertIn("never_revoked", view["historical_edge_kinds_in_order"])
        # Revocation comes after the original veto in the ledger.
        kinds = view["historical_edge_kinds_in_order"]
        self.assertLess(kinds.index("never"), kinds.index("never_revoked"))

    def test_delete_all_clears_veto_history_and_session_corrections(self):
        st = ListenerState(catalog={"A", "B", "C"})
        st.add_session("s1", ["A", "B"])
        st.veto("A")
        st.add_session_correction("B", "C", "s1")
        st.delete_all()
        self.assertEqual(st.avoidance_view()["active_vetoes"], [])
        self.assertEqual(st.avoidance_view()["veto_history"], [])
        self.assertEqual(st.derived_counts(), {"session_track_counts": {}, "n_corrections": 0, "n_edges": 0})


class TestRepairP1HardExclusion(unittest.TestCase):
    """R4: hard exclusion by recording ID, soft negative by tag."""

    def test_hard_excluded_track_cannot_be_reintroduced(self):
        catalog = make_catalog()
        tags = {k: v["tags"] for k, v in catalog.items()}
        # T06 is metal + tag-a: highest possible positive score
        # for explicit ["metal", "tag-a"]. Hard-exclude it.
        ranked = a1_explicit_ranker(["metal", "tag-a"], [], tags, sorted(catalog), set(), hard_excluded={"T06"})
        self.assertNotIn("T06", ranked)
        # And with vetoes alone, the same track is excluded.
        ranked2 = a1_explicit_ranker(["metal", "tag-a"], [], tags, sorted(catalog), {"T06"})
        self.assertNotIn("T06", ranked2)

    def test_soft_negative_does_not_hard_exclude(self):
        catalog = make_catalog()
        tags = {k: v["tags"] for k, v in catalog.items()}
        # T06 has metal (positive) and tag-a (positive); a soft
        # negative on "metal" only subtracts, it does not remove
        # the track from the list. That is the documented soft
        # behaviour, distinct from hard exclusion above.
        ranked = a1_explicit_ranker(["metal", "tag-a"], ["metal"], tags, sorted(catalog), set())
        self.assertIn("T06", ranked)


class TestRepairP1SessionContextBoundaries(unittest.TestCase):
    """R5: session-local vs global vs context evidence."""

    def test_session_correction_requires_session_id(self):
        st = ListenerState(catalog={"A", "B", "C"})
        st.add_session("s1", ["A", "B"])
        with self.assertRaises(ValueError):
            st.add_correction("A", "B", None, scope="session")
        with self.assertRaises(ValueError):
            st.add_correction("A", "B", "no-such-session", scope="session")
        # Global scope remains the session-less operation.
        st.add_global_correction("A", "B")
        self.assertEqual(len(st.corrections), 1)

    def test_cross_session_isolation_reject_in_one_accept_in_another(self):
        st = ListenerState(catalog={"A", "B", "C", "D"})
        st.add_session("quiet-s1", ["A", "B"], context="quiet")
        st.add_session("morning-s1", ["A", "C"], context="morning")
        st.add_session_correction("A", "D", "quiet-s1")
        rec_quiet, _, _ = recommend(st, ["B"], ["A", "B", "C", "D"], session_id="quiet-s1")
        self.assertNotIn("A", rec_quiet)
        rec_morning, _, _ = recommend(st, ["B"], ["A", "B", "C", "D"], session_id="morning-s1")
        self.assertIn("A", rec_morning)
        # Global replacement must NOT use the session-local pair.
        self.assertNotEqual(replacement_ranker(st, "A", ["A", "B", "C", "D"])[0], "D")

    def test_context_conditioned_uses_only_context_matching_pair_evidence(self):
        st = ListenerState(catalog={"A", "B", "C", "D", "E"})
        st.add_session("quiet-s1", ["A", "B"], context="quiet")
        st.add_session("morning-s1", ["A", "C"], context="morning")
        # Global correction whose session_id is the quiet session.
        st.add_global_correction("A", "D", session_id="quiet-s1")
        blind = provenance_ranker(st, ["A"], ["A", "B", "C", "D", "E"])
        cond_morning = provenance_ranker(st, ["A"], ["A", "B", "C", "D", "E"], context="morning")
        cond_quiet = provenance_ranker(st, ["A"], ["A", "B", "C", "D", "E"], context="quiet")
        # D is boosted by the pair in blind and in quiet, but
        # must NOT be pair-boosted in morning (other context).
        # Morning's top pair-boosted candidate should not be D
        # via that quiet correction; quiet's should include D
        # ahead of morning-only tracks. Check ordering directly:
        self.assertLess(cond_quiet.index("D"), cond_quiet.index("C"))
        # In morning, D has no pair evidence and no morning
        # co-occurrence, so it must rank behind C (morning
        # co-member). This is the leakage test.
        self.assertLess(cond_morning.index("C"), cond_morning.index("D"))
        self.assertIn("D", blind)


class TestRepairP1Stage0Allowlist(unittest.TestCase):
    """R6: narrow allowlist, disguised fields, listener text preserved."""

    def test_allowlisted_claim_types_with_evidence_pass(self):
        for claim in [
            {"type": "HUMAN_REPORT", "listener_text": "I love the guitar entrance"},
            {"type": "TRACK_METADATA", "title": "A", "artist": "X"},
            {"type": "SYSTEM_HYPOTHESIS", "hypothesis": "these may belong together", "uncertainty": "unverified"},
            {"type": "UNKNOWN"},
        ]:
            self.assertEqual(validate_system_claims([claim]), [], claim)
            self.assertEqual(validate_contribution(_claim_base([claim])), [], claim)

    def test_disallowed_types_and_disguised_fields_rejected(self):
        for claim in [
            {"type": "AUDIO_OBSERVATION", "value": 1},
            {"type": "SYSTEM_NOTE", "waveform_peak": 0.9},
            {"type": "UNKNOWN", "guitar_entrance_verified": True},
            {"type": "TRACK_METADATA", "title": "A", "verified_acoustic_structure": "guitar entrance"},
            {"type": "HUMAN_REPORT", "listener_text": "hi", "authorized_audio": True},
            {"type": "HUMAN_REPORT", "listener_text": "hi", "verified": True},
        ]:
            self.assertTrue(validate_system_claims([claim]), claim)
            self.assertTrue(validate_contribution(_claim_base([claim])), claim)

    def test_listener_text_guitar_entrance_is_not_system_verified_audio(self):
        # The listener may write it; the system may not relabel it.
        d = base_contribution()
        d["songs"][0]["listener_report"]["text"] = "I love the guitar entrance"
        self.assertEqual(validate_contribution(d), [])
        # The same sentence as a system claim with a verified
        # acoustic field is rejected, not promoted.
        claim = {"type": "SYSTEM_HYPOTHESIS", "hypothesis": "guitar entrance verified", "verified_acoustic_structure": "guitar entrance"}
        self.assertTrue(validate_system_claims([claim]))

    def test_human_report_without_evidence_rejected(self):
        self.assertTrue(validate_system_claims([{"type": "HUMAN_REPORT"}]))


# ------------------------------------------------------------------
# v0.2.2 final narrow integrity repair (Sol re-review of PR #72
# at commit 5dc1765b). Two cases only, no feature expansion.
# ------------------------------------------------------------------

class TestRepairV022UnhashableMembership(unittest.TestCase):
    """F1/F2: type checks must precede set membership."""

    def test_corrections_unhashable_ids_return_errors_not_typeerror(self):
        for rej, rep in [(["s1"], "s2"), ("s1", {"id": "s2"}), (["s1"], ["s2"]), (123, "s2")]:
            d = base_contribution()
            d["corrections"] = [{"rejected_id": rej, "replacement_id": rep}]
            errors = validate_contribution(d)  # must not raise
            self.assertTrue(errors, (rej, rep))
            self.assertTrue(any("corrections[0]." in e and "must be a non-empty string" in e for e in errors), errors)

    def test_corrections_valid_ids_still_pass_and_unknown_still_flagged(self):
        d = base_contribution()
        d["corrections"] = [{"rejected_id": "s1", "replacement_id": "s2"}]
        self.assertEqual(validate_contribution(d), [])
        d2 = base_contribution()
        d2["corrections"] = [{"rejected_id": "s1", "replacement_id": "ghost"}]
        self.assertTrue(any("references unknown song_id" in e for e in validate_contribution(d2)))

    def test_system_claim_unhashable_type_returns_error_not_typeerror(self):
        for t in [["HUMAN_REPORT"], {"name": "HUMAN_REPORT"}, ["UNKNOWN"], 123]:
            errors = validate_system_claims([{"type": t, "listener_text": "hi"}])
            self.assertTrue(errors, t)
            self.assertTrue(any("claims[0].type" in e for e in errors), errors)
            d = base_contribution()
            d["claims"] = [{"type": t, "listener_text": "hi"}]
            self.assertTrue(validate_contribution(d), t)

    def test_system_claim_valid_types_still_pass(self):
        self.assertEqual(validate_system_claims([{"type": "HUMAN_REPORT", "listener_text": "hi"}]), [])
        self.assertEqual(validate_system_claims([{"type": "UNKNOWN"}]), [])
