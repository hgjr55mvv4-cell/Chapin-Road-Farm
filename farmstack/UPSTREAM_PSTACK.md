# pstack upstream integration — source and host audit

**Status: REFERENCE REGISTERED / NOT INSTALLED.** The official source was inspected through GitHub on **2026-10-26**. Entries below describe upstream metadata at that inspection point; future releases may differ.

## Canonical upstream

- **Project:** [pstack](https://github.com/cursor/plugins/tree/main/pstack), in public [cursor/plugins](https://github.com/cursor/plugins).
- **Author and social identity:** [Lauren Tan](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json), linking as `@poteto` in its [README](https://github.com/cursor/plugins/blob/main/pstack/README.md).
- **Plugin manifest:** [`pstack/.cursor-plugin/plugin.json`](https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json), inspected manifest Git blob `2d5accfaed9959e5a15226df48b17a59a16a4132`, version **0.15.32**.
- **License:** [`pstack/LICENSE`](https://github.com/cursor/plugins/blob/main/pstack/LICENSE), **MIT**, copyright **2026 Lauren Tan**. Preserve copyright and the MIT text for substantial copied/adapted source. We have copied no upstream code into this draft.
- **Core entry point:** [`skills/poteto-mode/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md), playbook routing with principles, verification and model-specific delegation.
- **Learning from mistakes:** [`skills/correct/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md), which prioritizes structural, typed, lint or behavioral-test guards over repeatedly writing instructions.
- **Host setup:** [`skills/setup-pstack/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md). Model slugs are host/account-specific and must be detected before configuration.

## Installation routes documented by upstream (NOT executed)

**Cursor plugin-compatible environment:**
```text
/add-plugin pstack
```

**Claude Code-compatible environment:**
```text
/plugin marketplace add cursor/plugins
/plugin install pstack@cursor-plugins
```

These are instructions to be issued **inside those products**, not GitHub Actions, iOS Terminal, ChatGPT messages, or this repo. They require an appropriate host, entitlement, permissions and evaluation of third-party instructions. There is **no matching ChatGPT-native pstack plugin** in the ChatGPT plugin directory from the exact-name search conducted on 2026-10-26. Its GitHub presence is not evidence of ChatGPT installability.

## Portability matrix (design hypothesis, not tests)

| Component | Cursor | Claude Code | ChatGPT + GitHub tools | FarmStack direction |
| --- | --- | --- | --- | --- |
| Plugin and slash-command loading | Supported in upstream README | Documented via pstack Claude Code adapter | **Not directly available as pstack** | Link to upstream; no false install claim |
| Human-readable skill/playbook guidance | Supported | Documented | Can read public files manually, not automatic plugin runtime | Extract *ideas*, independently rewrite concise CRF-specific guidance |
| Autonomous subagents / model routing | Host-dependent | Host-dependent | Tools/entitlements differ | Abstract roles; avoid hardcoded vendor/model or hidden spending |
| Code verification and PR stacking | Host workflow | Host workflow | GitHub connector supports bounded branches, code reviews and PRs | Verify branch ancestry and changed files before status claims |
| Auto merge, long-lived agents, autonomous loops | Upstream workflow variants | Environment-dependent | Not authorized | **DISABLED/HOLD** regardless of upstream defaults |
| Repeated-error guardrails (`correct`) | Skill instructions | Via adapter if supported | No direct command; can adapt concept | Candidate first experiment: catch wrong-base branch creation with test/guard |

## Acceptance gates before installation/vendor

1. **Host reality:** somebody with an authorized Cursor/Claude Code environment can install and report real commands. No account/device assumptions.
2. **Security:** inspect exact pinned plugin revision, permissions, external network/tool commands, optional package dependencies, branch/write rights, auto update settings and generated files.
3. **Rights:** if adapting source files, retain MIT attribution/license and identify exact copied portions; mere attribution does not replace tests.
4. **Isolation:** install in a sandbox/authorized checkout before production integration; disable unrestricted autonomous merging, code execution, purchases and background activity.
5. **Value:** compare against our existing AGENTS.md + explicit draft PR protocol on **one** historical defect or source audit, with identical evidence and outcomes. Measure failure catch rate, regression and total human/tool cost. No claim of increased intelligence from adopting a skill framework.
6. **Operator control:** no required desktop or prolonged manual setup for the iPad-primary operator; allow another authorized team member to supply a compatible development host.

**Decision as of this draft:** Include pstack as a researched external dependency/inspiration. **Do not vendor, auto-install, activate or fork entire upstream** until host compatibility, security and measurable marginal benefit are established.
