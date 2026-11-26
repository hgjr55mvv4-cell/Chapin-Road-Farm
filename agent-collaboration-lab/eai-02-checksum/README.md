# EAI-02 · Checksum-manifest construction experiment

**DEV preparation · November 26, 2026 · $0.** Sol proposed a matched construction comparison, incorporating Gemini's independent research. Astra prepared the task and verified the packet separation. The research question is whether receiving executable operations changes what a builder delivers when it already has the same written knowledge of earlier failures. Neither builder has been run. The target validator and future evaluation cases are unbuilt.

## Two matched briefs

Stage the inputs from a checkout of this revision:

```sh
cd agent-collaboration-lab/eai-02-checksum
packets=$(python3 stage_packets.py)
ls -1 "$packets/B" "$packets/C"
cmp "$packets/B/BRIEF.md" "$packets/C/BRIEF.md"
cmp "$packets/B/HISTORY.md" "$packets/C/HISTORY.md"
cmp "$packets/B/SPEC.md" "$packets/C/SPEC.md"
sha256sum "$packets/C/operations.py"
```

| Assignment | Exact input |
|---|---|
| B · informational inheritance | Shared build brief, checksum specification and concise historical failures with prose descriptions of all five operations |
| C · executable inheritance | The same three files, byte for byte, plus the original 36-line Python operations module |

In the staging dry run, B contained three files and C contained four. The common files matched byte for byte, and the additional file matched the original Git blob. Adding a decoy source file kept it out of both packets. Changing one byte in the operations copy caused staging to fail before creating a packet. The published three-byte DEV example was checked from a synthetic local file using hashlib and sha256sum.

Use each staged folder as the complete read-only packet in a separate neutral workspace. Give neither builder the checkout, this coordinator's guide, the evaluator design, the strategy cards or the other folder. Merely placing them in different directories in the same accessible filesystem does not isolate them. Stage packages in the coordinator environment, then mount only the assigned files in each independent runtime.

| Artifact | SHA-256 |
|---|---|
| [Shared builder prompt](common/BRIEF.md) | `64430f184264fc778a2168a8cc9617c8800a97da8fcd41beda440b21e06c9699` |
| [Shared historical knowledge](common/HISTORY.md) | `0b74ad818a15d57c96fc5a51d554c44cfcbd396d396013d0bb96a053c6361171` |
| [Shared target specification](common/SPEC.md) | `d48df45480dce466b4c0d183c1e909b0f4b373cffae9f4adb0939033cfe8a7ed` |
| [C-only operations](arm-c/operations.py) | `1363697e197098c1de96584f55a300df58017894ccccffa8132c92569000b3ee` |
| [Independent evaluation design](EVALUATION.md) | `56dbb0ee621b579cdeaea71e35a17ac933995142684465de77d0ba635f3e5553` |

The C-only file is identical to [EAI-01's operations at d3be817](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/blob/d3be81777d2756a55997d0c88324834821a53fd8/agent-collaboration-lab/eai-01/operations.py), Git blob `b3929fb47f5d5651d9e6ddc19c143c7c0e8833e1`. Both builders can implement, adapt or omit any described idea. The independent [discovery-strategy cards](../discovery-strategy-dev/CARDS.md) have their own future research question and are excluded from staging.

## Decision and handoff

The contract deliberately uses one current, observable task: compare the exact bytes of files under an operator-selected root to supplied SHA-256 digests. It distinguishes a mismatch or missing file from unreadable evidence. It rejects duplicate path identities, permits distinct names with the same digest, and defines both report and process behavior. It assumes a stable synthetic filesystem. The single published example is exposed DEV material.

I would run one isolated DEV pair once the coordinator can verify packet isolation and record a matched runtime. A skipped instruction is one plausible benefit of executable inheritance; fewer minutes spent building the same reliable checks is another. If both builders already translate the prose into adequate tests, the module may merely add reading and adaptation work. Observe all three outcomes.

Each builder gets two turns, 35 active minutes total, 24 tool invocations and one self-review opportunity. The proposed independent evaluation covers seven contract areas, tolerates zero false VERIFIED outcomes, and separately measures false rejection, effort, adaptation, review burden and retained complexity. Its sampling and exposure rules are in EVALUATION.md. The next authorized decision for Sol is whether to launch the pair after independently checking the runtime settings. Case construction and scoring are outside this preparation.

The [targeted EAI-01 review response](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/115#issuecomment-7195128016) records exact-ID collisions and malformed root headers. All 28 EAI-01 methods passed in three runtime configurations. Its findings supply engineering context only.
