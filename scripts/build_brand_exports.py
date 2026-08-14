from __future__ import annotations

import copy
import base64
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from html import escape
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image

from build_brand_vectors import (
    GREEN,
    GREEN_LIGHT,
    GREEN_STRONG,
    INK,
    SHELL,
    Outline,
    number,
    outlined_text,
    paths_fragment,
)


ROOT = Path(__file__).resolve().parents[1]
SOCIAL = ROOT / "brand/social"
TEMPLATES = ROOT / "brand/templates"
PRESS = ROOT / "brand/press"


@dataclass(frozen=True)
class Export:
    key: str
    source: str
    output: str
    width: int
    height: int
    layout: str
    platforms: tuple[str, ...]
    safe_area: tuple[int, int, int, int]
    opaque: bool = True


EXPORTS = (
    Export(
        "openGraph",
        "brand/social/openly-useful-open-graph-1200x630.svg",
        "brand/social/openly-useful-open-graph-1200x630.png",
        1200,
        630,
        "editorial-share",
        ("Open Graph", "website links", "Slack", "Discord"),
        (60, 48, 1080, 534),
    ),
    Export(
        "githubPreview",
        "brand/social/openly-useful-github-preview-1280x640.svg",
        "brand/social/openly-useful-github-preview-1280x640.png",
        1280,
        640,
        "repository-preview",
        ("GitHub repository social preview",),
        (64, 48, 1152, 544),
    ),
    Export(
        "linkedinShare",
        "brand/social/openly-useful-linkedin-share-1200x627.svg",
        "brand/social/openly-useful-linkedin-share-1200x627.png",
        1200,
        627,
        "editorial-share",
        ("LinkedIn link share",),
        (60, 48, 1080, 531),
    ),
    Export(
        "communityHeader",
        "brand/social/openly-useful-community-header-1500x500.svg",
        "brand/social/openly-useful-community-header-1500x500.png",
        1500,
        500,
        "community-header",
        ("X header", "Mastodon header", "Bluesky banner"),
        (160, 70, 1180, 360),
    ),
    Export(
        "linkedinCover",
        "brand/social/openly-useful-linkedin-cover-4200x700.svg",
        "brand/social/openly-useful-linkedin-cover-4200x700.png",
        4200,
        700,
        "company-cover",
        ("LinkedIn Page cover",),
        (900, 90, 2400, 520),
    ),
    Export(
        "instagramSquare",
        "brand/social/openly-useful-instagram-square-1080x1080.svg",
        "brand/social/openly-useful-instagram-square-1080x1080.png",
        1080,
        1080,
        "social-post",
        ("Instagram square", "LinkedIn image post"),
        (72, 72, 936, 936),
    ),
    Export(
        "instagramPortrait",
        "brand/social/openly-useful-instagram-portrait-1080x1350.svg",
        "brand/social/openly-useful-instagram-portrait-1080x1350.png",
        1080,
        1350,
        "social-portrait",
        ("Instagram portrait", "LinkedIn portrait post"),
        (72, 90, 936, 1170),
    ),
    Export(
        "storyReel",
        "brand/social/openly-useful-story-reel-1080x1920.svg",
        "brand/social/openly-useful-story-reel-1080x1920.png",
        1080,
        1920,
        "story-reel",
        ("Instagram Story", "Instagram Reel cover", "YouTube Short cover"),
        (90, 250, 900, 1420),
    ),
    Export(
        "youtubeBanner",
        "brand/social/openly-useful-youtube-banner-2560x1440.svg",
        "brand/social/openly-useful-youtube-banner-2560x1440.png",
        2560,
        1440,
        "youtube-banner",
        ("YouTube channel banner",),
        (507, 508, 1546, 423),
    ),
    Export(
        "youtubeThumbnail",
        "brand/social/openly-useful-youtube-thumbnail-1280x720.svg",
        "brand/social/openly-useful-youtube-thumbnail-1280x720.png",
        1280,
        720,
        "video-thumbnail",
        ("YouTube thumbnail", "video cover"),
        (64, 54, 1152, 612),
    ),
    Export(
        "presentationCover",
        "brand/templates/openly-useful-presentation-cover-1920x1080.svg",
        "brand/templates/openly-useful-presentation-cover-1920x1080.png",
        1920,
        1080,
        "presentation-cover",
        ("presentation title slide", "webinar holding slide"),
        (96, 86, 1728, 908),
    ),
    Export(
        "documentCover",
        "brand/templates/openly-useful-document-cover-letter-2550x3300.svg",
        "brand/templates/openly-useful-document-cover-letter-2550x3300.png",
        2550,
        3300,
        "document-cover",
        ("US Letter document cover", "press packet cover"),
        (180, 180, 2190, 2940),
    ),
    Export(
        "emailSignature",
        "brand/templates/openly-useful-email-signature-1200x240.svg",
        "brand/templates/openly-useful-email-signature-1200x240.png",
        1200,
        240,
        "email-signature",
        ("email signature at 600 × 120 CSS pixels",),
        (24, 24, 1152, 192),
    ),
    Export(
        "pressMarkPrimary",
        "brand/press/openly-useful-mark-primary-transparent-1024.svg",
        "brand/press/openly-useful-mark-primary-transparent-1024.png",
        1024,
        1024,
        "press-mark-primary",
        ("press", "partner", "transparent light-surface mark"),
        (128, 128, 768, 768),
        False,
    ),
    Export(
        "pressMarkReverse",
        "brand/press/openly-useful-mark-reverse-transparent-1024.svg",
        "brand/press/openly-useful-mark-reverse-transparent-1024.png",
        1024,
        1024,
        "press-mark-reverse",
        ("press", "partner", "transparent dark-surface mark"),
        (128, 128, 768, 768),
        False,
    ),
    Export(
        "pressLockupPrimary",
        "brand/press/openly-useful-lockup-primary-transparent-1600x289.svg",
        "brand/press/openly-useful-lockup-primary-transparent-1600x289.png",
        1600,
        289,
        "press-lockup-primary",
        ("press", "partner", "transparent light-surface lockup"),
        (40, 32, 1520, 225),
        False,
    ),
    Export(
        "pressLockupReverse",
        "brand/press/openly-useful-lockup-reverse-transparent-1600x289.svg",
        "brand/press/openly-useful-lockup-reverse-transparent-1600x289.png",
        1600,
        289,
        "press-lockup-reverse",
        ("press", "partner", "transparent dark-surface lockup"),
        (40, 32, 1520, 225),
        False,
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedded_png(relative_path: str) -> str:
    payload = base64.b64encode((ROOT / relative_path).read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def local_tag(element: ElementTree.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def graphic_children(relative_path: str) -> tuple[str, float, float]:
    path = ROOT / relative_path
    root = ElementTree.parse(path).getroot()
    view_box = [float(part) for part in root.get("viewBox", "").split()]
    if len(view_box) != 4 or view_box[:2] != [0, 0]:
        raise ValueError(f"Unsupported viewBox in {relative_path}")
    children: list[str] = []
    for child in root:
        if local_tag(child) in {"title", "desc", "metadata"}:
            continue
        clone = copy.deepcopy(child)
        for descendant in clone.iter():
            descendant.tag = local_tag(descendant)
            descendant.tail = None
        children.append(ElementTree.tostring(clone, encoding="unicode"))
    return "\n".join(children), view_box[2], view_box[3]


def place_asset(
    relative_path: str,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    opacity: float = 1,
) -> str:
    body, source_width, source_height = graphic_children(relative_path)
    scale = min(width / source_width, height / source_height)
    draw_width = source_width * scale
    draw_height = source_height * scale
    draw_x = x + (width - draw_width) / 2
    draw_y = y + (height - draw_height) / 2
    return (
        f'<g data-source="/{escape(relative_path)}" '
        f'data-source-sha256="{sha256(ROOT / relative_path)}" '
        f'transform="translate({number(draw_x)} {number(draw_y)}) scale({number(scale)})" '
        f'opacity="{number(opacity)}">\n{body}\n</g>'
    )


def place_outline(
    outline: Outline,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    align: str = "left",
) -> str:
    scale = min(width / outline.width, height / outline.height)
    draw_width = outline.width * scale
    draw_height = outline.height * scale
    if align == "center":
        draw_x = x + (width - draw_width) / 2
    elif align == "right":
        draw_x = x + width - draw_width
    else:
        draw_x = x
    draw_y = y + (height - draw_height) / 2
    return (
        f'<g transform="translate({number(draw_x)} {number(draw_y)}) scale({number(scale)})">\n'
        f'{paths_fragment(outline, fill, indent="  ")}\n</g>'
    )


def base_defs() -> str:
    return f"""
  <defs>
    <pattern id="ou-grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{GREEN}" opacity=".13"/>
    </pattern>
    <pattern id="ou-grid-reverse" width="42" height="42" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.3" fill="{GREEN_LIGHT}" opacity=".17"/>
    </pattern>
    <clipPath id="ou-photo"><rect x="0" y="0" width="1" height="1"/></clipPath>
  </defs>
""".rstrip()


def svg_document(title: str, description: str, width: int, height: int, body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" '
        'shape-rendering="geometricPrecision">\n'
        f'  <title id="title">{escape(title)}</title>\n'
        f'  <desc id="desc">{escape(description)}</desc>\n'
        f"{base_defs()}\n{body}\n</svg>\n"
    )


def shell_background(width: int, height: int) -> list[str]:
    return [
        f'<rect width="{width}" height="{height}" fill="{SHELL}"/>',
        f'<rect width="{width}" height="{height}" fill="url(#ou-grid)"/>',
    ]


def ink_background(width: int, height: int) -> list[str]:
    return [
        f'<rect width="{width}" height="{height}" fill="{INK}"/>',
        f'<rect width="{width}" height="{height}" fill="url(#ou-grid-reverse)"/>',
    ]


def editorial_share(export: Export, label: Outline) -> str:
    w, h = export.width, export.height
    photo_x = w * 0.61
    body = shell_background(w, h)
    body.extend(
        [
            f'<rect x="{number(photo_x)}" width="{number(w - photo_x)}" height="{h}" fill="{INK}"/>',
            f'<clipPath id="share-photo"><rect x="{number(photo_x)}" y="0" width="{number(w - photo_x)}" height="{h}"/></clipPath>',
            f'<image data-raster-source="/brand/monitorfolk-workshop.png" href="{embedded_png("brand/monitorfolk-workshop.png")}" x="{number(photo_x)}" y="0" width="{number(w - photo_x)}" height="{h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#share-photo)"/>',
            f'<rect x="{number(photo_x)}" width="6" height="{h}" fill="{GREEN}"/>',
            place_outline(label, x=w * .055, y=h * .065, width=w * .50, height=h * .042, fill=GREEN_STRONG),
            place_asset(
                "brand/ou-lockup-stacked-v4.svg",
                x=w * .07,
                y=h * .19,
                width=w * .46,
                height=h * .64,
            ),
        ]
    )
    return svg_document(
        "Openly Useful social share card",
        "The canonical Openly Useful stacked lockup beside the Monitorfolk workshop illustration.",
        w,
        h,
        "\n".join(body),
    )


def repository_preview(export: Export, label: Outline, prompt: Outline) -> str:
    w, h = export.width, export.height
    body = ink_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="18" height="{h}" fill="{GREEN_LIGHT}"/>',
            f'<rect x="{w - 96}" y="0" width="96" height="{h}" fill="{GREEN}"/>',
            place_outline(label, x=w * .075, y=h * .10, width=w * .65, height=h * .05, fill=GREEN_LIGHT),
            place_asset(
                "brand/ou-lockup-horizontal-reverse-v4.svg",
                x=w * .075,
                y=h * .29,
                width=w * .62,
                height=h * .29,
            ),
            f'<rect x="{number(w * .075)}" y="{number(h * .76)}" width="{number(w * .67)}" height="2" fill="{GREEN_LIGHT}" opacity=".65"/>',
            place_outline(prompt, x=w * .075, y=h * .80, width=w * .56, height=h * .055, fill=GREEN_LIGHT),
            place_asset(
                "brand/ou-monitor-reverse-v3.svg",
                x=w * .79,
                y=h * .25,
                width=w * .13,
                height=h * .50,
                opacity=.92,
            ),
        ]
    )
    return svg_document(
        "Openly Useful repository social preview",
        "A dark repository card with the exact reverse horizontal lockup and Open Monitor mark.",
        w,
        h,
        "\n".join(body),
    )


def community_header(export: Export, label: Outline) -> str:
    w, h = export.width, export.height
    body = ink_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{number(w * .11)}" height="{h}" fill="{GREEN}"/>',
            f'<rect x="{number(w * .11)}" y="{number(h * .14)}" width="3" height="{number(h * .72)}" fill="{GREEN_LIGHT}"/>',
            place_asset(
                "brand/ou-monitor-reverse-v3.svg",
                x=w * .025,
                y=h * .23,
                width=w * .06,
                height=h * .54,
            ),
            place_asset(
                "brand/ou-lockup-horizontal-reverse-v4.svg",
                x=w * .24,
                y=h * .25,
                width=w * .52,
                height=h * .32,
            ),
            place_outline(label, x=w * .24, y=h * .66, width=w * .52, height=h * .07, fill=GREEN_LIGHT),
        ]
    )
    return svg_document(
        "Openly Useful community header",
        "A crop-safe three-to-one community banner using the exact reverse lockup.",
        w,
        h,
        "\n".join(body),
    )


