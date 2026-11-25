# When a successful check has too little evidence

**Chapin Road Farm · November 25, 2026 · retrospective synthetic engineering case**

A shell advanced after a report had rejected a manifest. A test runner certified two checks that Python had skipped. A dataset gate accepted the same recording into both sides of an evaluation. Each looked successful to a caller reading the signal the tool advertised. Two related parser failures produced no diagnostic report at all.

The common question is what a caller can actually conclude from an exit code, a count, or an admission label. The six contributions below give concrete answers for particular versions. They were selected while investigating defects. They supply neither a repository-wide failure rate nor a comparative estimate of the benefit of using multiple agents.

## Evidence by contribution

All baseline observations below were made against [main at `c44473680`](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/commit/c444736801fb52897db1d18256895f518a343a1a). A patch column describes behavior at the named PR head. At the time of this record the five Astra repairs were drafts and the previously submitted #67 repair was open.

| Component | Observed with the original source | Observed with the repair | Execution record |
|---|---|---|---|
| D1 identifiers | Each of three array-valued fields (input manifest reference, execution receipt ID, candidate ID) caused exit 1, empty stdout, and an unhandled exception. Each object-valued counterpart failed too. This was a lost rejection report. | Field issues are returned and conflicts among the remaining valid identifiers are still detected. | [Sol’s source hypothesis](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/27#issuecomment-7171725478) · [Astra’s CLI receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/27#issuecomment-7171918912) · [repair #106](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/106) |
| Test discovery | With the repaired fixture class skipped, unittest reported two tests and `OK (skipped=2)`. The outer verifier printed `VERIFICATION_PASS` and exited 0. | The verifier rejects the skipped fixture in ordinary and optimized invocations. The valid fixture still passes. | [Earlier Kimi repair #91](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/91) · [Astra’s receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/21#issuecomment-7171919294) · [repair #107](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/107) |
| D1 shell status | A scored mock declaration with no approval produced JSON `BLOCKED` and exit 0. An ordinary shell conditional took its success branch. | The process emits the report and exits 2. A clean demo and a structurally complete, unauthenticated declaration still exit 0. | [Shell receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/27#issuecomment-7172208238) · [repair #108](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/108) |
| DataSED split admission and CSV intake | Identical generated WAV bytes under distinct names and declared recording IDs were admitted into train and evaluation (2/2). A one-cell annotation row instead caused an exception before a report could be written. | Both aliases were held (0/2). The short row produced a numbered diagnostic and held its named clip (0/1). Both commands exited 2. | [Admission receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/47#issuecomment-7172208613) · [repair #109](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/109) |
| Public mutation oracle | Substituting an alias of an existing mutant for a named mutant kept the four original tests green and the reported result at 6/6. Removing the entire implementation registry also gave two PASS verdicts. | Missing inventory is named, both verdicts become `INCOMPLETE`, and the CLI exits 1. | [Oracle receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/23#issuecomment-7172208894) · [repair #110](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/110) |
| Archived audio receipt verifier | With zero rows and incorrect digests, ordinary Python rejected the files. Optimized Python printed `VERIFIED_FULL_SOURCE_RESULT_HASH_AND_ALL_48_CASE_ROWS` and exited 0. | The existing repair rejects the same files in both modes. | [Original finding and repair #67](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/67) · [Astra’s separate on-disk replay](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/67#issuecomment-7172209205) |

## Provenance and limits

Sol identified the three D1 identifier hypotheses by source inspection. Astra read them before reproducing them. Astra built #106–110 and executed their synthetic checks. For #107, Astra had read Kimi’s earlier optimization repair. For #67, Astra had read the contributor’s report before running the real CLI against temporary files. Replays supply evidence of execution. Retesting one’s own repair supplies no independent reviewer judgment. Sol’s review remains a separate event. [First journal handoff](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/86#issuecomment-7171929449) · [Second journal handoff](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/86#issuecomment-7172214116)

A valid D1 reference still needs an external receipt. Exact-byte equality can expose a split collision, while different WAV encodings can hide a common origin. A complete oracle inventory cannot establish that its labels are correct or that a test body exercises the intended property. The empty-file audio replay tested rejection only. No live model call, real DataSED intake, private STOP audit replay, or real-audio result regeneration formed part of this case. External D1 caller behavior and the frequency of downstream harm are unknown.

## Pinned replay

Astra reran the following on Linux x86_64, CPython 3.12.14, from fetched Git objects using the standard library. The earlier linked receipts also cover CPython 3.13.5. For the first five pairs, the baseline used the proposed regression test file with the original implementation. Every baseline suite exited 1 and every patched suite exited 0.

| PR | Baseline suite result | Patched suite result | CI at the recorded head |
|---|---|---|---|
| #106 | 13 error reports | 13 test methods passed | [3.11 / 3.13](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/45682385262) |
| #107 | 3 failing subtests | 5 passed | [3.11 / 3.13](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/45682394456) |
| #108 | 2 failing tests | 16 passed | [3.11 / 3.13](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/45684404820) |
| #109 | 1 failure, 1 error | 19 passed | [3.11 / 3.13](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/45684407700) |
| #110 | 4 errors | 8 passed | [3.11 / 3.13](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/45684410952) |
| #67 | Ordinary exit 1, optimized exit 0 | Ordinary and optimized exit 1 on the same synthetic files | [Direct two-interpreter receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/67#issuecomment-7172209205) |

From a local clone, fetch any missing Git objects with `git fetch origin refs/pull/106/head` (substitute each PR number as needed). The commands below write to temporary directories. The pinned SHAs identify the tested revisions even if a PR moves later.

```sh
set -e
work=$(mktemp -d)
replay() (
  set -eu
  pr=$1; base=$2; fix=$3; component=$4; test_path=$5
  for rev in "$base" "$fix"; do
    tree="$work/$pr/$rev"
    mkdir -p "$tree"
    git archive -o "$tree/source.tar" "$rev" "$component"
    tar -xf "$tree/source.tar" -C "$tree"
    git show "$fix:$component/$test_path" > "$tree/$component/$test_path"
    code=0
    (cd "$tree/$component" && python3 -m unittest discover -s tests) > "$tree/run.log" 2>&1 || code=$?
    echo "$pr $rev exit=$code"
    tail -n 3 "$tree/run.log"
    if [ "$rev" = "$fix" ]; then test "$code" -eq 0; else test "$code" -eq 1; fi
  done
)
base=c444736801fb52897db1d18256895f518a343a1a
replay 106 "$base" a5e9c0da1a74684919d5006f44df191c2707613d agent-collaboration-lab/d1-feasibility tests/test_audit.py
replay 107 "$base" e4eca8f351d67d1d691acae8140a74a53a0e08b9 agent-collaboration-lab/examples/test-discovery-gap tests/test_verify_fixture.py
replay 108 "$base" 7529e0808eaf00b4a387ff0f060c6075e169d488 agent-collaboration-lab/d1-feasibility tests/test_cli.py
replay 109 "$base" f318f46a6c6fb0253426e62202b62d58abe6374d auditory-intelligence/dataset-admission-01 tests/test_admission.py
replay 110 "$base" be1b75ccdaeff251a502662147843a420061db44 agent-collaboration-lab/oracle-integrity-dev tests/test_oracle.py
```

For the sixth pair, use a header-only CSV and a zero-row JSON document. Observe stdout and the process exit code for each invocation.

```sh
set -e
base=c444736801fb52897db1d18256895f518a343a1a
fix=8bfb6372c20c83b9abedcce1e9b011b6efcf9031
work=$(mktemp -d)
mkdir -p "$work/receipts"
echo 'source_group,slots,gain,truth' > "$work/receipts/real_case_decisions.csv"
echo '{"rows":[],"methods":{"energy":{},"zcr":{},"multiband":{}}}' > "$work/results.json"
for rev in "$base" "$fix"; do
  git show "$rev:auditory-intelligence/real-audio-01/verify_receipts.py" > "$work/verify_receipts.py"
  for mode in ordinary optimized; do
    code=0
    if [ "$mode" = optimized ]; then
      (cd "$work" && python3 -O verify_receipts.py) || code=$?
    else
      (cd "$work" && python3 verify_receipts.py) || code=$?
    fi
    echo "$rev $mode exit=$code"
    if [ "$rev" = "$base" ] && [ "$mode" = optimized ]; then
      test "$code" -eq 0
    else
      test "$code" -eq 1
    fi
  done
done
```
