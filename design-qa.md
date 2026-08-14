# Openly Useful Design QA

QA date: 2026-08-14

System version: 3.0.0
Scope: homepage, public design-system specimen, institutional/reverse/character marks, complete lockups, production brand board, social card, favicon, Monitorfolk, typography, cache behavior, and compatibility routes.

## Source and implementation inputs

- Approved composition source: the 1536 × 1024 v2 production board at commit `f42e47f`.
- Pre-remediation homepage capture: `/tmp/openly-useful-home-brand-audit.webp` at 1440 × 1000.
- Pre-remediation board capture: `/tmp/openly-useful-board-brand-audit.webp` at 1536 × 1024.
- Post-remediation homepage capture: `/tmp/openly-useful-home-brand-v3.webp` at 1440 × 1000.
- Post-remediation mobile capture: `/tmp/openly-useful-home-brand-v3-mobile.webp` at 390 × 844.
- Post-remediation board capture: `/tmp/openly-useful-board-brand-v3.webp` at 1536 × 1024.
- Post-remediation social capture: `/tmp/openly-useful-social-brand-v3.webp` at 1200 × 630.
- Public component capture: `/tmp/openly-useful-lockup-specimen-v3.webp` at 1280 × 900.
- Mobile component capture: `/tmp/openly-useful-design-system-v3-mobile.webp` at 390 × 844.

## Findings and corrections

| Priority | Finding | Correction | Post-fix evidence |
|---|---|---|---|
| P0 | The same symbol was paired with independently defined wordmarks across the homepage, board, social card, header, and footer. Weight, tracking, width, spacing, tagline weight, scale ratio, and alignment differed. | Introduced one `ou-lockup` component with horizontal and stacked variants. Moved all internal typography and spacing into shared tokens and `brand.css`. | Homepage and board now produce the same 336 px mark, 88 px/780 wordmark, 22 px/700 tagline, tracking, line height, optical width, and vertical spacing. |
| P1 | The declared brand fonts were not delivered, so the wordmark changed with the viewer's installed fonts and operating system. | Self-hosted the official Atkinson Hyperlegible Next and IBM Plex Mono variable WOFF2 files with their OFL licenses. | Browser font checks return `true` for both families on every verified surface. |
| P1 | Unversioned SVG and raster paths could mix a newly deployed page with a stale cached asset. | Published v3 symbol routes, a v3 favicon/board, and `og-v5.png`; redirected historical routes to the current equivalents. | Active surfaces contain no deprecated routes; compatibility redirects are release-validated. |
| P1 | Old Open Shell and early social assets were treated as required top-level production files. | Moved them to `brand/archive/pre-v3/` and removed them from the active asset contract. | The manifest contains only current assets; validation rejects archived paths in active surfaces. |
| P1 | The homepage Monitorfolk face was aligned by eye but did not reuse the exact canonical face proportions; its square SVG was also stretched to a non-square rendered box. | Replaced the custom face with a uniformly scaled canonical eye/U group and enforced `height:auto` wherever the character renders. | Geometry validation proves the same source coordinates and path; browser QA reports a square, undistorted render. |
| P2 | The design-system page documented a lockup but did not expose a reusable implementation contract. | Added a live component specimen, variants, properties, states, accessibility rules, usage guidance, and architecture document. | Public specimen renders four governed lockups and exact 16/20/34/64 px optical samples. |

## Cross-surface dimensional proof

Desktop homepage and board use the same `board/display` maximum unit. Browser rounding is the only measured delta.

| Element | Homepage | Brand board | Delta |
|---|---:|---:|---:|
| Institutional mark | 335.98 px | 336.00 px | 0.02 px |
| Wordmark visual width | 704.07 px | 704.11 px | 0.04 px |
| Wordmark font/weight | 88 px / 780 | 88 px / 780 | 0 |
| Wordmark tracking | -5.456 px | -5.456 px | 0 |
| Tagline visual width | 335.53 px | 335.61 px | 0.08 px |
| Tagline font/weight | 22 px / 700 | 22 px / 700 | 0 |

## Required fidelity surfaces

| Surface | Result | Evidence |
|---|---|---|
| Symbol geometry | Passed | Primary, reverse, character, favicon, and Monitorfolk geometry assertions pass. |
| Complete lockup | Passed | Every active name/mark pairing uses `ou-lockup`; no page may redefine lockup children. |
| Typography | Passed | Both official variable fonts load locally; weight, tracking, line height, and optical width are shared. |
| Canonical copy | Passed | Manifest, homepage, board, social card, and specimen use the exact name and tagline. |
| Desktop responsive behavior | Passed | No horizontal overflow at 1440 × 1000, 1280 × 900, 1536 × 1024, or 1200 × 630. |
| Mobile responsive behavior | Passed | No horizontal overflow at 390 × 844; the 352.03 px wordmark remains inside the 362 px hero width. |
| Small-size rendering | Passed | Optical specimens measure exactly 16, 20, 34, and 64 CSS pixels. |
| Asset loading | Passed | No eagerly loaded image failures on the homepage, board, social card, or design-system page. |
| Console | Passed | No browser console errors or warnings across the verified homepage, board, social card, and design-system views. |
| Raster exports | Passed | Board is a real 1536 × 1024 PNG; social card is a real 1200 × 630 PNG. |
| Accessibility | Passed | Linked lockups are one named focus target; adjacent symbols have empty alt text; web taglines remain real text. |
| Release governance | Passed | Manifest, brand-system, geometry, site, and compatibility-route checks are part of the release gate. |

## Final result

passed
