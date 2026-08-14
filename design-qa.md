# Openly Useful Design QA

QA date: 2026-08-13  
Scope: official O/U Open Monitor family, production brand board, social card, public landing page, and design-system specimen.

## Comparison setup

- Source visual truth: user-selected brand board at `f044059:brand/brandkit-open-monitor.png`; the user's focused defect capture was also reviewed at its supplied 590 × 1248 dimensions.
- Implementation visual truth: `brand/brandkit-open-monitor.png`, rendered by the browser from `brand/brandkit.html` and the canonical SVG files.
- Full implementation capture: `/tmp/openly-useful-design-qa/implementation-brandkit-pass2.png`.
- Full combined comparison: `/tmp/openly-useful-design-qa/brandkit-comparison-pass2.png`.
- Focused combined comparison: `/tmp/openly-useful-design-qa/brandkit-focused-comparison.png`.
- Full comparison viewport: 1536 × 560 CSS pixels at 1× density; source and implementation were each normalized from 1536 × 1024.
- Focused comparison viewport: 1536 × 560 CSS pixels at 1× density.
- State: default light brand presentation, no hover, focus, loading, or reduced-motion state.

The source and implementation were reviewed together in both the full-board and focused institutional/character comparisons. The focused comparison was required because the eye-to-U clearance was too small to judge reliably from a reduced full-board view.

## Finding history

| Priority | Finding | Fix | Post-fix evidence |
|---|---|---|---|
| P1 | The generated source independently redrew the institutional and character faces. Square U stroke caps created visible notches and inconsistent eye-to-U spacing. | Replaced stroked U shapes with one filled canonical path; aligned eye centers to the U stems; rebuilt production raster layouts from the canonical SVGs. | Focused combined comparison shows continuous eye blocks, a four-unit eye/U gap, and equal left/right alignment in both variants. `scripts/validate_brand_geometry.py` passes. |
| P1 | The Monitorfolk starter used eye centers that did not match its U stem centers, and its square caps visually collapsed the gap. | Moved the U stems to the exact eye centerlines and used butt caps so stroke extension cannot invade the gap. | Automated bot geometry assertions pass. |
| P2 | The first production-board pass undersized the wordmark relative to the selected source. | Increased and rebalanced the real-text wordmark while retaining accessible, non-raster typography on the live product. | The second full-board comparison matches the source hierarchy and left-column visual weight. |
| P2 | Earlier browser exports had JPEG bytes behind `.png` filenames. | Converted production and QA exports to real PNG encoding and added dimension/signature checks to release validation. | `file` identifies all three production exports as PNG; `scripts/validate_site.py` passes. |

## Required fidelity surfaces

| Surface | Result | Evidence |
|---|---|---|
| Logo geometry | Passed | Eye centerlines are x = 24 and x = 40; eye/U gap is 4 units; U/inner-counter gap is 2.5 units. The same construction is used by the primary, reverse, character, favicon, and Monitorfolk assets. |
| Typography | Passed | Brand hierarchy matches the selected board while product-facing text remains real text using the documented sans/mono stacks. |
| Spacing and composition | Passed | Brand board preserves the selected split composition and hierarchy; the lower construction area is intentionally normalized into repeatable system cards. |
| Color | Passed | Ink/Shell contrast is 15.83:1; Terminal-700/Shell contrast is 6.93:1. Both exceed WCAG AA for body text. |
| Image quality | Passed | Workshop imagery uses the approved source crop at its intended aspect ratio; official logos are never redrawn inside raster compositions. |
| Copy | Passed | Organization name and the exact tagline, “Useful things, openly made.”, are consistent. |
| Responsive behavior | Passed | Landing page and design-system page have no horizontal overflow at 1440 × 1000, 1280 × 900, or 390 × 844. |
| Icon sizing | Passed | Optical specimens render at exactly 16, 20, 34, and 64 CSS pixels. The 16 px size is favicon-only; 20 px is the minimum general digital mark. |
| Asset loading | Passed | Browser checks reported no broken images across the landing page, design-system page, brand board, or comparison views. |
| Console | Passed | Browser console reported no errors or warnings in the verified views. |
| Release validation | Passed | `python3 scripts/validate_site.py` and the nested brand geometry validator both pass. |

## Intentional differences from the generated source

- AI-rendered lettering was replaced with real, selectable typography.
- The lower construction area was made more systematic and scannable.
- Official institutional and character marks use exact production colors rather than the source raster's approximate black/green treatment.

These differences improve production reliability without changing the approved visual direction.

## Final result

passed
