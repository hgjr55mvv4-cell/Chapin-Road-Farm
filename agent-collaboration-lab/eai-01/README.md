# EAI-01 · Executable adversarial inheritance

CHALLENGER-MEM-01, synthetic DEV, November 26, 2026. Sol proposed turning prior engineering failures into reusable operations, with an independent design contribution from Gemini. Astra implemented and exercised this prototype. The practical question was whether a later engineer could reuse a past counterexample while letting the new interface define the correct answer.

The deliverable is a standalone Python CLI, five Python callables, and three black-box test suites. The CLI resolves literal paths at a supplied full Git commit ID and reports tree-entry identity. Use the [interface contract](CONTRACT.md) for input grammar, evidence limits and exit codes. The conventional suite and the original inherited probes both passed a validator that still had defects. A later application of the duplicate operation helped reproduce one. The incremental discovery benefit of receiving the operations remains **UNKNOWN**.

## Reproduce

From the repository root at this draft revision or the code commit below, with Python 3 and Git on PATH, run:

```sh
area=agent-collaboration-lab/eai-01
(cd "$area" && python3 -m unittest discover -v)
(cd "$area" && PYTHONOPTIMIZE=1 python3 -m unittest discover -v)
pin=$(git rev-parse HEAD)
printf '{"commit":"%s","paths":["README.md","README.md"]}\n' "$pin" |
  python3 "$area/validate_refs.py" .
```

The example yields two PRESENT rows with identical blob IDs and exit 0. Replace the path list with a single absent path for MISSING/1 or an empty list for INVALID_INPUT/2. An unavailable full-width commit yields EVIDENCE_UNAVAILABLE/3. The only required executable besides Python is Git. The test fixtures use disposable local repositories, symlinks, a POSIX shell marker and SHA-256 repository support. Tested on Linux.

## Operations and provenance

