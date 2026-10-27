"""Verify test-discovery gap with Python stdlib only. NOT original audit code."""
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent


def require(condition, detail):
    """Fail closed even when Python removes assert statements with -O."""
    if not condition:
        raise ValueError(detail)


# Do not let an inherited optimization setting disable the fixture's own asserts.
child_env = os.environ.copy()
child_env.pop('PYTHONOPTIMIZE', None)

cmds = [
    ("direct plain-function tests", [sys.executable, str(root/'bad/test_checks.py')], "DIRECT_CHECKS_EXECUTED=2", {0}),
    ("broken discovery", [sys.executable, '-m', 'unittest', 'discover', '-s', str(root/'bad'), '-p', 'test_*.py', '-v'], "Ran 0 tests", {0,5}),
    ("repaired discovery", [sys.executable, '-m', 'unittest', 'discover', '-s', str(root/'good'), '-p', 'test_*.py', '-v'], "Ran 2 tests", {0}),
]
print('Python', sys.version.split()[0], 'platform', sys.platform)
for name, command, marker, expected_codes in cmds:
    result = subprocess.run(command, text=True, capture_output=True, env=child_env)
    transcript = result.stdout + result.stderr
    print('\n##', name)
    print('command:', ' '.join(command))
    print(transcript.strip())
    print('exit_code:', result.returncode)
    require(result.returncode in expected_codes,
            (name, 'unexpected exit code', result.returncode, expected_codes))
    require(marker in transcript, (name, 'missing required marker', marker))
print('\nVERIFICATION_PASS: 0-test discovery versus 2-test repaired path reproduced (Python 3.13+ may exit 5 on zero tests)')
