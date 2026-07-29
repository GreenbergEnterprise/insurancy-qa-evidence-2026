# Insurancy production conversion QA

Audit date: July 29, 2026  
Target: `https://insurancy.com/`  
Method: live browser testing plus a bounded production crawl  
Result: core quote flow works, but eight ticket-ready defects were confirmed

## Executive summary

The highest-value anonymous quote journey successfully reached carrier results and the application contact step. No real lead was submitted.

The most important production defects are:

1. Three legacy product-specific quote links open 404 pages in new tabs.
2. An internal iROI calculator link returns 404.
3. Zero-cent quote prices render as malformed values such as `$22.`.
4. The Ameritas homepage logo opens the Ethos review.
5. Quote and result controls lack accessible names and selected-state semantics.

## Coverage

### Browser journeys

- Desktop homepage at 1280×720
- Mobile homepage, navigation, and submenu at 390×844
- Primary anonymous quote entry
- Synthetic quote through live carrier results
- Quote result to application contact step
- Policy-type quiz from step 1 to step 2
- Full assessment from step 1 to step 2
- All 12 homepage-linked `rates.insurancy.com` quiz and quote routes
- Broken internal iROI path
- Legacy guaranteed-issue quote path
- Homepage carrier carousel

### Crawl

- 299 sitemap seeds
- 1,400 fetched production URLs
- 39,380 internal link instances
- 1,417 unique internal targets discovered
- 1,377 HTTP 200 pages
- 22 permanent redirects
- 1 internal HTTP 404
- 379 unique external destinations checked
- 30 unique external destinations returned 404 across 52 link instances

The 17-target difference between discovered and fetched internal URLs is generated testimonial/review filter pagination such as `?stars=5&sort=oldest&page=11`. That space keeps producing further combinations, so the audit bounded it at 1,400 URLs. All sitemap pages and primary conversion routes are included.

External 401, 403, 429, and network/SSL failures are retained in the raw JSON but are not classified as dead links. The browser proved that several bot-blocked `rates.insurancy.com` routes work for real users.

## Findings

| Ticket | Priority | Finding | Conversion impact |
|---|---:|---|---|
| [INS-001](tickets/INS-001-fix-legacy-quote-404s.md) | P0 | Legacy guaranteed-issue, final-expense, and accidental-death quote links open 404 pages | Direct loss of high-intent visitors |
| [INS-002](tickets/INS-002-fix-iroi-broken-link-and-404-metadata.md) | P1 | No-medical-exam article links to a missing iROI route; 404 title says “Coming Soon” | Broken calculator journey and weak diagnostics |
| [INS-003](tickets/INS-003-fix-truncated-zero-cent-prices.md) | P1 | Banner Life premium displays as `$22.` | Damages pricing credibility at the decision point |
| [INS-004](tickets/INS-004-fix-ameritas-logo-misroute.md) | P1 | Ameritas logo routes to the Ethos review | Trust and carrier-navigation failure |
| [INS-005](tickets/INS-005-label-quote-and-results-controls.md) | P1 | Quote and result selects are unnamed; choice state is not announced | Assistive-technology users may abandon the funnel |
| [INS-006](tickets/INS-006-correct-initial-quote-progress.md) | P2 | Fresh quote form reports “3/4 complete” before required answers | Confusing and potentially misleading progress |
| [INS-007](tickets/INS-007-clean-up-external-404-links.md) | P2 | 30 unique external 404 targets across 52 link instances | Content credibility and SEO degradation |
| [INS-008](tickets/INS-008-fix-low-priority-page-semantics.md) | P3 | Missing H1, missing image alt text, and one server-rendered unlabeled select | Accessibility and content hygiene |

The compact task list is in [tickets.csv](tickets.csv). Every ticket includes reproduction steps, acceptance criteria, and a standalone implementation prompt.

## What passed

- Homepage had no horizontal overflow at 390px.
- Mobile menu and Life Insurance submenu opened correctly.
- All 12 homepage-linked quiz/quote routes loaded their first interactive step.
- The policy-type quiz advanced from “What are your goals?” to “How old are you?”
- The full assessment advanced from state to date of birth.
- A synthetic anonymous quote produced live Corebridge and Banner Life results.
- The most-affordable result opened a complete application-start page.
- Policy details carried correctly into the application.
- The application contact fields rendered at 390px without horizontal overflow.
- No real name, email, phone number, payment, application, or lead was submitted.

## Screenshot evidence

### Baselines

- [Desktop homepage hero](screenshots/desktop-home-hero.png)
- [Mobile homepage](screenshots/mobile-home-390x844.png)
- [Mobile menu](screenshots/mobile-menu-open-390x844.png)
- [Mobile Life Insurance submenu](screenshots/mobile-life-menu-open-390x844.png)

### Quote and application journey

- [Mobile quote form and initial 3/4 progress](screenshots/mobile-quote-form-centered-390x844.png)
- [Mobile quote fields](screenshots/mobile-quote-fields-390x844.png)
- [Quote results popup](screenshots/quote-results-popup-441x897.png)
- [Malformed Banner Life price](screenshots/mobile-banner-price-format.png)
- [Policy-type quiz step 2](screenshots/desktop-policy-quiz-step2.png)
- [Application policy summary](screenshots/mobile-application-start-390x844.png)
- [Application contact fields](screenshots/mobile-application-contact-form-390x844.png)

### Defects

- [Broken iROI destination](screenshots/broken-iroi-404.png)
- [Legacy guaranteed-issue source link](screenshots/legacy-quote-source-cancer.png)
- [Legacy quote 404](screenshots/broken-legacy-quote-404.png)
- [Ameritas logo on the homepage](screenshots/ameritas-logo-source.png)
- [Ethos destination after clicking Ameritas](screenshots/ameritas-logo-wrong-destination.png)

## Data and scripts

- [Complete production audit JSON](data/production-audit.json)
- [Internal broken-link CSV](data/internal-broken-links.csv)
- [External 404 CSV](data/external-404-links.csv)
- [Rate-funnel smoke JSON](data/rate-funnel-smoke.json)
- [Rate-funnel smoke CSV](data/rate-funnel-smoke.csv)
- [Reusable crawler](scripts/site_qa_audit.py)
- [Evidence-table builder](scripts/build_audit_tables.py)

Run from this audit directory:

```bash
python3 scripts/site_qa_audit.py \
  --base-url https://insurancy.com/ \
  --sitemap https://insurancy.com/sitemap.xml \
  --max-pages 1400 \
  --max-external 1000 \
  --workers 24 \
  --timeout 20 \
  --output data/production-audit.json

python3 scripts/build_audit_tables.py
```

The crawler intentionally exits nonzero when a broken internal link is present.

## Evidence limits

- The browser surface supported screenshots but not a real session video recording. No synthetic “video” was generated or presented as real interaction evidence.
- The 1280×7439 full-page homepage capture showed stitching artifacts from fixed/animated content and is excluded from findings.
- External bot blocks are inconclusive unless manually reproduced in a normal browser.
- The audit stopped before the application’s final Submit action to avoid creating a fake lead or transmitting contact data.
