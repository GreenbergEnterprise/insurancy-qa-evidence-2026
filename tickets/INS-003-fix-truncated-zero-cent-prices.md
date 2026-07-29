# INS-003 — Render zero-cent quote prices with two decimal places

Priority: P1  
Area: Quote results / pricing trust  
Status: Production-confirmed

## Problem

When a monthly premium has zero cents, the results UI renders the Banner Life price as `$22.` rather than `$22.00`. The malformed price appears both in the recommended card and the results list.

Evidence:

- `../screenshots/mobile-banner-price-format.png`
- Synthetic quote used: Arizona, male, DOB 01/01/1986, 5′10″, 180 lb, preferred non-tobacco, $250,000 coverage, 20-year term.

## Reproduction

1. Run the synthetic quote above.
2. Open the results page.
3. Scroll to the Banner Life recommended result.
4. Observe `$22.` with no cents.

## Recommended fix

Centralize currency formatting and always render two fractional digits for USD. Do not concatenate integer, decimal point, and cents in separate branches that omit `"00"`.

## Acceptance criteria

- `22`, `22.0`, and `"22.00"` all render as `$22.00`.
- `21.91` renders as `$21.91`.
- Negative, null, missing, and non-numeric inputs have explicit safe behavior.
- Recommended cards and the full results list use the same formatter.
- Screen-reader text exposes the complete price, including cents.
- Unit and visual regression tests include a zero-cent premium.

## Copy/paste implementation prompt

Fix currency rendering in the Insurancy rate-results application. Find every premium formatter used by the recommended cards and the complete results list. Replace string concatenation or conditional cents rendering with one shared USD formatter, preferably `Intl.NumberFormat("en-US", { style: "currency", currency: "USD", minimumFractionDigits: 2, maximumFractionDigits: 2 })`. Ensure numeric and numeric-string API values normalize safely. Add unit tests for `22`, `22.0`, `"22.00"`, `21.91`, null, and invalid input, plus a visual regression proving the Banner Life card displays `$22.00`.
