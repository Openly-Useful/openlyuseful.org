# Openly Useful Brand Kit

The Openly Useful identity turns a comfortable sharing ecosystem into one direct relationship: **O + U**.

## Core metaphor

The **Open Monitor** combines:

- an outer **O** for open space, open systems, and the shared environment around the work;
- an inner **U** for useful, user, and you;
- two cursor-like eyes that make the relationship feel awake, friendly, and ready to help.

The institutional mark has no antenna. The character form adds one antenna only when the identity is acting as a guide or participant. Every expression should feel open but not exposed, capable but not intimidating, nostalgic but not frozen in the past.

## Included assets

| Asset | Purpose |
|---|---|
| `manifest.json` | Canonical name, tagline, version, assets, and allowed lockup contexts |
| `ou-monitor-mark-v3.svg` | Primary institutional mark for light surfaces |
| `ou-monitor-reverse-v3.svg` | Reverse institutional mark for Ink or Terminal surfaces |
| `ou-monitor-character-v3.svg` | Antenna form for expressive character contexts |
| `ou-monitor-bot-v3.svg` | Deterministic Monitorfolk starter character |
| `ou-wordmark-v4.svg` / `ou-wordmark-reverse-v4.svg` | Canonical name converted to fixed outlines |
| `ou-tagline-v4.svg` / `ou-tagline-reverse-v4.svg` | Canonical tagline converted to fixed outlines |
| `ou-lockup-horizontal-v4.svg` / reverse | Complete navigation/footer composition; never rebuild from children |
| `ou-lockup-stacked-v4.svg` / reverse | Complete hero/board/social composition; never rebuild from children |
| `ou-profile-mark-v1.svg` | Canonical institutional mark on Shell for avatars and application icons |
| `ou-profile-mark-v1.png` | Exact 1024 × 1024 GitHub organization upload derived from the profile SVG |
| `profile-mark-raster.html` | Forced-square browser source used to generate every profile PNG without crop drift |
| `brandkit.html` | Reproducible source for the production brand board |
| `brandkit-open-monitor-v5.png` | Production brand board rendered from the canonical outlined lockup |
| `monitorfolk-workshop.png` | Cropped editorial illustration used by the board and social card |
| `og-card.html` | Previous standalone social-card source retained for compatibility; production exports now come from `scripts/build_brand_exports.py` |
| `/apple-touch-icon-v1.png` | 180 × 180 touch icon derived from the profile master |
| `/icon-192-v1.png` / `/icon-512-v1.png` | Installable-web-app icons derived from the profile master |
| `/site.webmanifest` | Browser application metadata pointing only to the canonical icon family |
| `social/openly-useful-open-graph-1200x630.png` | Canonical social and link-preview card rendered with the outlined lockup |
| `studio/openly-useful-studio-open-graph-1200x630.png` | Ink-dominant Studio link-preview derivative using the unchanged reverse lockup |
| `open-source/openly-useful-open-source-open-graph-1200x630.png` | Shell Open Source link-preview derivative using the unchanged primary lockup |
| `social/` | Upload-ready social headers, share cards, posts, video art, exact-size SVG sources, and a platform manifest |
| `press/` | Transparent primary/reverse mark and horizontal-lockup exports plus press boilerplate |
| `templates/` | Presentation, document, and email-signature masters |

The manifest and versioned SVG files form the visual source of truth. Each approved lockup is one precomposed, outlined vector: the mark, wordmark, tagline, spacing, and proportions are all frozen in the same `viewBox`. The homepage, design-system page, and both production raster layouts scale those exact paths. The licensed font files remain the reproducible source for rebuilding the outlines and the site’s interface typography; they are no longer used to typeset the visible logo at runtime. The workshop illustration sets the character world and is not a geometry source.

The social, press, and template kits are compositions around those canonical assets, not additional logos. Each SVG source embeds an unchanged versioned mark or lockup inside an outer transform, and `scripts/validate_brand_exports.py` compares the embedded paths and recorded source hashes to the canonical files. Platform-safe areas and upload mappings live in `social/manifest.json`.

The Studio and Open Source Open Graph cards are domain-specific derivatives, not replacements for the governed export kit. Their HTML sources reference the exact approved lockups and local fonts; they introduce no alternate logo geometry or color tokens.

Retired pre-v3 assets live under `archive/pre-v3/` for historical reference only. Historical public URLs permanently redirect to the current identity so old links do not break and cannot serve competing branding.

## Emotional direction

Think shared Unix workstation, public library computer room, a carefully maintained README, a corkboard of local knowledge, and patient people teaching one another. Use beige hardware, recycled paper, soft plants, green task lamps, wood, matte plastic, and restrained hand-inked or halftone texture.

Nostalgia comes from **shared rituals**, not vintage decoration. Never reduce contrast, use illegible pixel type, add faux scan-line damage, or copy Linux/Tux, BSD, Roblox, The Jetsons, or another project’s protected character language.

## Character system

Monitorfolk are modular maintainers with rounded monitor heads and the exact O/U face on every screen. Favor scenes with two or more characters pairing, reviewing, repairing, carrying, or teaching. Their posture is useful and collaborative—not heroic, collectible, or game-like. Antennas, shell color, headphones, and workwear may vary; the face geometry may not.

## Production rules

- Preserve clear space of one inner U width around the institutional logo.
- Minimum digital mark size: 20 px; the supplied favicon is approved at 16 px. Minimum print size: 6 mm.
- Use Terminal green on Shell; use the reverse mark on Ink or Terminal.
- Use the institutional mark for organization, navigation, repositories, products, favicons, legal, and formal partnership contexts.
- Use `ou-profile-mark-v1.svg` or its exact raster derivative for organization avatars and application icons; do not use the character mark or a platform-generated identicon.
- Use the antenna character mark for editorial, community, onboarding, and illustration contexts only.
- Do not rotate, stretch, outline, add facial features, move the U, replace the cursor eyes, add gradients, or place the mark inside another container.
- Do not place Monitorfolk where a system error, warning, or destructive action needs undivided attention.
- Use the exact tagline: **Useful things, openly made.**
- Use the complete horizontal or stacked v4 SVG; do not recombine its children on a product surface.
- Scale the complete asset through `design-system/brand.css`. Do not redefine wordmark weight, tracking, optical width, tagline weight, or internal lockup spacing.

## Geometry and optical QA

- Eye centerlines are fixed at x = 24 and x = 40 in the 64-unit institutional grid. These are the exact centerlines of the U stems.
- Eye bottoms end at y = 30; the U begins at y = 34, preserving a four-unit gap at every rendered size.
- The filled U ends at y = 47.5; the inner O counter ends at y = 50, preserving a 2.5-unit lower gap.
- The U is a filled path, not a stroked path. Do not recreate it with square stroke caps; cap extension is what caused the original eyes and stems to appear fused.
- The same alignment rule is enforced in the reverse, character, favicon, and Monitorfolk assets by `scripts/validate_brand_geometry.py` and the repository’s required validation check.
- Official logo appearances in the live site, brand board, and social card must reference the versioned paths in `manifest.json`; redrawing the face inside a raster composition is prohibited.
- `scripts/validate_brand_system.py` rejects active legacy URLs, independent lockup overrides, live-text logos, missing outlined masters, incorrect canonical copy, or missing compatibility redirects.

See [`/design-system/README.md`](../design-system/README.md) for tokens, components, patterns, accessibility, voice, and governance.
