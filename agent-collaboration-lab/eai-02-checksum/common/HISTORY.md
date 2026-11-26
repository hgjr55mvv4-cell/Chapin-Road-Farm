# Historical engineering knowledge · shared brief v1

These observations concern earlier tools with different contracts. Each proposed perturbation or observation below is optional. Derive its expected outcome from the new target specification.

| Failure family | Earlier observation | Reusable operation and limits |
|---|---|---|
| Empty evidence | A verifier reported success on an empty evidence inventory. | Given a list, substitute a fresh empty list. The contract determines whether it is valid, invalid or gives an indeterminate result. |
| Required-check suppression | A runner counted skipped checks and still reported success. | Mark a named unittest method skipped with the standard unittest skip facility and observe what actually ran. This applies only when a particular check is required and execution is observable. |
| Duplicate evidence | Substituting an existing item for a distinct one kept the item count intact. | In a copy of a list, replace one destination item with the item at a different source position. Start with unequal items and preserve length. The target determines the unit of identity and whether repetition is legitimate. |
| Unexpected data type | A wrong-type JSON field caused an exception before a structured rejection. | In a copy of a mapping, replace one existing member with a value of a different Python type. Choose a replacement that exercises a distinction in the target's contract. |
| Verdict and exit disagreement | A tool wrote a blocked verdict but returned a successful process status. | After execution, compare the observed process return code with the independently specified code for the structured verdict. An unknown verdict or a disagreement fails that check. The observer cannot detect a factually wrong but internally consistent pair. |
