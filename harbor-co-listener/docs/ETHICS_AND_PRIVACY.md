# Ethics, music rights, and consent

## Personal meaning belongs to the listener

Our project must not mine trauma, relationships, identity, or emotional vulnerabilities from song choices. **A person decides what a song means to them.** The AI can offer a tentative listening observation, not a diagnosis or a claimed private memory. A different listener's reaction can also be valid.

## Local first

The v0.1 web prototype loads user-supplied audio as a local browser object and stores note state in the open tab. Session JSON exports contain text and timestamps, **not audio bytes**; they can still contain highly personal stories. Review before sharing. Browser sessions are not a reliable archival record.

Proposed future listener profiles must be opt-in, inspectable, revocable, short-lived by default, scoped to the intended listener, and never silently shared with other AIs or research datasets. No such feature is yet implemented. We will not claim perfect deletion from public GitHub history.

## Copyright and source integrity

Do not commit music tracks, sampled copyrighted recordings, full lyrics, paywalled figures or unreleased personal sessions without documented permission. A CC label does **not** mean every use is allowed. Inspect each track license, attribution obligations, noncommercial restrictions, and redistribution rules. Metadata licenses may differ from audio licenses. Links and synthetic or owned audio are safer for public development.

## Research and participant protections

Public open-source collaboration is **not** the same as formal human-subjects research authorization. If a study collects identifiable responses or makes health-related claims, obtain appropriate institutional ethics review before recruitment. Seek explicit informed consent, minimize collection, allow opt-out, and avoid coercing personal disclosure. Do not recruit minors into emotional listening studies through this project.

## Scientific boundaries

Do not equate predicted sentiment, enjoyment, acoustic arousal, physiological synchronization, self-reported “felt understood,” and subjective consciousness. Different operationalizations need distinct tests. Beware culturally contingent emotion labels and overconfident personalization. Negative results belong in public reports without revealing individuals.

## Security

Never commit API keys, tracking pixels, external audio URLs containing secrets, or identifying file paths. Report vulnerabilities privately to the repository maintainers when feasible; GitHub issue threads are public.
