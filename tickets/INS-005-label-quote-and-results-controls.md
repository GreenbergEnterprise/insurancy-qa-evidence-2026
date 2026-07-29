# INS-005 — Add accessible names and selection state to quote controls

Priority: P1  
Area: Quote funnel / accessibility / conversion  
Status: Production-confirmed

## Problem

The embedded quote form exposes eight `<select>` elements without `id`, `name`, `aria-label`, or `aria-labelledby`. Their accessibility-tree role is simply “combobox” with no name. The results page also has visible coverage, term, and payment selects without accessible names.

Multi-select quiz choices visually change state but do not expose `aria-pressed`, `aria-selected`, or a checked state.

This makes the most valuable funnel difficult or impossible to complete reliably with screen readers, voice control, or automated assistive input.

Evidence:

- `../screenshots/mobile-quote-fields-390x844.png`
- `../screenshots/desktop-policy-quiz-step2.png`
- Browser inspection confirmed eight unnamed quote-form selects and six visible unnamed results selects.

## Recommended fix

Use real `<label for>` associations for every select and input. Give segmented choice buttons `aria-pressed` or implement native radio/checkbox controls. Ensure the visible selected state and programmatic state always match.

## Acceptance criteria

- Every visible form control has a unique accessible name.
- Date fields are announced as month, day, and year.
- Height fields are announced as feet and inches.
- Coverage, term, payment frequency, state, and health controls are distinguishable.
- Toggle/multi-select choices expose selected state.
- Keyboard-only users can complete the quote and quiz.
- Axe or equivalent automated checks pass on quote entry, quiz, results, and application start.
- Screen-reader smoke tests cover the full no-contact quote path.

## Copy/paste implementation prompt

Perform an accessibility remediation of the Insurancy quote entry, policy-type quiz, results filters, and application start. Add explicit `<label for>`/`id` associations for every input and select, including date month/day/year, state, height feet/inches, weight, coverage amount, term, and payment mode. For visual choice buttons, expose state with native radio/checkbox controls or correct `aria-pressed`/`aria-checked` semantics. Preserve existing styling. Add automated accessibility tests and keyboard-flow tests, then manually verify with a screen reader that the anonymous quote can be completed without guessing any control.
