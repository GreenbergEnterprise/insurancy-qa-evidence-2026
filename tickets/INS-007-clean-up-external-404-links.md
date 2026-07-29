# INS-007 — Repair or remove confirmed external 404 links

Priority: P2  
Area: Content quality / trust / SEO  
Status: Production-confirmed

## Problem

The first production pass found 30 unique external destinations returning HTTP 404. Some targets are repeated across multiple articles. These include retired Insurance Information Institute URLs, old government/citation URLs, expired partner pages, and three revenue links handled separately in INS-001.

Complete evidence:

- `../data/external-404-links.csv`

Bot-blocked 401/403/429 responses are not included in this ticket because those are inconclusive from automation.

## Recommended fix

For each CSV row, find the current authoritative replacement URL. If no equivalent source exists, remove or rewrite the citation without weakening the factual claim. Keep revenue links in INS-001 as the first batch.

## Acceptance criteria

- Every CSV target is replaced, redirected, or intentionally removed.
- Replacement citations support the surrounding claim.
- No automated-bot 403 is treated as a dead link without manual confirmation.
- The external-link checker runs on a schedule and reports new 404/410 responses.
- Editorial owners receive source page, anchor text, target, and status.

## Copy/paste implementation prompt

Use the attached `external-404-links.csv` as the authoritative remediation queue for Insurancy content. For each source page and anchor, locate the current authoritative replacement URL, update the content, and preserve the meaning of the surrounding claim. Prioritize revenue links and government/primary sources. Remove links only when no defensible replacement exists. Do not classify 401, 403, or 429 bot responses as broken without manual browser verification. Add an external-link check that records source page, anchor text, target, final URL, and HTTP status.
