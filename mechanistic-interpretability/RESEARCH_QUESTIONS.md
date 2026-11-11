# Questions, falsifiers, and non-goals

**Status: DESIGN. No local model execution.**

## RQ1 — Behavioral steering versus capability

Can a frozen, bounded internal intervention **increase final correctness** on previously unseen correction cases compared with the identical strong prompt-only workflow?

**Falsifiers:** No paired accuracy advantage; gain no better than a norm-matched random direction; damage on initially correct cases; false-evidence susceptibility or quality/safety-floor violation.

## RQ2 — Representation–action gap

Can a probe encode whether the model is wrong without the model producing the correct final answer? Does acting on that probe cause net benefit?

**Falsifiers:** Probe fails out of the discovery distribution, causal intervention fails, or the apparent gain is an artifact of verbosity, refusal, guessing, or output selection.

## RQ3 — Appropriate causal lever

Do native MLP units, contrastive residual-stream directions, SAE features, or circuit components offer better specificity and efficacy?

**Falsifiers:** Semantic coherence fails causal tests; simple distributed or native baselines match more elaborate methods; intervention lies far outside observed activation ranges.

## RQ4 — Generalization

Do effects persist across case families, paraphrases, subject matter, model checkpoints and non-target tasks?

**Falsifiers:** Effect disappears when shared templates or facts are removed, or increases incoherence, overconfidence, unsafe compliance or false corrections.

## RQ5 — Practical value

Does the intervention improve at a defensible all-in cost against strong prompting, retrieval and procedural memory?

**Falsifier:** Quality parity with materially greater compute, tooling complexity or human operating burden.

## Distinctions to maintain

- **Native MLP neuron:** one unit/coordinate in the original model.
- **SAE feature:** learned dictionary coordinate, not the same neuron.
- **Residual-stream direction:** usually distributed change in an internal vector space.
- **Causal circuit:** components and relationships needed to explain an operation.
- **Probe:** predictive correlation; not automatically an effective actuator.
- **Prompt/procedural state:** external context/selection method, not an internal activation or trained weight.

## Non-goals

Persona/color demos as an endpoint; anthropomorphism or consciousness claims; generic “increase intelligence” scores without controls; safety-bypass steering; training, weight modification, live farm deployment or human-subject experiments. Study benign, rights-clear public/synthetic cases.

## Sequence and authorization gates

Public literature/documentation → independent Muse/Astra design critique → optional standard-library **mock-only** validation (requires scope check) → separately authorized model/environment qualification → exploratory candidate discovery → prospective freeze → independent confirmation and a bounded temporary decision. A gate does not automatically authorize its successor.