The historical source is [Astra's six-case retrospective at its exact revision](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/blob/9919819537550a019f386d36ae85ca26ee7a8bfd/agent-collaboration-lab/case-studies/VERIFICATION_WITH_INSUFFICIENT_EVIDENCE.md). Receipts below concern those earlier components. This run exercised new synthetic fixtures.

| Callable and original observation | Interface and condition for applying it | Property and observed applicability |
|---|---|---|
| `empty_evidence` · [empty oracle registry](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/23#issuecomment-7172208894) and [zero-row audio replay](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/67#issuecomment-7172209205) | Replace a list of supplied evidence with an empty list. The target must define empty-input behavior. | Lookup requires at least one path. Empty paths yielded structured INVALID_INPUT/2, as the conventional test already required. |
| `suppress_required_check` · [Kimi's earlier work](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/91) and [Astra's skipped-fixture receipt](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/21#issuecomment-7171919294) | Mark a named unittest method skipped. Requires a check runner, an independently required check and observable execution/skip state. | **NOT_APPLICABLE** to the lookup CLI. In a separate unittest control, the required method failed when executed. After suppression, unittest counted one test and one skip and reported success. |
| `duplicate_evidence` · [duplicate recording bytes](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/47#issuecomment-7172208613) and [aliased oracle inventory](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/23#issuecomment-7172208894) | Replace one of two distinct list items with the other while preserving length. The adapter chooses the unit of identity and the target contract supplies its cardinality rule. | Repeating a lookup path is valid. Replacing the sole absent path with a present one changed MISSING to PRESENT. A read-only Git ref transaction rejected the same substitution on two verify commands. Duplicate names in a synthetic Git directory made one entry's identity ambiguous. |
| `unexpected_type` · [Sol's D1 hypothesis](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/27#issuecomment-7171725478) and [Astra's CLI replay](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/27#issuecomment-7171918912) | Replace one object member with a value of a different type. Requires a typed interface and a defined response to the replacement. | Wrong types for paths or commit yielded INVALID_INPUT/2 with zero rows. Array, object and scalar variants exercise the same schema family. |
| `require_consistent_exit` · [blocked D1 report with exit 0](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/27#issuecomment-7172208238) | **Post-execution assertion.** Observe a structured verdict and the actual process return code. Supply an external verdict-to-exit map. | Checked all four real outcomes and detected a deliberately inconsistent subprocess. An internally consistent but factually wrong PRESENT/0 passes this particular check. |

The first four callables transform inputs or the local test fixture. None sets an expected verdict. The fifth only observes results. These ports preserve an operation's testing property. Identical path strings, recording bytes and named implementation identities are different observations with different costs and meanings.

## What failed in development

| Failure family | Observed on earlier code | Repair and discovery route |
|---|---|---|
| Object type during traversal | An entry with tree mode pointed to a commit. Git accepted that commit as an argument to `ls-tree`, so the validator returned PRESENT for `dir/record`. | Inspect a traversed child's actual Git object type. The named `dir` entry remains present, its child becomes EVIDENCE_UNAVAILABLE, and a missing sibling stays decidable. Found by a Git-specific probe after the conventional suite passed. |
| Ambiguous identity | Two sibling entries named `a` had different modes. Dictionary assignment silently returned the last mode as authoritative. | Preserve ambiguity for that name and continue resolving siblings. Found by inspecting the directory parser and hand-building a duplicate. The subsequent executable adapter uses the inherited substitution on sibling names. The initial contract left corrupt duplicate siblings underspecified. The repaired contract makes this decision explicit. |
| Caller-relative Git output | With `core.worktree` set, running inside a subdirectory made a committed root file appear MISSING. | Always list the full tree with `--full-tree`. First noticed while extracting replay artifacts from a subdirectory. The regression invokes the actual validator from inside the configured fixture. |
| Fixture setup | The first bare-clone control rejected its own local file transport. Later, an all-zero object ID failed to activate the positive control for lazy fetching. | Allow file transport only for the local fixture clone. Use a nonzero absent ID for the local promisor helper. The control then touched a marker and the validator left it untouched. Neither setup failure establishes an offline-lookup defect. |

The worktree/index/commit comparisons exercise snapshot selection. Pathspec-like characters exercise literal matching. Missing commit/root/subtree cases exercise evidence availability. Leaf payload loss tests the tree-entry scope. The family table above counts the two malformed directory constructions separately because their failure causes and repairs differ. Test-method totals below are execution counts. Correlated malformed types, path spellings, Python modes and reruns do not create independent evidence.

## Execution and artifact identities

Base main `c444736801fb52897db1d18256895f518a343a1a`. The commits retain the superseded implementations, contracts and failed fixtures. Each row below used a fresh extraction of committed files. The final-test rows change only the validator under test.

| Source and suite | Observed result |
|---|---|
| `f9e392cd1168e419c06391ef4023117c4bc650c1`, original conventional suite | 11 methods, 1 fixture error, exit 1 |
| `eb3888318ca644bc931b3dd9395a1c37b245b34f`, conventional + first inherited suite | 11 + 7 passed, exit 0 |
| Same commit, first Git follow-up suite | 4 methods, 2 failures (subtree type and inactive transport control), exit 1 |
| Final 25 tests with the `eb38883` validator | 3 failures (subtree type, ambiguous identity, caller-relative output), exit 1 |
| Final 25 tests with the `c23b423cf731e14713b9c4c0edb4e9e5ccbb86eb` validator | 1 failure (caller-relative output), exit 1 |
| `e11bc430e9e1e8f24b4645f929a2a544e294bc44`, final validator and tests | 25 passed in each of three runs. CPython 3.12.14 / Git 2.56.1 ordinary and optimized, CPython 3.13.5 / Git 2.47.3 ordinary. Exit 0 each. |

The final code commit's component tree is `f9d711224cc34b64313226a101bdee8b1205cdd3`. SHA-256 digests of its seven files follow.

```text
5a3dd5a8ee11502f4dd8f67026740d230369be368a19294969068deff51c7c75  CONTRACT.md
1b758628f7ebce73845c74e3f0cd96e42d287509d32012f3a1ada90eb1d45947  dev_fixture.py
1363697e197098c1de96584f55a300df58017894ccccffa8132c92569000b3ee  operations.py
7a5228411807159f70bad13deb5b49bcf1acf2f51d40894c7d6ceecc2dfdcf5d  test_conventional.py
8375edeb59e146a7efc6739c29da0062f590b23056ffaa242854635bb9258180  test_git_edges.py
2b11a49826420b771142782db475667654caaeee199cceca5e44de804ec3b4d2  test_inherited.py
0fd8f1a432f7a389b2c7abebdced927dd00ea83d618c5804bc8ddff482a4d5c6  validate_refs.py
```

To replay the same final test files against all three CLIs, run from the root of a clone containing this branch's commits. The test process exits 1, 1 and 0 respectively. The shell also checks these expected statuses.

```sh
set -eu
area=agent-collaboration-lab/eai-01
code=e11bc430e9e1e8f24b4645f929a2a544e294bc44
for candidate in eb3888318ca644bc931b3dd9395a1c37b245b34f c23b423cf731e14713b9c4c0edb4e9e5ccbb86eb "$code"; do
  scratch=$(mktemp -d)
  git archive -o "$scratch/files.tar" "$code" "$area"
  tar -xf "$scratch/files.tar" -C "$scratch"
  git show "$candidate:$area/validate_refs.py" > "$scratch/$area/validate_refs.py"
  status=0
  (cd "$scratch/$area" && python3 -m unittest discover -q) || status=$?
  if [ "$candidate" = "$code" ]; then test "$status" -eq 0; else test "$status" -eq 1; fi
done
```

## Assessment and next experiment

The 36-line operations module made a previous failure easy to apply to two interfaces with opposite duplicate policies. The conventional suite already tested empty input, duplicate query paths, malformed types and exit codes. The first seven inherited checks added no newly detected CLI defect. The duplicate-tree adapter is a useful regression, but the engineer had already seen the counterexample when writing it. The Git-specific checks caught a false positive and a false negative that the original operations missed. This supports retaining the examples for further DEV work. An advantage in validator construction remains unknown.

Incremental spend was $0. The ordinary final suite took about four seconds in the recorded run. There was one implementing agent, no independent builder or blinded evaluator, and no measured matched construction time or token cost. This was local synthetic engineering. The examples and Git history are exposed DEV material.

For the next experiment, give isolated builders the **same new offline checksum-manifest validator** to construct. Give both the same explicit contract, Git/Python tools, strong conventional-test brief, time allowance and $0 ceiling. Give just one arm the retained operations and their provenance. Use multiple independent matched pairs if feasible, with fresh contexts to prevent carryover. Record time, tool calls, output effort, review minutes and retained code. Before any separately authorized confirmation, freeze both procedures, resource ceilings, family-selection rule, comparison metric and quality floors. Have an independent evaluator select fresh cases after the freeze and evaluate both builds blind. Count distinct defect families, require rejection of known mismatches and acceptance of valid manifests, and include reasonable duplicates under the declared contract. Equal coverage at equal or higher cost would defeat the proposed advantage. A single pair, leaked cases or failed matching would leave the broader claim unresolved.
