# Public launch checklist — no additional paid services

This repository has a self-contained, static research homepage at **[index.html](index.html)** and a local-first interactive prototype at **[harbor-co-listener/index.html](harbor-co-listener/index.html)**. It does not require a framework, subscription or externally hosted JS.

## What has been done

- Created an accessible, mobile-responsive public research front door.
- Added machine-readable search/social description tags and links to reproducible research, issues, and the prototype.
- Added an automated Node smoke test with a public GitHub Actions workflow. **Workflow success must be checked in GitHub; merely committing the workflow is not a passed run.**
- Kept scientific status explicit: no confirmed personal hidden-pattern detection or AI audio understanding.

## One-time GitHub settings (repo administrator)

GitHub does not currently expose changing Pages, description or topics through our connected repository editing tools. These settings are **not changed by this commit**.

1. Open [repository settings → Pages](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/settings/pages). Under Build and deployment, select **Deploy from a branch**, branch **main**, directory **/(root)**; Save. After GitHub reports deployment, use the **Visit site** link. Do not advertise a live URL until checked. Public GitHub Pages is supported for public repos on GitHub Free.
2. Open the [repository About panel](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm) and use the gear icon. Suggested description: **“Open-source research at Chapin Road Farm: human–AI collaboration, music perception, personal listening, and reproducible experiments.”**
3. Suggested GitHub topics: \`human-ai-interaction\`, \`music-cognition\`, \`music-information-retrieval\`, \`open-research\`, \`audio-analysis\`, \`human-centered-ai\`. Topics are public and should describe actual work, not claim finished capabilities.
4. Confirm that the [Actions tab](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions) shows a passing **Public site smoke tests** run. Static tests don't replace device or external-link checks.

## After activation: external checks

- Visit the live site on a phone and desktop.
- Open the Listening Room through the homepage link; choose a *rights-cleared file*, mark a moment and verify private JSON export.
- Check VoiceOver, keyboard focus, readable text and contrast. These are pending real-device verification, not claims of certification.
- Check the Pages URL and add it as GitHub repository homepage when verified.
- Encourage first outside contributions with small, evidenced issues and PRs.

No analytics, trackers or external audio uploads are present in the homepage. GitHub Pages hosting has its own normal service logs. This checklist does not claim access to those logs.

## Status language

**Implemented** means code exists; **tested** means a named environment/receipt exists; **qualified** means predetermined gates passed; **scientifically confirmed** requires valid independent evidence. Don't confuse them.
