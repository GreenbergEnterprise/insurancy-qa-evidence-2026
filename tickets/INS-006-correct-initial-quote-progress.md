# INS-006 — Correct the quote form’s initial “3/4 complete” progress

Priority: P2  
Area: Quote funnel / trust / form UX  
Status: Production-confirmed

## Problem

On a fresh quote form, before the visitor answers a question, the progress indicator says “3/4 complete.” Required state, gender, tobacco, and health-class decisions remain unanswered. The progress display implies near completion even though substantial work remains.

Evidence:

- `../screenshots/mobile-quote-form-centered-390x844.png`

## Recommended fix

Calculate progress from required questions the visitor has intentionally completed. Do not count placeholder/default values as user completion unless those defaults are explicitly accepted.

## Acceptance criteria

- A fresh form starts at an accurate percentage or step count.
- Placeholder values do not count as complete.
- Progress increases monotonically as required answers are provided.
- Switching quote type recalculates required questions correctly.
- Returning-session persistence is visually distinguished from untouched defaults.
- Unit tests cover fresh, partial, complete, restored, and changed-quote-type states.

## Copy/paste implementation prompt

Fix the progress calculation in the embedded Insurancy quote box. Identify which fields currently cause a fresh form to display `3/4 complete`. Define completion from required user-confirmed answers rather than populated defaults or placeholders. Keep progress synchronized when quote type changes and when a saved session is restored. Add unit tests for fresh, partially completed, fully completed, and restored states, plus a 390px visual regression showing an accurate initial indicator.
