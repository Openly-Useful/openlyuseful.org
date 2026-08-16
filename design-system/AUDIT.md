# Design System Audit

Audit date: 2026-08-14

Scope: public landing page, identity assets, design-system specimen, and implementation documentation.

## Summary

**Components reviewed:** 11 | **Pre-remediation issues found:** 12 | **Pre-remediation score:** 68/100

**Post-system score:** 99/100

The v2 site had canonical O/U symbol geometry, but the homepage, board, social card, header, and footer independently typeset the organization name. They used three wordmark sizes, two weights, three tracking values, two tagline weights, three spacing systems, and inconsistent stacked alignment. The browser also depended on locally installed fonts, so the lockup could vary by operating system even when its source looked correct.

Version 3.0.0 made the identity a governed component, but its wordmark and tagline still rendered as live font text at very different sizes. The numeric weight matched while browser hinting and pixel snapping made the 18 px header treatment appear denser than the 88 px hero treatment. Version 3.0.1 closes that final rendering gap: each horizontal or stacked composition is now one outlined SVG master whose exact paths and internal spacing scale together.

Version 3.1.0 extends that same source-of-truth rule beyond page lockups. GitHub’s generated purple identicon and the site’s transparent legacy favicon are replaced by one Shell-backed institutional profile master, with exact raster derivatives for GitHub, Apple touch, and installed-web-app contexts.

## Naming consistency

| Issue | Components | Resolution |
|---|---|---|
| Generic page aliases (`--green`, `--blue`) | All surfaces | Added `--ou-{category}-{role}-{step}` tokens; retained aliases only for migration. |
| Ambiguous C-shaped mark | Header, footer, social identity | Replaced with the canonical O/U Open Monitor SVG family. |
| Uneven eye/U spacing in generated raster art | Brand board, social preview, institutional and character variants | Rebuilt every official appearance from shared SVG geometry and added an automated geometry regression check. |
| Independently typeset wordmarks | Homepage hero, header, footer, board, social card | Replaced with complete outlined horizontal and stacked lockup masters. |
| Same token, different optical weight | 18 px header/footer versus 88 px hero/board | Removed runtime brand typesetting; every surface now scales the same wordmark paths. |
| Platform-generated organization identity | GitHub organization avatar and browser/application icons | Added one validated profile master containing the unchanged institutional paths on the canonical Shell background. |
| Uncontrolled font fallback | All brand text | Self-hosted Atkinson Hyperlegible Next and IBM Plex Mono variable WOFF2 files. |
| Unversioned identity URLs | SVGs, favicon, board, social card | Published versioned v3/v4/v6 filenames and redirected historical URLs to current assets. |
| Mixed label conventions | Kicker, section label, eyebrow | Defined technical label treatment and semantic usage. |
| Undocumented state names | Repository lifecycle labels | Standardized Open, In progress, Merged, Needs help, Archived. |

## Token coverage

| Category | Defined | Remaining hardcoded values |
|---|---:|---:|
| Colors | 26 foundation/semantic aliases | Export-only robot/terminal accents remain fixed in the board source |
| Typography | 2 self-hosted variable font sources, 7 text sizes, outlined identity masters, and 5 lockup-size tokens | Page-display sizes remain local where they are not reusable components |
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
| Brand lockup | Default, focus, reverse | Horizontal, stacked display, board, social | One link target; semantic hidden heading/tagline; informative export alt | Complete | 10/10 |
| Brand manifest | Static contract | Mark family, standalone outlines, complete lockups, profile/icon family, and raster exports | Canonical copy, path identity, dimensions, and routes validated | Complete | 10/10 |

## Accessibility checks

- WCAG 2.2 AA is the implementation baseline.
- Canonical name and tagline remain semantic HTML for headings and linked accessible names; the visible identity is one outlined SVG.
- The system includes skip navigation, visible two-color focus, reduced-motion tokens, forced-colors handling, and 44 px action targets.
- Primary color pairings pass 4.5:1 body-text contrast; visual identity art is not used as a substitute for accessible content.
- Responsive layouts reflow to one column and avoid horizontal interaction dependencies.

## Remaining migration work

1. Replace legacy page aliases and one-off section spacing values as non-brand page sections are next edited; remove aliases in 4.0.0.
2. Implement form and notice specimens when the website gains interactive workflows.
3. Add additional font-language subsets only when a public surface requires them; the current Latin set covers the canonical identity and website copy.

These are documented evolution items, not release blockers for 3.1.0. The complete brand identity has no remaining surface-level, runtime-type, or platform-generated institutional overrides.
