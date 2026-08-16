# Openly Useful

The public website for **Openly Useful**, an independent studio making thoughtful products and open-source tools.

**Useful things, openly made.**

This is a dependency-free static site deployed on one Vercel project with a host-aware two-domain architecture:

| Domain | Brand expression | Role |
|---|---|---|
| [`openlyuseful.com`](https://openlyuseful.com) | **Openly Useful Studio** | Products, partnerships, capabilities, and experiments |
| [`openlyuseful.org`](https://openlyuseful.org) | **Openly Useful Open Source** | Public projects, documentation, contribution, and the shared design system |

Both domains use the same canonical Open Monitor identity, Atkinson Hyperlegible Next and IBM Plex Mono type system, and Shell / Unix Ink / Terminal / Process foundations. The Studio page is the Ink-dominant inverse expression of that system; it does not introduce a second mark or palette.

Vercel conditionally rewrites the `.com` root, robots file, and sitemap to their Studio documents, then falls back to the corresponding Open Source documents for `.org`. The internal documents intentionally do not occupy `index.html`, `robots.txt`, or `sitemap.xml`, because Vercel gives the filesystem precedence over rewrites. `www` hosts permanently redirect to their matching apex domain.

## Identity system

- [`design-system/README.md`](design-system/README.md) documents strategy, tokens, components, patterns, accessibility, voice, and governance.
- [`design-system/tokens.css`](design-system/tokens.css) is the canonical implementation token source.
- [`design-system/brand.css`](design-system/brand.css) is the only supported sizing layer for the approved outlined lockup assets.
- [`design-system/ARCHITECTURE.md`](design-system/ARCHITECTURE.md) documents boundaries, validation flow, reliability, and trade-offs.
- [`brand/README.md`](brand/README.md) documents the Open Monitor O/U identity, Monitorfolk character language, asset rules, and approved brand-kit board.
- [`brand/manifest.json`](brand/manifest.json) is the machine-readable identity and asset contract.
- [`brand/media-kit.html`](brand/media-kit.html) is the public download index for social, press, and template assets.
- [`brand/studio/open-graph.html`](brand/studio/open-graph.html) is the additive Studio social-card source; it embeds the unchanged approved reverse lockup.
- [`brand/open-source/open-graph.html`](brand/open-source/open-graph.html) is the additive Open Source social-card source; it embeds the unchanged approved primary lockup.
- [`brand/social/manifest.json`](brand/social/manifest.json) records exact platform dimensions, safe areas, upload mappings, and generated-file hashes.
- [`scripts/build_brand_vectors.py`](scripts/build_brand_vectors.py) reproducibly converts the licensed source fonts into the canonical outlined wordmark, tagline, and lockups.
- [`scripts/build_brand_exports.py`](scripts/build_brand_exports.py) reproducibly assembles and rasterizes the complete social, press, document, presentation, and email export kit.
- [`brand/ou-profile-mark-v1.svg`](brand/ou-profile-mark-v1.svg) is the single institutional source for the GitHub organization avatar, browser favicon, touch icon, and installed-app icons.
- The live public specimen is available at [`/design-system`](https://openlyuseful.org/design-system); approved downloads are available at [`/brand/media-kit.html`](https://openlyuseful.org/brand/media-kit.html). These open-source identity resources remain canonical on `.org`.

## Local preview

Serve this directory with any static web server, for example `python3 -m http.server 3000`, then open `/open-source.html` or `/studio.html` directly. The public root/robots/sitemap split depends on Vercel host matching and must be verified on a deployed preview; Vercel does not evaluate `has` conditions in `vercel dev`.

## License

Website content and code are released under the MIT License unless otherwise noted.
