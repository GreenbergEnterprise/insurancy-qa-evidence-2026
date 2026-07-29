# INS-001 — Replace legacy quote links that open 404 pages

Priority: P0  
Area: Revenue funnel / content migration  
Status: Production-confirmed

## Problem

At least three in-content quote links still point to retired `quote.insurancy.com` paths. A user clicks a product-specific insurance link, a new tab opens, and the new tab contains only “The page can’t be found” with no quote recovery CTA.

Confirmed examples:

- `/life-insurance/health-conditions/cancer/` → `https://quote.insurancy.com/quote/guaranteed/_issue`
- `/life-insurance/health-conditions/cancer/` → `https://quote.insurancy.com/quote/final_expense/`
- `/life-insurance/mortgage-life-insurance/` → `https://quote.insurancy.com/quote/accidental_death/`

Evidence:

- `../screenshots/legacy-quote-source-cancer.png`
- `../screenshots/broken-legacy-quote-404.png`
- `../data/external-404-links.csv`

## Reproduction

1. Open `https://insurancy.com/life-insurance/health-conditions/cancer/`.
2. Scroll to “Summary: Should You Get Life Insurance While You Have Cancer?”
3. Click “guaranteed issue life insurance.”
4. Observe a new tab at `quote.insurancy.com/quote/guaranteed/_issue`.
5. Observe “The page can’t be found.”

## Recommended fix

Replace every retired `quote.insurancy.com/quote/...` destination with the matching live `rates.insurancy.com/custom/quote/...` route or the central live quote page. Add a redirect at the legacy host as a safety net where infrastructure ownership permits.

## Acceptance criteria

- No published page links to a 404 on `quote.insurancy.com`.
- Guaranteed issue links open the live guaranteed-issue quote funnel.
- Final expense links open the live final-expense quote funnel.
- Accidental death links open the live accidental-death quote funnel.
- Legacy URLs return a permanent redirect to a working destination, if controllable.
- Automated link tests fail the build for any future `quote.insurancy.com` 4xx.

## Copy/paste implementation prompt

Audit the Insurancy codebase and content for all links whose host is `quote.insurancy.com`. Replace retired quote paths with the matching live quote funnels on `https://rates.insurancy.com/custom/quote/`: guaranteed issue → `/guaranteed/`, final expense → `/final-expense/`, and accidental death → `/accidental/`. Preserve user intent and analytics parameters. If legacy-host routing is in this repository, add permanent redirects from the old paths to the new paths. Add automated tests that crawl rendered internal content and fail when a revenue CTA returns 4xx. Verify the cancer and mortgage-life-insurance pages manually on desktop and 390px mobile width. Do not submit a real lead while testing.
