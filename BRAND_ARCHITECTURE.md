# Openly Useful brand architecture

Openly Useful is one master studio brand with two complementary public homes.

| Expression | Domain | Role |
|---|---|---|
| **Openly Useful Studio** | **OpenlyUseful.com** | Commercial and institutional home for products, capabilities, partnerships, and experiments |
| **Openly Useful Open Source** | **OpenlyUseful.org** | Open-source hub for public projects, documentation, contribution, and shared identity resources |

The domain endings reinforce the distinction, but each page also states its role in navigation, metadata, page copy, and cross-domain links. Neither domain is a separate brand.

## Publisher and legal-entity model

Openly Useful uses one canonical publisher identity across both domains and across skills, MCP servers, packages, and provider listings. **Openly Useful** is the public display name. **Openly Useful LLC** is the planned legal entity; its current status is **`formation-pending`**. The planned entity must not be described as formed, active, or the current legal publisher or operator until formation and required publisher verification are complete.

[`OpenlyUseful.org/publisher`](https://openlyuseful.org/publisher) is the human-readable publisher record, and [`publisher/manifest.json`](publisher/manifest.json) is its published machine-readable authority endpoint. The public manifest is projected from the governed editable publisher source; it is not a separately maintained second source of truth. Provider-specific artifacts may adapt packaging, but must derive publisher identity, domains, contacts, policy URLs, and namespaces from that authority endpoint.

- `OpenlyUseful.com` is the Studio and product-facing home.
- `OpenlyUseful.org` is the Open Source, documentation, policy, and canonical publisher home.
- `org.openlyuseful` is the open-source MCP namespace.
- `com.openlyuseful` is the reserved Studio MCP namespace.

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
- Publisher, support, privacy, terms, and security records remain canonical on `.org`; the corresponding `.com` paths permanently redirect there.
