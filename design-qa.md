# Openly Useful Design QA

QA date: 2026-08-14

System version: 3.0.1
Scope: homepage, public design-system specimen, institutional/reverse/character marks, complete lockups, production brand board, social card, favicon, Monitorfolk, typography, cache behavior, and compatibility routes.

## Source and implementation inputs

- Approved composition source: the 1536 × 1024 v2 production board at commit `f42e47f`.
- Pre-remediation homepage capture: `/tmp/openly-useful-home-brand-audit.webp` at 1440 × 1000.
- Pre-remediation board capture: `/tmp/openly-useful-board-brand-audit.webp` at 1536 × 1024.
- Final outlined-lockup homepage capture: `/tmp/ou-v4-preview.bs3M39/home.png` at 1440 × 1000.
- Final outlined-lockup mobile capture: `/tmp/ou-v4-home-mobile.png` at 390 × 844.
- Final board capture: `/tmp/ou-v4-preview.bs3M39/board.png` at 1536 × 1024.
- Final social capture: `/tmp/ou-v4-preview.bs3M39/og.png` at 1200 × 630.

## Findings and corrections

| Priority | Finding | Correction | Post-fix evidence |
|---|---|---|---|
| P0 | The same symbol was paired with independently defined wordmarks across the homepage, board, social card, header, and footer. Weight, tracking, width, spacing, tagline weight, scale ratio, and alignment differed. | Introduced governed horizontal and stacked lockup variants. | Every active mark/name pairing uses one of the two approved compositions. |
| P0 | Version 3.0.0 assigned the same `780` token everywhere but left the wordmark as live text. At 18 px, browser hinting and pixel snapping made the header look heavier than the 88 px hero. | Converted the canonical name and tagline to outlines and precomposed the complete horizontal and stacked SVGs. Runtime CSS now scales the whole asset and cannot typeset, space, or transform its children. | Validation proves that the same 13 wordmark paths are embedded in every light/reverse horizontal and stacked master; none contains an SVG `<text>` element or live visual logo text. |
| P1 | The declared brand fonts were not delivered, so the wordmark changed with the viewer's installed fonts and operating system. | Self-hosted the official Atkinson Hyperlegible Next and IBM Plex Mono variable WOFF2 files with their OFL licenses. | Browser font checks return `true` for both families on every verified surface. |
| P1 | Unversioned SVG and raster paths could mix a newly deployed page with a stale cached asset. | Published v4 outlined lockups, `brandkit-open-monitor-v4.png`, and `og-v6.png`; redirected historical routes to current equivalents. | Active surfaces contain no deprecated routes; compatibility redirects are release-validated. |
| P1 | Old Open Shell and early social assets were treated as required top-level production files. | Moved them to `brand/archive/pre-v3/` and removed them from the active asset contract. | The manifest contains only current assets; validation rejects archived paths in active surfaces. |
| P1 | The homepage Monitorfolk face was aligned by eye but did not reuse the exact canonical face proportions; its square SVG was also stretched to a non-square rendered box. | Replaced the custom face with a uniformly scaled canonical eye/U group and enforced `height:auto` wherever the character renders. | Geometry validation proves the same source coordinates and path; browser QA reports a square, undistorted render. |
| P2 | The design-system page documented a lockup but did not expose a reusable implementation contract. | Added a live component specimen, variants, properties, states, accessibility rules, usage guidance, and architecture document. | Public specimen renders four governed lockups and exact 16/20/34/64 px optical samples. |

## Cross-surface dimensional proof

Desktop homepage and board scale the same stacked SVG `viewBox`. Browser rounding is the only measured delta.

| Element | Homepage | Brand board | Delta |
|---|---:|---:|---:|
| Complete stacked lockup width | 705.563 px | 705.609 px | 0.046 px |
| Complete stacked lockup height | 481.594 px | 481.625 px | 0.031 px |
| Wordmark outline paths | 13 | 13 | 0; exact path-data match |
| Tagline outline paths | 27 | 27 | 0; exact path-data match |
| Stacked master viewBox | 8400.113 × 5733.643 | 8400.113 × 5733.643 | 0 |

## Required fidelity surfaces

| Surface | Result | Evidence |
|---|---|---|
| Symbol geometry | Passed | Primary, reverse, character, favicon, and Monitorfolk geometry assertions pass. |
| Complete lockup | Passed | Every active name/mark pairing scales a complete v4 SVG; no page contains lockup children to redefine. |
| Typography | Passed | Logo weight, tracking, and optical width are fixed paths. Self-hosted fonts remain available for interface typography and reproducible generation. |
| Canonical copy | Passed | Manifest, homepage, board, social card, and specimen use the exact name and tagline. |
| Desktop responsive behavior | Passed | No horizontal overflow at 1440 × 1000, 1280 × 900, 1536 × 1024, or 1200 × 630. |
| Mobile responsive behavior | Passed | No horizontal overflow at 390 × 844; the complete stacked asset is 352.797 × 240.797 px inside the 362 px hero width. |
| Small-size rendering | Passed | Optical specimens measure exactly 16, 20, 34, and 64 CSS pixels. |
| Asset loading | Passed | No eagerly loaded image failures on the homepage, board, social card, or design-system page. |
| Console | Passed | No browser console errors or warnings across the verified homepage, board, social card, and design-system views. |
| Raster exports | Passed | Board is a real 1536 × 1024 PNG; social card is a real 1200 × 630 PNG. |
| Accessibility | Passed | Linked lockups are one named focus target; the homepage preserves a semantic `h1` and tagline as visually hidden text; informative specimens provide exact alternative text. |
| Release governance | Passed | Manifest, brand-system, geometry, site, and compatibility-route checks are part of the release gate. |

## Final result

passed