def company_cover(export: Export, label: Outline) -> str:
    w, h = export.width, export.height
    body = shell_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{number(w * .14)}" height="{h}" fill="{GREEN}"/>',
            f'<rect x="{number(w * .86)}" y="0" width="{number(w * .14)}" height="{h}" fill="{INK}"/>',
            place_asset(
                "brand/ou-lockup-horizontal-v4.svg",
                x=w * .31,
                y=h * .20,
                width=w * .38,
                height=h * .38,
            ),
            place_outline(label, x=w * .31, y=h * .67, width=w * .38, height=h * .08, fill=GREEN_STRONG, align="center"),
        ]
    )
    return svg_document(
        "Openly Useful LinkedIn Page cover",
        "A centered crop-safe company cover with the canonical horizontal lockup.",
        w,
        h,
        "\n".join(body),
    )


def social_post(export: Export, label: Outline, prompt: Outline) -> str:
    w, h = export.width, export.height
    body = shell_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{w}" height="{number(h * .055)}" fill="{GREEN}"/>',
            place_outline(label, x=w * .075, y=h * .105, width=w * .85, height=h * .045, fill=GREEN_STRONG, align="center"),
            place_asset(
                "brand/ou-lockup-stacked-v4.svg",
                x=w * .16,
                y=h * .20,
                width=w * .68,
                height=h * .54,
            ),
            f'<rect x="{number(w * .075)}" y="{number(h * .83)}" width="{number(w * .85)}" height="{number(h * .10)}" rx="{number(h * .018)}" fill="{INK}"/>',
            place_outline(prompt, x=w * .12, y=h * .845, width=w * .76, height=h * .065, fill=GREEN_LIGHT, align="center"),
        ]
    )
    return svg_document(
        "Openly Useful square social post",
        "A square launch card built from the exact stacked lockup and terminal prompt motif.",
        w,
        h,
        "\n".join(body),
    )


