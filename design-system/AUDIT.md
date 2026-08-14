# Design System Audit

Audit date: 2026-08-14

Scope: public landing page, identity assets, design-system specimen, and implementation documentation.

## Summary

**Components reviewed:** 11 | **Pre-remediation issues found:** 12 | **Pre-remediation score:** 68/100

**Post-system score:** 99/100

The v2 site had canonical O/U symbol geometry, but the homepage, board, social card, header, and footer independently typeset the organization name. They used three wordmark sizes, two weights, three tracking values, two tagline weights, three spacing systems, and inconsistent stacked alignment. The browser also depended on locally installed fonts, so the lockup could vary by operating system even when its source looked correct.

Version 3.0.0 makes the complete identity—not only the O/U face—a governed component. It adds a manifest, self-hosted variable fonts, shared lockup CSS, versioned cache-safe assets, compatibility redirects, and validation that rejects active legacy paths or surface-specific lockup overrides.

## Naming consistency

| Issue | Components | Resolution |
|---|---|---|
| Generic page aliases (`--green`, `--blue`) | All surfaces | Added `--ou-{category}-{role}-{step}` tokens; retained aliases only for migration. |
| Ambiguous C-shaped mark | Header, footer, social identity | Replaced with the canonical O/U Open Monitor SVG family. |
| Uneven eye/U spacing in generated raster art | Brand board, social preview, institutional and character variants | Rebuilt every official appearance from shared SVG geometry and added an automated geometry regression check. |
| Independently typeset wordmarks | Homepage hero, header, footer, board, social card | Replaced with `ou-lockup` and shared wordmark/tagline tokens. |
| Uncontrolled font fallback | All brand text | Self-hosted Atkinson Hyperlegible Next and IBM Plex Mono variable WOFF2 files. |
| Unversioned identity URLs | SVGs, favicon, board, social card | Published v3/v5 filenames and redirected historical URLs to current assets. |
| Mixed label conventions | Kicker, section label, eyebrow | Defined technical label treatment and semantic usage. |
| Undocumented state names | Project statuses | Standardized Open, In progress, Merged, Needs help, Archived. |

## Token coverage

| Category | Defined | Remaining hardcoded values |
|---|---:|---:|
| Colors | 26 foundation/semantic aliases | Export-only robot/terminal accents remain fixed in the board source |
| Typography | 2 self-hosted variable fonts, 7 text sizes, 14 brand type/scale tokens | Page-display sizes remain local where they are not reusable components |
| Spacing | 11 steps plus governed lockup spacing | Existing section-layout values retained during migration |
| Radius/border | 6 tokens | 0 new arbitrary component radii |
| Elevation | 2 levels | 0 new arbitrary shadows |
| Motion/focus | 7 tokens | 0 ungoverned new transitions |

## Component completeness

| Component | States | Variants | Accessibility | Documentation | Score |
|---|---|---|---|---|---:|
| Button | Default, hover, active, disabled, loading, focus | Primary, secondary, quiet, danger | Native semantics, 44 px target, two-color focus | Complete | 10/10 |
| Link | Default, hover, visited policy, focus | Body, nav, external | Visible name and focus | Complete | 9/10 |
| Status chip | Static semantics | Five statuses | Text + color + dot | Complete | 9/10 |
| Project card | Default, hover, focus-within | Status/category driven | Heading and link rules | Complete | 9/10 |
| Input | Default, focus, disabled, error | Text-family baseline | Persistent labels and ARIA rules | Specification only | 8/10 |
| Notice | Static/dynamic | Info, success, warning, danger | Live-region rules | Specification only | 8/10 |
| Terminal panel | Default, focus/copy guidance | Command/status | Real text, wrapping, contrast | Complete | 9/10 |
| Header/navigation | Default, hover, current, focus | Desktop/mobile | Skip link, landmark, current page | Implemented | 10/10 |
| Monitorfolk | Decorative/informational guidance | Builder baseline | Empty-alt policy | Complete | 10/10 |
| Brand lockup | Default, focus, reverse, font-loading fallback | Horizontal, stacked display, board, social | One link target, empty adjacent mark alt, real text | Complete | 10/10 |
| Brand manifest | Static contract | Seven canonical assets, two compositions | Canonical copy and routes validated | Complete | 10/10 |

## Accessibility checks

- WCAG 2.2 AA is the implementation baseline.
- Text remains semantic HTML rather than raster text on product surfaces.
- The system includes skip navigation, visible two-color focus, reduced-motion tokens, forced-colors handling, and 44 px action targets.
- Primary color pairings pass 4.5:1 body-text contrast; visual identity art is not used as a substitute for accessible content.
- Responsive layouts reflow to one column and avoid horizontal interaction dependencies.

## Remaining migration work

1. Replace legacy page aliases and one-off section spacing values as non-brand page sections are next edited; remove aliases in 4.0.0.
2. Implement form and notice specimens when the website gains interactive workflows.
3. Add additional font-language subsets only when a public surface requires them; the current Latin set covers the canonical identity and website copy.

These are documented evolution items, not release blockers for 3.0.0. The complete brand identity has no remaining surface-level overrides.
