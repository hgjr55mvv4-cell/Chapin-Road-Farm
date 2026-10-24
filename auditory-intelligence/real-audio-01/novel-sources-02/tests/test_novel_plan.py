"""Offline tests for the frozen novel source-ID evaluation plan (no WAVs)."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from novel_source_dev import METHODS, SCHEDULES, GAIN, plan  # noqa: E402


class NovelSourcePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = HERE.parent.parent
        cls.manifest = HERE.parent / "selected_sources.json"
        cls.original = cls.root / "sources.json"
        cls.document, cls.held, cls.groups = plan(cls.manifest, cls.original)

    def test_exact_new_source_counts_and_unique_ids(self):
        originals = json.loads(self.original.read_text())["sources"]
        old_ids = {r["source_id"] for r in originals}
        ids = [r["source_id"] for r in self.document["new_eval_sources"]]
        self.assertEqual(len(ids), 15)
        self.assertEqual(len(set(ids)), 15)
        self.assertFalse(old_ids.intersection(ids))
        self.assertEqual({x: len(v) for x, v in self.held.items()},
                         {"dog": 5, "chainsaw": 5, "rain": 5})

    def test_complete_three_factor_cross(self):
        self.assertEqual(len(self.groups), 125)
        self.assertEqual(len({tuple(g["indices"]) for g in self.groups}), 125)
        for category in ("dog", "chainsaw", "rain"):
            counts = {r["filename"]: 0 for r in self.held[category]}
            for group in self.groups:
                counts[group["filenames"][category]] += 1
            self.assertEqual(set(counts.values()), {25})

    def test_frozen_four_active_schedules_and_one_gain(self):
        self.assertEqual(SCHEDULES, (
            ("dog", "chainsaw"), ("chainsaw", "dog"),
            ("dog", "dog"), ("chainsaw", "chainsaw"),
        ))
        self.assertEqual(GAIN, 0.5)
        self.assertEqual(METHODS, ("energy", "zcr", "multiband"))
        self.assertEqual(len(self.groups) * len(SCHEDULES), 500)

    def test_changed_training_role_rejected(self):
        original = json.loads(self.original.read_text())
        original["sources"][0]["role"] = "eval"
        with tempfile.TemporaryDirectory() as td:
            new_path = Path(td) / "original.json"
            new_path.write_text(json.dumps(original))
            with self.assertRaisesRegex(ValueError, "Training sources changed"):
                plan(self.manifest, new_path)

    def test_selection_manifest_byte_drift_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            modified = Path(td) / "changed.json"
            modified.write_bytes(self.manifest.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "Frozen source selection changed"):
                plan(modified, self.original)


if __name__ == "__main__":
    unittest.main()
