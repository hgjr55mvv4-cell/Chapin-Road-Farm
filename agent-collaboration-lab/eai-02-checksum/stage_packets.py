"""Materialize the two builder inputs in fresh directories. Coordinator only."""
import hashlib
from pathlib import Path
import shutil
import tempfile

SOURCE = Path(__file__).resolve().parent
COMMON = ("BRIEF.md", "HISTORY.md", "SPEC.md")
OPERATIONS_SHA256 = "1363697e197098c1de96584f55a300df58017894ccccffa8132c92569000b3ee"


def stage():
    common = {name: (SOURCE / "common" / name).read_bytes() for name in COMMON}
    operations = (SOURCE / "arm-c" / "operations.py").read_bytes()
    if hashlib.sha256(operations).hexdigest() != OPERATIONS_SHA256:
        raise ValueError("supplied operations differ from the EAI-01 pin")
    root = Path(tempfile.mkdtemp(prefix="eai02-packets-"))
    try:
        for arm in ("B", "C"):
            folder = root / arm
            folder.mkdir()
            for name, data in common.items():
                (folder / name).write_bytes(data)
        (root / "C" / "operations.py").write_bytes(operations)
    except OSError:
        shutil.rmtree(root)
        raise
    return root


if __name__ == "__main__":
    print(stage())
