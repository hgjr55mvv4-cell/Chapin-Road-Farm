# SOURCE_AUDIT — primary research and evidence limits

**Status: source/metadata spot-check, October 25, 2026; not a reproduction or comprehensive full-text systematic review.** Venue labels and results below were checked against the linked source pages where accessible. Interpret all effects as authors' reported findings unless independently reproduced.

| Work | Verified status and publication | Relevance | Scope / limiting evidence |
| --- | --- | --- | --- |
| [Bricken et al., *Towards Monosemanticity*](https://transformer-circuits.pub/2023/monosemantic-features/index.html) | Anthropic research report, 2023 | SAE features can be more interpretable than native neurons in a small model | Monosemanticity not equivalent to task benefit; page too large for complete independent fetch in this audit |
| [*Scaling and Evaluating Sparse Autoencoders*](https://transformer-circuits.pub/2024/scaling-monosemanticity/) | Anthropic research report, 2024 | Larger-scale feature extraction and intervention | Incomplete dictionaries; causal interpretation requires controlled experiments |
| [Lindsey et al., *On the Biology of a Large Language Model*](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) | Anthropic research report, March 27 2025 | Attribution graphs and perturbation studies in Claude 3.5 Haiku | Partial circuit traces; mechanism hypotheses need intervention tests |
| [Mueller et al., *MIB: A Mechanistic Interpretability Benchmark*](https://proceedings.mlr.press/v267/mueller25a.html) | **ICML 2025**, PMLR 267 | Localization and causal-variable tracks; supervised DAS strongest for causal variables, SAE features not better than neurons there | Results conditional on tested tasks/models, not proof of universal inadequacy |
| [Karvonen et al., *SAEBench*](https://arxiv.org/abs/2503.09532) | **Accepted to ICML 2025**; arXiv version 4 June 2025 | Unsupervised proxy SAE scores do not reliably predict practical gains | Comparisons depend on metrics and applications, not our correction task |
| [Basu et al., *Interpretability without actionability*](https://arxiv.org/abs/2603.18353) | **arXiv preprint**, submitted March 18 2026 | 400 physician-adjudicated triage vignettes; probe 98.2% AUROC; tested intervention families often fail to repair missed hazards | Domain- and setup-specific; clinical work is external evidence only, not a proposed project benchmark |
| [Russinovich, *CounterSteer*](https://arxiv.org/abs/2609.36570) | **arXiv preprint**, submitted Sept 29 2026 | Reported reduction in indirect prompt injection with residual-stream intervention under bounded utility gates | Author-reported; prompt-injection task only; parameter manipulation partly resisted |
| [Qwen team, *Qwen3*](https://qwenlm.github.io/blog/qwen3/) | Official Qwen release technical blog, April 29 2025 | Qwen3-0.6B: **28 layers**; Qwen3-8B: **36 layers** | Cannot run an 8B layer-30 intervention on 0.6B; checkpoint, layer indexing and model hooks still need verification |
| [Sauers original demonstration — claimed via relayed screenshot](https://x.com/Sauers_/) | Social-media report; original experiment not independently replicated here | Green/persona behavior shows a potential causal target | Exact post, weights revision, intervention sign, hook, seeds, answer selection, and multiple-testing scope not independently audited |

## Methodological warnings

1. Interpretability vs causal fidelity vs output steering vs task improvement are **four different endpoints**.
2. All references to “successful” interventions must state the author/source and domain; no local study has been run.
3. Publication venue and peer review are not independent replication.
4. Prompt comparisons must have identical questions, trustworthy/false evidence, templates, token budgets, decoding and scorer. B1 must be literally A1 plus the steering operation.
5. Do not treat correlated generations as independent experimental units or repeatedly select confirmation results.
6. The public repo is not a medical, psychological or safety-model evaluation environment.

## Remaining source verification

Before confirmation, obtain and review full implementations/data rights, post-/pre-print revisions, exact intervention method, and any independent reproducibility receipts. In particular, recover Sauers' exact demonstration source and the original Grok local files if desired; currently **UNKNOWN**.
