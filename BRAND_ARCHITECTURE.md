# Openly Useful brand architecture

Openly Useful is one master studio brand with two complementary public homes.

| Expression | Domain | Role |
|---|---|---|
| **Openly Useful Studio** | **OpenlyUseful.com** | Commercial and institutional home for products, capabilities, partnerships, and experiments |
| **Openly Useful Open Source** | **OpenlyUseful.org** | Open-source hub for public projects, documentation, contribution, and shared identity resources |

The domain endings reinforce the distinction, but each page also states its role in navigation, metadata, page copy, and cross-domain links. Neither domain is a separate brand.

## Canonical language

- Master description: **Openly Useful is an independent studio making thoughtful products and open-source tools.**
- Studio descriptor: **Independent products and experiments.**
- Studio primary line: **Practical software, thoughtfully made.**
- Open Source descriptor: **Open-source tools for everyone.**
- Canonical tagline: **Useful things, openly made.**
- Portfolio signpost: **Products and studio work live at OpenlyUseful.com. Open-source work lives at OpenlyUseful.org.**

Use **Openly Useful** as two words in prose and identity work. Use **OpenlyUseful.com** and **OpenlyUseful.org** only when writing the domains. Product brands lead with their own names and may use **A product from Openly Useful** as a quiet endorsement.

## Visual relationship

Both sites use the exact governed Open Monitor mark and lockups, Atkinson Hyperlegible Next and IBM Plex Mono, shared spacing, and the Shell / Unix Ink / Terminal / Process foundations. The Studio is the Ink-dominant inverse side of the same system: more editorial and product-focused, without redrawing the mark or introducing a competing palette.

The `.org` design system, media kit, and approved identity files remain canonical. Domain-specific social cards are additive compositions around the unchanged approved lockups.

## Routing contract

- `openlyuseful.com/` serves `studio.html` through a Vercel host-matched rewrite.
- `openlyuseful.org/` serves `open-source.html` through the default root rewrite.
- Host-specific documents use internal filenames so Vercel's filesystem precedence cannot shadow the public root, robots, or sitemap rewrites.
- Each domain has its own canonical metadata, robots response, sitemap, and sibling-domain cross-link.
- `www.openlyuseful.com` and `www.openlyuseful.org` permanently redirect to their matching apex domains.
- Open-source documentation remains canonical on `.org`; `.com/design-system` permanently redirects there.