def social_portrait(export: Export, label: Outline, prompt: Outline) -> str:
    w, h = export.width, export.height
    body = shell_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{w}" height="{number(h * .045)}" fill="{GREEN}"/>',
            place_outline(label, x=w * .08, y=h * .095, width=w * .84, height=h * .038, fill=GREEN_STRONG, align="center"),
            place_asset(
                "brand/ou-lockup-stacked-v4.svg",
                x=w * .14,
                y=h * .16,
                width=w * .72,
                height=h * .48,
            ),
            f'<rect x="{number(w * .08)}" y="{number(h * .70)}" width="{number(w * .84)}" height="{number(h * .18)}" rx="{number(h * .025)}" fill="{INK}"/>',
            place_asset(
                "brand/ou-monitor-reverse-v3.svg",
                x=w * .11,
                y=h * .73,
                width=w * .12,
                height=h * .12,
            ),
            place_outline(prompt, x=w * .28, y=h * .75, width=w * .56, height=h * .075, fill=GREEN_LIGHT, align="center"),
            f'<rect x="{number(w * .08)}" y="{number(h * .925)}" width="{number(w * .84)}" height="2" fill="{GREEN}" opacity=".55"/>',
        ]
    )
    return svg_document(
        "Openly Useful portrait social post",
        "A four-to-five social post with the exact stacked lockup and a terminal panel.",
        w,
        h,
        "\n".join(body),
    )


