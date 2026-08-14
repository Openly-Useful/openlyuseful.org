# Openly Useful Social Kit

Version **1.0.0**, aligned to Openly Useful brand system **3.1.0**.

This folder contains upload-ready PNG files and same-size editable SVG compositions. Every logo instance is copied without path edits from the canonical versioned brand assets. Platform crops can change the surrounding composition, but they may not change the O/U face, weight, spacing, wordmark, or tagline.

## Upload map

| Surface | Upload this file | Size | Notes |
|---|---|---:|---|
| Website, Open Graph, Slack, Discord | `openly-useful-open-graph-1200x630.png` | 1200 × 630 | Default link preview; editorial illustration is intentionally cropped on the right. |
| GitHub repository social preview | `openly-useful-github-preview-1280x640.png` | 1280 × 640 | Flat-color PNG under 1 MB; safe on light and dark link surfaces. |
| LinkedIn link share | `openly-useful-linkedin-share-1200x627.png` | 1200 × 627 | LinkedIn’s 1.91:1 link-post composition. |
| X, Mastodon, Bluesky header | `openly-useful-community-header-1500x500.png` | 1500 × 500 | Critical content stays inside the center band; X may crop roughly 60 px from top and bottom. |
| LinkedIn Page cover | `openly-useful-linkedin-cover-4200x700.png` | 4200 × 700 | Center-weighted with no critical detail near the lower-right profile overlay. |
| Instagram square | `openly-useful-instagram-square-1080x1080.png` | 1080 × 1080 | Launch, announcement, and evergreen identity post. |
| Instagram portrait | `openly-useful-instagram-portrait-1080x1350.png` | 1080 × 1350 | Four-to-five feed post with extra vertical room. |
| Story, Reel cover, Short cover | `openly-useful-story-reel-1080x1920.png` | 1080 × 1920 | All critical elements are inside the documented center safe area in `manifest.json`. |
| YouTube channel banner | `openly-useful-youtube-banner-2560x1440.png` | 2560 × 1440 | Lockup and descriptor are wholly inside the 1546 × 423 cross-device safe area. |
| YouTube thumbnail | `openly-useful-youtube-thumbnail-1280x720.png` | 1280 × 720 | Evergreen channel thumbnail; customize the generator for episode-specific copy. |

Use `/brand/ou-profile-mark-v1.png` for all square profile images. Do not create a separate platform avatar. The 1024 × 1024 master safely downscales to GitHub, X, LinkedIn, Mastodon, Bluesky, Instagram, and YouTube profile contexts.

## Platform specifications

Specifications were checked on **2026-08-14** against primary platform guidance:

- [GitHub repository social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview): 1280 × 640 for best display, under 1 MB.
- [X profile image and header](https://help.x.com/en/managing-your-account/common-issues-when-uploading-profile-photo.html): 400 × 400 profile and 1500 × 500 header; edge cropping can occur.
- [LinkedIn Page images](https://www.linkedin.com/help/linkedin/answer/a563309/image-specifications-for-your-linkedin-pages-and-career-pages?lang=en): 400 × 400 logo, 4200 × 700 Page cover, and 1200 × 627 link images.
- [YouTube channel branding](https://support.google.com/youtube/answer/10456525): 2560 × 1440 recommended banner; 1546 × 423 center safe area at that size; 6 MB maximum.
- [Instagram photo resolution](https://www.facebook.com/help/1631821640426723/): 1080 px width with supported aspect ratios from 1.91:1 through 3:4.
- [Mastodon profile setup](https://docs.joinmastodon.org/user/profile/): avatars downscale to 400 × 400 and headers to 1500 × 500, each under 2 MB.

Platform guidance changes. Reconfirm the dimensions before a major campaign or whenever a platform visibly changes its crop behavior.

## Safe-area and editing rules

- `manifest.json` records the exact `[x, y, width, height]` safe area for every file.
- Keep logos and essential copy inside that safe area. Decorative color rails and dot fields may extend beyond it.
- Edit the strings or layout functions in `scripts/build_brand_exports.py`, then rebuild. Do not manually move individual logo paths in the SVG output.
- Use PNG files for upload. Keep SVG files as editable/reproducible sources.
- Use the institutional mark for identity and organization surfaces. Monitorfolk remain editorial imagery, never a replacement logo.
- Do not add campaign copy directly to the canonical evergreen exports; create a separately named campaign derivative.

## Rebuild

Install `scripts/requirements-vector.txt`, then run:

```sh
python3 scripts/build_brand_vectors.py
python3 scripts/build_brand_exports.py
python3 scripts/validate_brand_exports.py
```

The exporter uses `resvg` when installed, macOS `sips` locally, or CairoSVG with libcairo as a portable fallback. The source compositions remain standard self-contained vector geometry plus the versioned local Monitorfolk raster where noted.
