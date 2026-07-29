# INS-004 — Stop the Ameritas logo from opening the Ethos review

Priority: P1  
Area: Homepage trust / carrier navigation  
Status: Production-confirmed

## Problem

The homepage carrier carousel presents an Ameritas logo, but its link target is `/life-insurance/reviews/ethos-life-insurance-review/`. Clicking Ameritas opens the Ethos review.

No working Ameritas review route was found at the obvious published paths, so linking to a guessed Ameritas URL would create another 404.

Evidence:

- DOM link: accessible name `Ameritas`, `href="/life-insurance/reviews/ethos-life-insurance-review/"`
- `../screenshots/ameritas-logo-source.png`
- `../screenshots/ameritas-logo-wrong-destination.png`

## Reproduction

1. Open `https://insurancy.com/`.
2. In the carrier logo carousel, click Ameritas.
3. Observe the “Ethos Life Insurance Review” destination.

## Recommended fix

Correct the carrier data mapping. If a production Ameritas review exists, use its canonical route. Otherwise, make the logo non-clickable or send it to a neutral carrier directory until the review exists.

## Acceptance criteria

- Ameritas never routes to Ethos.
- Every homepage carrier logo maps to the matching carrier.
- Logo label, image alt text, href, analytics label, and destination H1 agree.
- A data-driven test iterates every carrier mapping and catches mismatches.

## Copy/paste implementation prompt

Find the data source that populates the Insurancy homepage carrier carousel. Correct the Ameritas entry, which currently uses the Ethos review URL. Do not invent an Ameritas route: first resolve the canonical production route from the repository or CMS. If no Ameritas page exists, remove the link behavior or route to the carrier directory. Add a test that renders every carrier entry and asserts the carrier name/alt text matches the destination slug or declared carrier ID. Verify the carousel on desktop and 390px mobile width.