def story_reel(export: Export, label: Outline, prompt: Outline) -> str:
    w, h = export.width, export.height
    body = ink_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{number(w * .065)}" height="{h}" fill="{GREEN}"/>',
            f'<rect x="{number(w * .065)}" y="{number(h * .13)}" width="3" height="{number(h * .74)}" fill="{GREEN_LIGHT}"/>',
            place_outline(label, x=w * .14, y=h * .17, width=w * .72, height=h * .035, fill=GREEN_LIGHT, align="center"),
            place_asset(
                "brand/ou-lockup-stacked-reverse-v4.svg",
                x=w * .16,
                y=h * .28,
                width=w * .68,
                height=h * .36,
            ),
            f'<rect x="{number(w * .14)}" y="{number(h * .72)}" width="{number(w * .72)}" height="{number(h * .10)}" rx="{number(h * .018)}" fill="{SHELL}"/>',
            place_outline(prompt, x=w * .20, y=h * .738, width=w * .60, height=h * .06, fill=GREEN_STRONG, align="center"),
        ]
    )
    return svg_document(
        "Openly Useful story and reel cover",
        "A nine-to-sixteen dark social cover keeping all critical branding inside the platform-safe center.",
        w,
        h,
        "\n".join(body),
    )


def youtube_banner(export: Export, label: Outline) -> str:
    w, h = export.width, export.height
    safe_x, safe_y, safe_w, safe_h = export.safe_area
    body = ink_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{number(w * .17)}" height="{h}" fill="{GREEN}"/>',
            f'<rect x="{number(w * .83)}" y="0" width="{number(w * .17)}" height="{h}" fill="{GREEN_STRONG}"/>',
            place_asset(
                "brand/ou-monitor-reverse-v3.svg",
                x=safe_x + safe_w * .03,
                y=safe_y + safe_h * .17,
                width=safe_w * .14,
                height=safe_h * .66,
            ),
            place_asset(
                "brand/ou-lockup-horizontal-reverse-v4.svg",
                x=safe_x + safe_w * .22,
                y=safe_y + safe_h * .18,
                width=safe_w * .58,
                height=safe_h * .38,
            ),
            place_outline(label, x=safe_x + safe_w * .22, y=safe_y + safe_h * .66, width=safe_w * .58, height=safe_h * .10, fill=GREEN_LIGHT, align="center"),
        ]
    )
    return svg_document(
        "Openly Useful YouTube channel banner",
        "A 2560 by 1440 channel banner with the complete identity inside YouTube's center safe area.",
        w,
        h,
        "\n".join(body),
    )


