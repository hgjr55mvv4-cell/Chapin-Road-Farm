"""Regression: receipt verification must reject corruption even under python -O."""
import io
import json
import types
import unittest
from pathlib import Path


class ReceiptGateTests(unittest.TestCase):
    def test_optimized_python_still_rejects_corrupted_receipt(self):
        verifier = Path(__file__).resolve().parents[1] / "verify_receipts.py"
        module = types.ModuleType("verify_receipts_optimized")
        exec(compile(verifier.read_text(), str(verifier), "exec", optimize=1), module.__dict__)

        bogus_results = json.dumps({
            "rows": [],
            "methods": {"energy": {}, "zcr": {}, "multiband": {}}
        })

        class CorruptedPath:
            def __init__(self, name):
                self.name = name

            def read_bytes(self):
                return b"wrong SHA-256, no real data"

            def read_text(self):
                return bogus_results

            def open(self, *args, **kwargs):
                return io.StringIO("source_group,slots,gain,truth\n")

        module.Path = CorruptedPath
        with self.assertRaisesRegex(ValueError, "Original result changed"):
            module.main()


if __name__ == "__main__":
    unittest.main()
