# INS-002 — Repair the broken iROI link and incorrect 404 metadata

Priority: P1  
Area: Internal navigation / calculator funnel / SEO  
Status: Production-confirmed

## Problem

The no-medical-exam article links “iROI calculator” to `/iroi-calculator/`, which returns HTTP 404. The live calculator is at `/life-insurance/life-insurance-investment-calculator/`.

The rendered 404 page also reports the document title “Coming Soon,” which contradicts the visible 404 content and weakens browser, analytics, and search diagnostics.

Evidence:

- `../screenshots/broken-iroi-404.png`
- `../data/internal-broken-links.csv`

## Reproduction

1. Open `https://insurancy.com/life-insurance/no-medical-exam-life-insurance/`.
2. Find the paragraph that links “iROI calculator.”
3. Click it.
4. Observe `https://insurancy.com/iroi-calculator/` and the 404 page.
5. Observe the browser title “Coming Soon.”

## Recommended fix

Update the article link to `/life-insurance/life-insurance-investment-calculator/`. Add a permanent redirect from `/iroi-calculator/` to the live calculator because the old path may already have backlinks. Give the 404 route accurate, consistent metadata.

## Acceptance criteria

- The article’s iROI link opens the live calculator with HTTP 200.
- `/iroi-calculator/` permanently redirects to the live calculator.
- The 404 document title is “Page Not Found | Insurancy” or equivalent.
- 404 Open Graph and canonical metadata do not claim the homepage URL.
- The production internal-link crawl reports zero broken internal links.

## Copy/paste implementation prompt

Fix the Insurancy iROI routing defect. Change the link on `/life-insurance/no-medical-exam-life-insurance/` from `/iroi-calculator/` to `/life-insurance/life-insurance-investment-calculator/`. Add a 308 permanent redirect from the old path to the live calculator. Correct the not-found route metadata so the title, description, canonical URL, Open Graph URL, and robots directives consistently describe a 404 page rather than “Coming Soon” or the homepage. Add route tests for the redirect, live destination, and 404 metadata, then run the site link checker.