def video_thumbnail(export: Export, label: Outline, prompt: Outline) -> str:
    w, h = export.width, export.height
    body = shell_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{number(w * .37)}" height="{h}" fill="{GREEN}"/>',
            place_asset(
                "brand/ou-monitor-reverse-v3.svg",
                x=w * .08,
                y=h * .22,
                width=w * .20,
                height=h * .56,
            ),
            place_outline(label, x=w * .44, y=h * .17, width=w * .48, height=h * .09, fill=GREEN_STRONG),
            place_asset(
                "brand/ou-wordmark-v4.svg",
                x=w * .44,
                y=h * .32,
                width=w * .48,
                height=h * .18,
            ),
            f'<rect x="{number(w * .44)}" y="{number(h * .62)}" width="{number(w * .48)}" height="{number(h * .15)}" rx="{number(h * .025)}" fill="{INK}"/>',
            place_outline(prompt, x=w * .48, y=h * .65, width=w * .40, height=h * .09, fill=GREEN_LIGHT, align="center"),
        ]
    )
    return svg_document(
        "Openly Useful video thumbnail",
        "A reusable video cover with a large exact Open Monitor mark and canonical wordmark.",
        w,
        h,
        "\n".join(body),
    )


def presentation_cover(export: Export, label: Outline, website: Outline) -> str:
    w, h = export.width, export.height
    photo_x = w * .62
    body = shell_background(w, h)
    body.extend(
        [
            f'<clipPath id="presentation-photo"><rect x="{number(photo_x)}" y="0" width="{number(w - photo_x)}" height="{h}"/></clipPath>',
            f'<image data-raster-source="/brand/monitorfolk-workshop.png" href="{embedded_png("brand/monitorfolk-workshop.png")}" x="{number(photo_x)}" y="0" width="{number(w - photo_x)}" height="{h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#presentation-photo)"/>',
            f'<rect x="{number(photo_x)}" width="8" height="{h}" fill="{GREEN}"/>',
            place_outline(label, x=w * .065, y=h * .09, width=w * .47, height=h * .05, fill=GREEN_STRONG),
            place_asset(
                "brand/ou-lockup-stacked-v4.svg",
                x=w * .075,
                y=h * .22,
                width=w * .44,
                height=h * .52,
            ),
            f'<rect x="{number(w * .065)}" y="{number(h * .86)}" width="{number(w * .48)}" height="2" fill="{GREEN}" opacity=".6"/>',
            place_outline(website, x=w * .065, y=h * .89, width=w * .32, height=h * .045, fill=GREEN_STRONG),
        ]
    )
    return svg_document(
        "Openly Useful presentation cover",
        "A widescreen title slide with the canonical lockup and Monitorfolk workshop illustration.",
        w,
        h,
        "\n".join(body),
    )


