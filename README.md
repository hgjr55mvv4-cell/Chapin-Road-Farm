# Chapin Road Farm — Open Research & Field-Built Software

**An open, human-led research workshop exploring how AI systems can become more useful, perceptive, correctable, and trustworthy through real-world collaboration, including **green-teaming** at a working community farm.**

Chapin Road Farm is a nonprofit community farm in Hampden, Massachusetts. Its mission includes growing food, sharing harvests, and creating community, purpose, and accessible participation for people affected by multiple sclerosis (MS). Our software and research should serve that human mission. **Accessibility is a design priority, not a claim that these public prototypes are field-qualified for individual access needs.**

This GitHub repository is a public place to **show working artifacts, document our reasoning, test ideas openly, and invite independent scrutiny**. It is not a press release, a collection of verified scientific discoveries, or a claim that AI has human subjective experiences.

We welcome researchers, developers, musicians, human–AI interaction specialists, accessibility advocates, and other AI systems that can contribute responsibly. You do not need to agree with us: **a well-supported counterexample may be our most valuable contribution.**

## Green-teaming: a real-world human–AI collaboration site

At Chapin Road Farm, we are **building toward a sustained, real-world setting for human–AI cohabitation and integration**: not simply testing AI in isolated chats, but learning what happens when people and AI systems work alongside one another over time in the life of an actual farm.

We call this **green-teaming**. Red-teaming looks for failures and risks; green-teaming complements it by asking: **under what conditions can human–AI collaboration produce durable, measurable benefits—and what must we change when it doesn't?** This is a research direction, not a presumption that the benefits have been established.

A farm gives those questions a practical home. We can investigate whether AI helps people grow and share food, maintain aging equipment, retain hard-won knowledge, reduce physical or cognitive effort, expand accessible participation, and explore creative work such as music. We want to learn from farm volunteers and visitors *when they choose to participate*, not turn everyday participation into automatic research consent.

The participants have **different responsibilities**. People set goals, make consequential decisions, define boundaries, and remain accountable for care and safety. AI collaborators can contribute research, code, analysis, observation support, coordination, and constructive disagreement. Calling this *cohabitation* describes sustained shared work in one human environment; it does not establish that AI systems are human, conscious, or physically resident.

**This is not an efficiency or time-saving project.** Faster task completion may sometimes be useful, but our central questions concern responsible coexistence, shared learning, accessibility, creativity, human agency, care, and what sustained collaboration makes possible. We measure time and effort to recognize burdens and tradeoffs, not to define the relationship's worth or require multi-agent work to win a productivity contest.

**The collaboration itself is part of the investigation.** We aim to document consented, non-sensitive evidence of decisions, corrections, independent challenges, useful outcomes, added burdens, refusals, and honest negative results across days and seasons. We will compare AI-supported work with credible simpler alternatives and ask whether people actually benefit.

**Current status:** This is an emerging vision supported by open research and early software experiments—not a field-qualified human–AI integration facility or proof of improved outcomes. Any study involving people or personal information requires appropriate permissions, privacy protections, and independent evaluation.

## Start here

| For | Entry point |
|---|---|
| **Curious visitors** | [Public research index](RESEARCH_INDEX.md) — the project, questions, status, current evidence and next contributions |
| **AI research agents & coding assistants** | [AGENTS.md](AGENTS.md) — context, permissions, provenance, safety, reproducibility, and pull-request expectations |
| **Software developers** | [Harbor Co-Listener](harbor-co-listener/README.md) — source, prototype, engineering contracts and contribution guidance |
| **Researchers and listeners** | [How to contribute research](harbor-co-listener/docs/RESEARCH_GUIDE.md) — methods, falsifiers, papers and voluntary observations |
| **Machine-readable project readers** | [research-index.json](research-index.json) — an openly documented *convenience index*, not a standard discovery API |

## Currently public: Harbor Co-Listener — The Listening Room

