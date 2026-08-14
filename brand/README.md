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
| `ou-monitor-mark.svg` | Primary institutional mark for light surfaces |
| `ou-monitor-reverse.svg` | Reverse institutional mark for Ink or Terminal surfaces |
| `ou-monitor-character.svg` | Antenna form for expressive character contexts |
| `ou-monitor-bot.svg` | Deterministic Monitorfolk starter character |
| `brandkit.html` | Reproducible source for the production brand board |
| `brandkit-open-monitor.png` | Production brand board rendered from the canonical SVGs |
| `monitorfolk-workshop.png` | Cropped editorial illustration used by the board and social card |
| `og-card.html` | Reproducible source for the social card |
| `/favicon.svg` | Small-size application icon |
| `/og-v4.png` | Social and link-preview card rendered with the canonical mark |

The SVG files are the implementation source of truth. Both production raster layouts load those exact SVGs; neither contains an independently drawn official logo. The workshop illustration sets the character world and is not a geometry source.

The retired `open-shell-*`, `shellfolk-builder.svg`, `brandkit-overview.png`, `og.png`, `og-v2.png`, and `og-v3.png` files remain in the repository as version history. Do not use them for new work.

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
- Use the antenna character mark for editorial, community, onboarding, and illustration contexts only.
- Do not rotate, stretch, outline, add facial features, move the U, replace the cursor eyes, add gradients, or place the mark inside another container.
- Do not place Monitorfolk where a system error, warning, or destructive action needs undivided attention.
- Use the exact tagline: **Useful things, openly made.**

## Geometry and optical QA

- Eye centerlines are fixed at x = 24 and x = 40 in the 64-unit institutional grid. These are the exact centerlines of the U stems.
- Eye bottoms end at y = 30; the U begins at y = 34, preserving a four-unit gap at every rendered size.
- The filled U ends at y = 47.5; the inner O counter ends at y = 50, preserving a 2.5-unit lower gap.
- The U is a filled path, not a stroked path. Do not recreate it with square stroke caps; cap extension is what caused the original eyes and stems to appear fused.
- The same alignment rule is enforced in the reverse, character, favicon, and Monitorfolk assets by `scripts/validate_brand_geometry.py` and the repository’s required validation check.
- Official logo appearances in the live site, brand board, and social card must reference `ou-monitor-mark.svg` or `ou-monitor-character.svg`; redrawing the face inside a raster composition is prohibited.

See [`/design-system/README.md`](../design-system/README.md) for tokens, components, patterns, accessibility, voice, and governance.