def document_cover(export: Export, label: Outline, website: Outline) -> str:
    w, h = export.width, export.height
    body = shell_background(w, h)
    body.extend(
        [
            f'<rect x="0" y="0" width="{w}" height="{number(h * .045)}" fill="{GREEN}"/>',
            place_outline(label, x=w * .075, y=h * .11, width=w * .85, height=h * .035, fill=GREEN_STRONG, align="center"),
            place_asset(
                "brand/ou-lockup-stacked-v4.svg",
                x=w * .14,
                y=h * .21,
                width=w * .72,
                height=h * .42,
            ),
            f'<rect x="{number(w * .075)}" y="{number(h * .76)}" width="{number(w * .85)}" height="{number(h * .08)}" rx="{number(h * .012)}" fill="{INK}"/>',
            place_asset(
                "brand/ou-monitor-reverse-v3.svg",
                x=w * .10,
                y=h * .775,
                width=w * .065,
                height=h * .05,
            ),
            place_outline(website, x=w * .20, y=h * .785, width=w * .56, height=h * .032, fill=GREEN_LIGHT),
            f'<rect x="{number(w * .075)}" y="{number(h * .91)}" width="{number(w * .85)}" height="3" fill="{GREEN}" opacity=".55"/>',
        ]
    )
    return svg_document(
        "Openly Useful document cover",
        "A US Letter cover page using the exact stacked lockup with print-safe margins.",
        w,
        h,
        "\n".join(body),
    )


def email_signature(export: Export, website: Outline) -> str:
    w, h = export.width, export.height
    body = [f'<rect width="{w}" height="{h}" fill="{SHELL}"/>']
    body.extend(
        [
            place_asset(
                "brand/ou-lockup-horizontal-v4.svg",
                x=36,
                y=42,
                width=620,
                height=112,
            ),
            f'<rect x="700" y="36" width="3" height="168" fill="{GREEN}"/>',
            place_outline(website, x=758, y=72, width=390, height=48, fill=GREEN_STRONG),
        ]
    )
    return svg_document(
        "Openly Useful email signature",
        "A two-times email signature image with the canonical horizontal lockup and website.",
        w,
        h,
        "\n".join(body),
    )


