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
- [`scripts/build_brand_vectors.py`](scripts/build_brand_vectors.py) reproducibly converts the licensed source fonts into the canonical outlined wordmark, tagline, and lockups.
- The live public specimen is available at [`/design-system`](https://openlyuseful.org/design-system).

## Local preview

Serve this directory with any static web server, for example `python3 -m http.server 3000`.

## License

Website content and code are released under the MIT License unless otherwise noted.
