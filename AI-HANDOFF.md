# Insurancy production QA — AI agent handoff

This public evidence snapshot was created July 29, 2026.

## Entry points

- Repository: `https://github.com/GreenbergEnterprise/insurancy-qa-evidence-2026`
- Full report: `https://raw.githubusercontent.com/GreenbergEnterprise/insurancy-qa-evidence-2026/main/report/production-qa-report.md`
- Machine-readable manifest: `https://raw.githubusercontent.com/GreenbergEnterprise/insurancy-qa-evidence-2026/main/manifest.json`
- Complete evidence ZIP: `https://github.com/GreenbergEnterprise/insurancy-qa-evidence-2026/releases/download/v2026.07.29/insurancy-qa-evidence.zip`
- Compact ticket queue: `https://raw.githubusercontent.com/GreenbergEnterprise/insurancy-qa-evidence-2026/main/tickets/tickets.csv`
- Complete crawl evidence: `https://raw.githubusercontent.com/GreenbergEnterprise/insurancy-qa-evidence-2026/main/data/production-audit.json`

## Objective

Fix the eight production-confirmed defects in priority order without regressing the anonymous quote journey:

1. `INS-001` — replace retired legacy quote links that open 404 pages.
2. `INS-002` — repair the broken iROI link, redirect the old route, and correct 404 metadata.
3. `INS-003` — render zero-cent premium prices with two decimal places.
4. `INS-004` — stop the Ameritas logo from opening the Ethos review.
5. `INS-005` — label quote/results controls and expose programmatic selection state.
6. `INS-006` — correct the fresh quote form’s `3/4 complete` state.
7. `INS-007` — repair or remove the confirmed external 404 inventory.
8. `INS-008` — remediate lower-priority H1, image-alt, and select-label semantics.

Each Markdown ticket under `tickets/` contains production evidence, reproduction steps, a recommended fix, acceptance criteria, and a copy/paste implementation prompt.

## Verification boundaries

- A synthetic anonymous quote reached live carrier results and application start.
- No real lead, name, email, phone number, payment, or final application was submitted.
- External 401, 403, 429, SSL, and bot-blocked results are not confirmed dead links.
- No real session video was available; do not present a synthetic animation as original session evidence.
- Two misleading debug or stitched screenshots were excluded.

## Suggested workflow

Use one ticket per implementation branch. Preserve the ticket ID in commits and pull requests. After each fix:

1. reproduce the original failure;
2. implement the smallest durable correction;
3. add the ticket’s automated checks;
4. repeat desktop and 390-pixel mobile smoke tests;
5. run internal or external link checks where applicable;
6. do not submit a real lead.
