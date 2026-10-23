# Oracle unknowns and interpretation disputes

An **UNKNOWN** is not a negative outcome, and disagreement between two LLMs is not a ground-truth resolution. Source and status must remain visible.

| Question | Evidence / known boundary | Status | Action |
|---|---|---|---|
| Is normalization allowed for “distinct string key”? | T2 allows string keys but does not explicitly define Unicode normalization. Python `str ==` treats composed and decomposed code-point strings as different. | **OPEN SPEC CLARIFICATION** | Propose a new T2 version defining code-point equality, case and whitespace; review independently before freezing. |
| What if interval start exceeds end? | T1 explicitly defines valid integer input as `start <= end`. | **OUT OF SCOPE**, not an implementation failure | Define invalid-input behavior only in a future version. |
| Were original STOP code claims reproduced here? | Only source-reported editorial extracts; private archive withheld. | **UNKNOWN / NOT RUN** | Don't count synthetic public exercises as the original audit. |
| Is dual-agent oracle construction better? | No blinded prospective, matched-cost model runs. | **UNKNOWN / NOT RUN** | Keep D1 causal study HOLD. |
| Can Muse read source directly? | Muse reported repeated GitHub blob fetch restrictions. | **PROVENANCE LIMITATION** | Include verbatim public contract in direct handoffs; don't classify speculative cases as confirmed defects. |

Preserve original contract and reported evidence; use versioned addenda for a substantive policy change. Do not publish held-out confirmation tasks.
