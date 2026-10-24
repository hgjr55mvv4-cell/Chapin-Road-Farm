"""Offline controls for training-excerpt ablation. No WAV download."""
from __future__ import annotations

import json
from pathlib import Path
import random
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from training_excerpt_dev import (  # noqa: E402
    FROZEN_CONTRACT_SHA256, frozen_inputs, normalized_fixed_window,
)


class TrainingExcerptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = HERE.parent / "frozen_contract.json"
        cls.ci = ROOT / "novel-sources-02" / "receipts" / "ci_source_summary_2026-10-24.json"
        cls.original = ROOT / "sources.json"
        cls.expanded = ROOT / "novel-sources-02" / "selected_sources.json"
        cls.document, cls.receipt, cls.source = frozen_inputs(
            cls.contract, cls.ci, cls.original, cls.expanded)

    def test_parent_checksums_and_version_frozen(self):
        self.assertEqual(len(FROZEN_CONTRACT_SHA256), 64)
        self.assertEqual(self.document["version"], "v0.1-frozen-before-execution")
        self.assertEqual(len(self.source["new_eval_sources"]), 15)
        self.assertEqual(self.receipt["workflow_conclusion"], "success")

    def test_offsets_are_precomputed_from_fixed_seed(self):
        offsets = self.document["training_offsets_seconds"]
        for sid in self.document["frozen_conditions"]["training_source_ids"]:
            expected = [round(x * .25, 2) for x in
                        random.Random(20261024 + int(sid)).sample(range(17), 3)]
            self.assertEqual(offsets[sid], expected)
            self.assertEqual(len(set(offsets[sid])), 3)
            self.assertTrue(all(0 <= x <= 4 for x in offsets[sid]))

    def test_fixed_window_normalizes_without_extra_selection(self):
        # 5s synthetic signal is used only to unit-test the excerpt wrapper.
        samples = [.20] * 40000
        segment, metrics = normalized_fixed_window(samples, 1.25)
        self.assertEqual(len(segment), 6400)
        self.assertAlmostEqual(max(segment), .8, places=7)
        self.assertEqual(metrics["offset_s"], 1.25)

    def test_low_energy_and_out_of_bounds_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "too quiet"):
            normalized_fixed_window([0.] * 40000, .5)
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            normalized_fixed_window([.2] * 40000, 4.5)

    def test_mutated_contract_has_new_version_requirement(self):
        with tempfile.TemporaryDirectory() as td:
            altered = Path(td) / "changed.json"
            altered.write_bytes(self.contract.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "contract changed"):
                frozen_inputs(altered, self.ci, self.original, self.expanded)


if __name__ == "__main__":
    unittest.main()
