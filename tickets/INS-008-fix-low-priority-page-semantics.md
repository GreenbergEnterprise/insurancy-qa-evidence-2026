# INS-008 — Fix missing page and image semantics

Priority: P3  
Area: Accessibility / SEO / content hygiene  
Status: Production-confirmed

## Problem

The crawl found:

- One HTTP 200 page without an H1: `/brian-greenberg-virtual-card/`
- Nine pages with non-decorative images that have empty alt text
- One calculator page with an unlabeled select in server-rendered HTML

The full affected-page inventory is in `../data/production-audit.json`.

## Recommended fix

Add a single descriptive H1 to the virtual card, meaningful alt text to informative images, `aria-hidden="true"`/empty alt only for decorative images, and an explicit label for the calculator select.

## Acceptance criteria

- Every indexable content page has one meaningful H1.
- Informative images have concise contextual alt text.
- Decorative images are explicitly hidden from assistive technology.
- The iROI calculator select has a unique label.
- Automated semantic checks pass across the production route set.

## Copy/paste implementation prompt

Remediate the low-priority semantic findings in the Insurancy crawl. Add a meaningful H1 to `/brian-greenberg-virtual-card/`. Review every image listed under `pages_with_missing_alt_images` in `production-audit.json`: add concise alt text when the image communicates information, or mark it decorative with empty alt plus `aria-hidden="true"`. Add an explicit programmatic label to the unlabeled select on `/life-insurance/life-insurance-investment-calculator/`. Add automated checks for missing H1s, unlabeled visible controls, and informative images without alt text.