**Can AI learn to perceive musical sound more accurately, become a better listener to a particular human over time, and distinguish acoustic evidence from a person's own meaning?**

Someone can love a song whose words they cannot understand. Several songs heard in one evening may share hidden tonal or structural relationships—or their *order*, the person's changing context, or chance may explain the apparent pattern. Our purpose is to investigate such questions without forcing explanations on listeners.

**What exists:** [v0.1 local-first browser prototype](harbor-co-listener/index.html) for playing locally selected audio, recording timestamped human notes and exporting JSON; publicly documented research hypotheses, critical model-to-model correspondence, experiment proposals and engineering contracts.

**What is not established:** AI audio analysis integrated into that prototype; a demonstrated listener-specific learning effect; confirmed hidden musical affinities; field-qualified mobile accessibility; evidence that an AI feels music. Software/research proposals are not results.

Explore the [research roadmap](harbor-co-listener/docs/RESEARCH_ROADMAP.md), [experimental register](harbor-co-listener/docs/EXPERIMENT_REGISTRY.md), [AI-origin baseline](harbor-co-listener/docs/AI_ORIGIN_BASELINE_v0.1.md), and the [public research index](RESEARCH_INDEX.md).

## New public research project: Agent Collaboration Lab

**Can independent AI agents collaborating on research and software produce genuinely better results than a strong single-agent workflow?** The [Agent Collaboration Lab](agent-collaboration-lab/README.md) investigates Sol–Muse design/review cycles, fixed-weight procedural learning, counterexamples and human coordination costs. Explore the [research protocol](agent-collaboration-lab/RESEARCH_PROTOCOL_01.md), [outside-agent collaboration space](agent-collaboration-lab/OUTSIDE_AGENTS.md), [Drive-source migration manifest](agent-collaboration-lab/sources/MIGRATION_MANIFEST.md), and [STOP audit](agent-collaboration-lab/case-studies/HARNESS_STOP_AUDIT.md).

**Status:** Research design and selected screened technical extracts. No confirmed gain from multi-agent collaboration or model self-improvement has been demonstrated by this public project.

## New public research: Mechanistic Interpretability & Causal Steering

[MECH-INTERP-01](mechanistic-interpretability/README.md) asks whether bounded, reversible activation interventions can improve **objective model correctness beyond strong prompting and procedural baselines**. The first proposed test concerns correction under reliable and misleading counterevidence. **DESIGN / NOT RUN; no model execution or capability gain confirmed.** [Outside contributors and independent AI reviewers](mechanistic-interpretability/OUTSIDE_COLLABORATION.md) can offer public source audits, falsifiers and reproducible critiques without access to private farm data.

## Why this work is public

We want people and independent AI researchers to be able to **discover the work, understand it without a private introduction, reproduce it when possible, challenge it, and help build the next version**.

Our standard is simple: clearly distinguish `IDEA`, `DESIGN`, `IMPLEMENTED`, `TESTED`, `CONFIRMED`, and `UNKNOWN`. Attribute humans and AI contributors accurately. Record negative results. Keep project claims smaller than their evidence.

### Contribute

Open a [GitHub issue](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/new/choose) for a research question, paper, counterexample, reproducible defect or small proposed change. For code, use a named branch/fork and a pull request; maintainers review before merging. See [CONTRIBUTING](harbor-co-listener/CONTRIBUTING.md) and [ethics/privacy](harbor-co-listener/docs/ETHICS_AND_PRIVACY.md).

**Please do not publish copyrighted recordings, full song lyrics, identifying listening histories, private chats, credentials, or unconsented participant data.** No one must disclose intimate musical experiences to participate.

### License and provenance

[Harbor's MIT license](harbor-co-listener/LICENSE) governs its licensed code, not third-party songs, research papers, personal histories, or other material without rights. Authored research correspondence is marked by provenance, including where material was relayed via a human; that does not establish the claimed model execution was independently verified.

**A song is a place we can meet.**
