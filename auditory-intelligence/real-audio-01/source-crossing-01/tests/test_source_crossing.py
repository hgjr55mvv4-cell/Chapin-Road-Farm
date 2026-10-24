"""Offline tests for the exposed eight-configuration crossing plan."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from source_crossing_dev import GAINS, SCHEDULES, plan_sources


class CrossedSourcePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((HERE.parent.parent / "sources.json").read_text())

    def test_exact_eight_crosses_and_six_source_recordings(self):
        held, groups = plan_sources(self.manifest)
        self.assertEqual(len(groups), 8)
        self.assertEqual(len(SCHEDULES) * len(GAINS) * len(groups), 192)
        self.assertEqual({tuple(g["cross_index"]) for g in groups},
                         {(d, c, r) for d in range(2) for c in range(2) for r in range(2)})
        self.assertEqual(sum(len(x) for x in held.values()), 6)

    def test_diagonal_matches_original_fold_pairing(self):
        _, groups = plan_sources(self.manifest)
        pairs = [g for g in groups if len(set(g["cross_index"])) == 1]
        self.assertEqual(len(pairs), 2)
        self.assertEqual(sorted(tuple(g["cross_index"]) for g in pairs),
                         [(0, 0, 0), (1, 1, 1)])

    def test_reused_source_id_rejected_even_across_categories(self):
        changed = copy.deepcopy(self.manifest)
        changed["sources"][-1]["source_id"] = changed["sources"][0]["source_id"]
        with self.assertRaisesRegex(ValueError, "Source identity reused"):
            plan_sources(changed)

    def test_changed_fold_pairing_rejected(self):
        changed = copy.deepcopy(self.manifest)
        row = next(r for r in changed["sources"] if r["role"] == "eval" and r["category"] == "dog")
        row["filename"] = "4-" + row["filename"][2:]
        with self.assertRaisesRegex(ValueError, "Evaluation fold order"):
            plan_sources(changed)


if __name__ == "__main__":
    unittest.main()