def press_asset(export: Export) -> str:
    if "Mark" in export.key:
        source = "brand/ou-monitor-reverse-v3.svg" if "Reverse" in export.key else "brand/ou-monitor-mark-v3.svg"
        padding = 128
    else:
        source = "brand/ou-lockup-horizontal-reverse-v4.svg" if "Reverse" in export.key else "brand/ou-lockup-horizontal-v4.svg"
        padding = 32
    body = place_asset(
        source,
        x=padding,
        y=padding,
        width=export.width - padding * 2,
        height=export.height - padding * 2,
    )
    return svg_document(
        f"Openly Useful {export.key}",
        "A transparent production raster source using the exact canonical vector asset.",
        export.width,
        export.height,
        body,
    )


def render(export: Export, source: str) -> None:
    source_path = ROOT / export.source
    output_path = ROOT / export.output
    source_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source, encoding="utf-8")
    resvg = shutil.which("resvg")
    if resvg:
        subprocess.run(
            [resvg, str(source_path), str(output_path), "--width", str(export.width), "--height", str(export.height)],
            check=True,
            capture_output=True,
        )
    elif sys.platform == "darwin" and shutil.which("sips"):
        subprocess.run(
            ["sips", "-s", "format", "png", str(source_path), "--out", str(output_path)],
            check=True,
            capture_output=True,
        )
    else:
        try:
            from cairosvg import svg2png
        except (ImportError, OSError) as error:
            raise RuntimeError(
                "Raster export needs resvg, macOS sips, or CairoSVG with libcairo."
            ) from error
        png = svg2png(
            bytestring=source.encode("utf-8"),
            url=str(source_path),
            output_width=export.width,
            output_height=export.height,
        )
        output_path.write_bytes(png)
    with Image.open(output_path) as image:
        expected_mode = "RGB" if export.opaque else "RGBA"
        converted = image.convert(expected_mode)
        converted.save(output_path, format="PNG", optimize=True)


def main() -> None:
    technical_font = ROOT / "design-system/fonts/IBMPlexMono-variable-latin1.woff2"
    label = outlined_text(
        technical_font,
        "AN INDEPENDENT OPEN-SOURCE COLLECTIVE",
        weight=700,
        tracking=50,
    )
    prompt = outlined_text(
        technical_font,
        "$ openly-useful --share",
        weight=600,
        tracking=5,
    )
    website = outlined_text(
        technical_font,
        "openlyuseful.org",
        weight=700,
        tracking=20,
    )

    for export in EXPORTS:
        if export.layout == "editorial-share":
            source = editorial_share(export, label)
        elif export.layout == "repository-preview":
            source = repository_preview(export, label, prompt)
        elif export.layout == "community-header":
            source = community_header(export, label)
        elif export.layout == "company-cover":
            source = company_cover(export, label)
        elif export.layout == "social-post":
            source = social_post(export, label, prompt)
        elif export.layout == "social-portrait":
            source = social_portrait(export, label, prompt)
        elif export.layout == "story-reel":
            source = story_reel(export, label, prompt)
        elif export.layout == "youtube-banner":
            source = youtube_banner(export, label)
        elif export.layout == "video-thumbnail":
            source = video_thumbnail(export, label, prompt)
        elif export.layout == "presentation-cover":
            source = presentation_cover(export, label, website)
        elif export.layout == "document-cover":
            source = document_cover(export, label, website)
        elif export.layout == "email-signature":
            source = email_signature(export, website)
        elif export.layout.startswith("press-"):
            source = press_asset(export)
        else:
            raise ValueError(export.layout)
        render(export, source)

    manifest = {
        "schemaVersion": 1,
        "kitVersion": "1.0.0",
        "brandVersion": "3.1.0",
        "canonicalProfileAsset": "/brand/ou-profile-mark-v1.png",
        "canonicalTagline": "Useful things, openly made.",
        "platformSpecsVerified": "2026-08-14",
        "exports": [
            {
                **asdict(export),
                "platforms": list(export.platforms),
                "safe_area": list(export.safe_area),
                "source": f"/{export.source}",
                "output": f"/{export.output}",
                "sha256": sha256(ROOT / export.output),
            }
            for export in EXPORTS
        ],
    }
    (SOCIAL / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(EXPORTS)} Openly Useful brand exports")


if __name__ == "__main__":
    main()
