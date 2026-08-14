# Openly Useful

The public website for **Openly Useful**, an independent open-source collective building practical public tools, reusable infrastructure, and systems people can inspect, adapt, and improve.

**Useful things, openly made.**

This is a dependency-free static site deployed on Vercel. `openlyuseful.org` is the canonical domain and `openlyuseful.com` redirects to it.

## Identity system

- [`design-system/README.md`](design-system/README.md) documents strategy, tokens, components, patterns, accessibility, voice, and governance.
- [`design-system/tokens.css`](design-system/tokens.css) is the canonical implementation token source.
- [`design-system/brand.css`](design-system/brand.css) is the only supported sizing layer for the approved outlined lockup assets.
- [`design-system/ARCHITECTURE.md`](design-system/ARCHITECTURE.md) documents boundaries, validation flow, reliability, and trade-offs.
- [`brand/README.md`](brand/README.md) documents the Open Monitor O/U identity, Monitorfolk character language, asset rules, and approved brand-kit board.
- [`brand/manifest.json`](brand/manifest.json) is the machine-readable identity and asset contract.
- [`brand/media-kit.html`](brand/media-kit.html) is the public download index for social, press, and template assets.
- [`brand/social/manifest.json`](brand/social/manifest.json) records exact platform dimensions, safe areas, upload mappings, and generated-file hashes.
- [`scripts/build_brand_vectors.py`](scripts/build_brand_vectors.py) reproducibly converts the licensed source fonts into the canonical outlined wordmark, tagline, and lockups.
- [`scripts/build_brand_exports.py`](scripts/build_brand_exports.py) reproducibly assembles and rasterizes the complete social, press, document, presentation, and email export kit.
- [`brand/ou-profile-mark-v1.svg`](brand/ou-profile-mark-v1.svg) is the single institutional source for the GitHub organization avatar, browser favicon, touch icon, and installed-app icons.
- The live public specimen is available at [`/design-system`](https://openlyuseful.org/design-system); approved downloads are available at [`/brand/media-kit.html`](https://openlyuseful.org/brand/media-kit.html).

## Local preview

Serve this directory with any static web server, for example `python3 -m http.server 3000`.

## License

Website content and code are released under the MIT License unless otherwise noted.
