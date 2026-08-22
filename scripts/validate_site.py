from __future__ import annotations

import json
import zlib
from html.parser import HTMLParser
from pathlib import Path
from struct import unpack

from validate_brand_geometry import validate_brand_geometry
from validate_brand_exports import validate_brand_exports
from validate_brand_system import validate_brand_system

ROOT = Path(__file__).resolve().parents[1]


class LandingPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        assert image.read(8) == b"\x89PNG\r\n\x1a\n"
        assert image.read(4) == b"\x00\x00\x00\r"
        assert image.read(4) == b"IHDR"
        return unpack(">II", image.read(8))


def png_rgb_pixels(path: Path) -> tuple[int, int, list[bytes]]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    offset = 8
    width = height = 0
    compressed = bytearray()
    while offset < len(data):
        length = unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type = unpack(">IIBB", chunk[:10])
            assert bit_depth == 8 and color_type == 2, path
        elif chunk_type == b"IDAT":
            compressed.extend(chunk)
        elif chunk_type == b"IEND":
            break

    raw = zlib.decompress(bytes(compressed))
    stride = width * 3
    rows: list[bytes] = []
    previous = bytearray(stride)
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        source = raw[cursor + 1 : cursor + 1 + stride]
        cursor += stride + 1
        row = bytearray(stride)
        for index, value in enumerate(source):
            left = row[index - 3] if index >= 3 else 0
            up = previous[index]
            upper_left = previous[index - 3] if index >= 3 else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                estimate = left + up - upper_left
                distances = (abs(estimate - left), abs(estimate - up), abs(estimate - upper_left))
                predictor = (left, up, upper_left)[distances.index(min(distances))]
            else:
                raise AssertionError(f"Unsupported PNG filter {filter_type}: {path}")
            row[index] = (value + predictor) & 0xFF
        rows.append(bytes(row))
        previous = row
    return width, height, rows


def assert_profile_raster(path: Path, expected_size: int) -> None:
    width, height, rows = png_rgb_pixels(path)
    assert (width, height) == (expected_size, expected_size)

    def pixel(x_unit: int, y_unit: int) -> tuple[int, int, int]:
        x = min(width - 1, round(width * x_unit / 64))
        y = min(height - 1, round(height * y_unit / 64))
        start = x * 3
        return tuple(rows[y][start : start + 3])

    shell = (247, 243, 233)
    green = (36, 122, 75)
    assert pixel(0, 0) == shell, f"{path}: profile canvas must use Shell"
    assert pixel(32, 8) == green, f"{path}: top of institutional O missing"
    assert pixel(32, 18) == shell, f"{path}: institutional counter missing"
    assert pixel(24, 25) == green, f"{path}: left canonical eye missing"
    assert pixel(24, 38) == green, f"{path}: left canonical U stem missing"


def main() -> None:
    validate_brand_geometry()
    validate_brand_system()
    validate_brand_exports()
    required = [
        "BRAND_ARCHITECTURE.md",
        "open-source.html",
        "styles.css",
        "studio.html",
        "studio.css",
        "studio-robots.txt",
        "studio-sitemap.xml",
        "favicon-v3.svg",
        "apple-touch-icon-v1.png",
        "icon-192-v1.png",
        "icon-512-v1.png",
        "site.webmanifest",
        "og-v6.png",
        "open-source-robots.txt",
        "open-source-sitemap.xml",
        "vercel.json",
        "publisher/index.html",
        "publisher/manifest.json",
        "legal/privacy.html",
        "legal/terms.html",
        "security.html",
        "support.html",
        "brand/README.md",
        "brand/manifest.json",
        "brand/ou-monitor-mark-v3.svg",
        "brand/ou-monitor-reverse-v3.svg",
        "brand/ou-monitor-character-v3.svg",
        "brand/ou-monitor-bot-v3.svg",
        "brand/ou-profile-mark-v1.svg",
        "brand/ou-profile-mark-v1.png",
        "brand/profile-mark-raster.html",
        "brand/ou-wordmark-v4.svg",
        "brand/ou-wordmark-reverse-v4.svg",
        "brand/ou-tagline-v4.svg",
        "brand/ou-tagline-reverse-v4.svg",
        "brand/ou-lockup-horizontal-v4.svg",
        "brand/ou-lockup-horizontal-reverse-v4.svg",
        "brand/ou-lockup-stacked-v4.svg",
        "brand/ou-lockup-stacked-reverse-v4.svg",
        "brand/brandkit-open-monitor-v5.png",
        "brand/monitorfolk-workshop.png",
        "brand/brandkit.html",
        "brand/og-card.html",
        "brand/media-kit.html",
        "brand/studio/open-graph.html",
        "brand/studio/openly-useful-studio-open-graph-1200x630.png",
        "brand/open-source/open-graph.html",
        "brand/open-source/openly-useful-open-source-open-graph-1200x630.png",
        "design-system/README.md",
        "design-system/ARCHITECTURE.md",
        "design-system/index.html",
        "design-system/brand.css",
        "design-system/tokens.css",
        "scripts/build_brand_vectors.py",
        "scripts/build_brand_exports.py",
        "scripts/validate_brand_exports.py",
        "scripts/requirements-vector.txt",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required site files: {', '.join(missing)}")
    for shadowing_path in ["index.html", "robots.txt", "sitemap.xml"]:
        assert not (ROOT / shadowing_path).exists(), f"{shadowing_path} would shadow a host-aware rewrite"

    html = (ROOT / "open-source.html").read_text(encoding="utf-8")
    parser = LandingPageParser()
    parser.feed(html)
    assert parser.title == "Openly Useful Open Source — Useful things, openly made."
    assert {"top", "projects", "principles", "about"}.issubset(parser.ids)
    assert "https://github.com/openly-useful" in [link.lower() for link in parser.links]
    assert "https://github.com/openly-useful/citewire" in [link.lower() for link in parser.links]
    assert "https://github.com/openly-useful/skill-feedback-engine" in [link.lower() for link in parser.links]
    assert "Agent Workflow Swarms" in html
    assert "https://github.com/openly-useful/agent-workflow-swarms" in [link.lower() for link in parser.links]
    assert "mailto:hello@openlyuseful.org" in parser.links
    assert "https://openlyuseful.org/brand/open-source/openly-useful-open-source-open-graph-1200x630.png" in html
    assert "https://openlyuseful.com" in parser.links
    assert "/design-system" in parser.links
    assert "/brand/ou-lockup-horizontal-v4.svg" in html
    assert "/brand/ou-lockup-stacked-v4.svg" in html
    assert "/brand/ou-profile-mark-v1.svg" in html
    assert "/apple-touch-icon-v1.png" in html
    assert "/site.webmanifest" in html
    assert "/brand/ou-monitor-bot-v3.svg" in html
    assert "open-shell" not in html
    assert "open-source collective" not in html.lower()
    assert "public benefit" not in html.lower()

    studio_html = (ROOT / "studio.html").read_text(encoding="utf-8")
    studio_parser = LandingPageParser()
    studio_parser.feed(studio_html)
    assert studio_parser.title == "Openly Useful Studio — Practical software, thoughtfully made."
    assert "Practical software." in studio_html
    assert "Thoughtfully made." in studio_html
    assert {"top", "work", "capabilities", "about"}.issubset(studio_parser.ids)
    assert "https://openlyuseful.org" in studio_parser.links
    assert "https://gloatroom.com" in studio_parser.links
    assert "mailto:hello@openlyuseful.org?subject=STUDIO" in studio_parser.links
    assert "hello@openlyuseful.com" not in studio_html
    assert "https://openlyuseful.com/brand/studio/openly-useful-studio-open-graph-1200x630.png" in studio_html
    assert "/brand/ou-lockup-horizontal-reverse-v4.svg" in studio_html
    assert "project status" not in studio_html.lower()
    assert "progressmark" not in studio_html.lower()

    publisher_urls = {
        "https://openlyuseful.org/publisher",
        "https://openlyuseful.org/support",
        "https://openlyuseful.org/legal/privacy",
        "https://openlyuseful.org/legal/terms",
        "https://openlyuseful.org/security",
    }
    public_footer_files = {
        "open-source.html": html,
        "studio.html": studio_html,
        "design-system/index.html": (ROOT / "design-system/index.html").read_text(encoding="utf-8"),
        "brand/media-kit.html": (ROOT / "brand/media-kit.html").read_text(encoding="utf-8"),
    }
    for name, public_html in public_footer_files.items():
        assert "OpenlyUseful.com: Studio" in public_html, name
        assert "OpenlyUseful.org: Open Source + publisher" in public_html, name
        assert "Planned legal entity: Openly Useful LLC" in public_html, name
        assert "formation-pending" in public_html, name
        footer_parser = LandingPageParser()
        footer_parser.feed(public_html)
        assert publisher_urls.issubset(footer_parser.links), name

    policy_pages = {
        "publisher/index.html": ("Publisher — Openly Useful", "https://openlyuseful.org/publisher"),
        "legal/privacy.html": ("Privacy — Openly Useful", "https://openlyuseful.org/legal/privacy"),
        "legal/terms.html": ("Terms — Openly Useful", "https://openlyuseful.org/legal/terms"),
        "security.html": ("Security — Openly Useful", "https://openlyuseful.org/security"),
        "support.html": ("Support — Openly Useful", "https://openlyuseful.org/support"),
    }
    formation_aware_files = dict(public_footer_files)
    for name, (expected_title, expected_canonical) in policy_pages.items():
        policy_html = (ROOT / name).read_text(encoding="utf-8")
        policy_parser = LandingPageParser()
        policy_parser.feed(policy_html)
        assert policy_parser.title == expected_title, name
        assert policy_parser.canonical == expected_canonical, name
        assert "Openly Useful LLC" in policy_html, name
        assert "formation-pending" in policy_html, name
        assert publisher_urls.issubset(policy_parser.links), name
        formation_aware_files[name] = policy_html

    support_html = formation_aware_files["support.html"]
    assert "mailto:hello@openlyuseful.org?subject=SUPPORT" in support_html
    assert "mailto:hello@openlyuseful.org?subject=SECURITY" in support_html
    assert 'href="/security"' in support_html
    security_html = formation_aware_files["security.html"]
    assert "mailto:hello@openlyuseful.org?subject=SECURITY" in security_html
    assert "security@openlyuseful.org" not in security_html
    assert "no guaranteed response time is offered" in security_html
    privacy_html = formation_aware_files["legal/privacy.html"]
    assert "founder-operated Openly Useful project is the current operator and data controller" in privacy_html
    terms_html = formation_aware_files["legal/terms.html"]
    assert "founder-operated Openly Useful project" in terms_html
    assert "current operator of the informational sites" in terms_html

    publisher = json.loads((ROOT / "publisher/manifest.json").read_text(encoding="utf-8"))
    assert publisher["schemaVersion"] == 1
    assert publisher["id"] == "openly-useful"
    assert publisher["displayName"] == "Openly Useful"
    assert publisher["authorityManifest"] == "https://openlyuseful.org/publisher/manifest.json"
    assert publisher["legal"] == {
        "plannedName": "Openly Useful LLC",
        "activeName": None,
        "status": "formation-pending",
        "plannedRoles": ["publisher", "operator", "licensee"],
    }
    assert publisher["domains"] == {
        "studio": "https://openlyuseful.com",
        "openSource": "https://openlyuseful.org",
        "publicAuthority": "openlyuseful.org",
    }
    assert publisher["organization"]["github"] == "https://github.com/Openly-Useful"
    assert publisher["contacts"] == {
        "public": "hello@openlyuseful.org",
        "routing": "Use the email subject to route publishing, security, legal, and support requests.",
    }
    assert publisher["policies"] == {
        "privacy": "https://openlyuseful.org/legal/privacy",
        "terms": "https://openlyuseful.org/legal/terms",
        "security": "https://openlyuseful.org/security",
        "support": "https://openlyuseful.org/support",
    }
    assert publisher["namespaces"] == {
        "npm": "@openly-useful",
        "openSourceMcp": "org.openlyuseful",
        "reservedStudioMcp": "com.openlyuseful",
    }
    assert publisher["publication"] == {
        "localGenerationAllowed": True,
        "localTestingAllowed": True,
        "externalPublicationAllowed": False,
        "authorization": "withheld",
        "blockingRequirements": [
            "formation-active",
            "publisher-authorization",
            "namespace-verification",
            "public-policy-url-verification",
        ],
    }
    assert "published authority endpoint" in publisher["artifactPolicy"]["authorityEndpoint"]
    assert "governed editable publisher source" in publisher["artifactPolicy"]["authorityEndpoint"]
    assert "sourceOfTruth" not in publisher["artifactPolicy"]
    assert "derive publisher identity" in publisher["artifactPolicy"]["derivation"]
    assert "must not be represented as formed" in publisher["artifactPolicy"]["activation"]
    assert "required publisher verification" in publisher["artifactPolicy"]["activation"]
    assert "ownership verification" not in publisher["artifactPolicy"]["activation"]

    formation_aware_files["README.md"] = (ROOT / "README.md").read_text(encoding="utf-8")
    formation_aware_files["BRAND_ARCHITECTURE.md"] = (ROOT / "BRAND_ARCHITECTURE.md").read_text(encoding="utf-8")
    forbidden_active_claims = {
        "operated by openly useful llc",
        "published by openly useful llc",
        "openly useful llc is active",
        "openly useful llc is the operator",
        "openly useful llc owns",
    }
    for name, public_text in formation_aware_files.items():
        lowered = public_text.lower()
        if "openly useful llc" in lowered:
            assert "formation-pending" in lowered, name
        assert "ownership verification" not in lowered, name
        for claim in forbidden_active_claims:
            assert claim not in lowered, f"{name}: premature legal-entity claim: {claim}"

    system_html = (ROOT / "design-system/index.html").read_text(encoding="utf-8")
    system_parser = LandingPageParser()
    system_parser.feed(system_html)
    assert system_parser.title == "Design System — Openly Useful"
    assert "The Open Monitor" in system_html
    assert "/brand/brandkit-open-monitor-v5.png" in system_html
    assert "/brand/ou-monitor-character-v3.svg" in system_html
    assert "Comfortable sharing" in system_html

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css
    assert "forced-colors" in css
    assert "@media (max-width:520px)" in css
    assert ".policy-shell" in css
    assert ".publisher-record" in css

    studio_css = (ROOT / "studio.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in studio_css
    assert "forced-colors" in studio_css
    assert "@media (max-width:560px)" in studio_css

    tokens = (ROOT / "design-system/tokens.css").read_text(encoding="utf-8")
    for token in [
        "--ou-color-shell-50",
        "--ou-color-ink-900",
        "--ou-color-terminal-600",
        "--ou-color-process-600",
        "--ou-font-sans",
        "--ou-space-4",
        "--ou-focus-ring",
    ]:
        assert token in tokens

    board = ROOT / "brand/brandkit-open-monitor-v5.png"
    assert board.stat().st_size > 100_000
    assert png_dimensions(board) == (1536, 1024)
    assert png_dimensions(ROOT / "brand/monitorfolk-workshop.png") == (704, 1024)
    assert png_dimensions(ROOT / "brand/social/openly-useful-open-graph-1200x630.png") == (1200, 630)
    assert png_dimensions(ROOT / "brand/studio/openly-useful-studio-open-graph-1200x630.png") == (1200, 630)
    assert png_dimensions(ROOT / "brand/open-source/openly-useful-open-source-open-graph-1200x630.png") == (1200, 630)
    assert_profile_raster(ROOT / "brand/ou-profile-mark-v1.png", 1024)
    assert_profile_raster(ROOT / "apple-touch-icon-v1.png", 180)
    assert_profile_raster(ROOT / "icon-192-v1.png", 192)
    assert_profile_raster(ROOT / "icon-512-v1.png", 512)

    web_manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    assert web_manifest["name"] == "Openly Useful"
    assert web_manifest["background_color"] == "#f7f3e9"
    assert web_manifest["theme_color"] == "#f7f3e9"
    assert {(icon["src"], icon["sizes"]) for icon in web_manifest["icons"]} == {
        ("/icon-192-v1.png", "192x192"),
        ("/icon-512-v1.png", "512x512"),
    }

    board_source = (ROOT / "brand/brandkit.html").read_text(encoding="utf-8")
    assert board_source.count("/brand/ou-monitor-mark-v3.svg") == 6
    assert board_source.count("/brand/ou-lockup-stacked-v4.svg") == 1
    assert board_source.count("/brand/ou-monitor-character-v3.svg") == 1
    assert "brandkit-open-monitor-source-tmp" not in board_source

    social_source = (ROOT / "brand/og-card.html").read_text(encoding="utf-8")
    assert social_source.count("/brand/ou-lockup-stacked-v4.svg") == 1

    media_kit = (ROOT / "brand/media-kit.html").read_text(encoding="utf-8")
    assert media_kit.count("/brand/ou-lockup-horizontal-v4.svg") == 1
    assert "/brand/ou-profile-mark-v1.png" in media_kit
    assert "/brand/social/openly-useful-open-graph-1200x630.png" in media_kit
    assert "/brand/press/openly-useful-lockup-primary-transparent-1600x289.png" in media_kit
    assert "/brand/templates/openly-useful-presentation-cover-1920x1080.png" in media_kit
    assert "One identity. Every useful surface." in media_kit

    sitemap = (ROOT / "open-source-sitemap.xml").read_text(encoding="utf-8")
    assert "https://openlyuseful.org/brand/media-kit.html" in sitemap
    for canonical_url in publisher_urls:
        assert canonical_url in sitemap
    studio_sitemap = (ROOT / "studio-sitemap.xml").read_text(encoding="utf-8")
    assert "https://openlyuseful.com/" in studio_sitemap

    vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    assert any(
        redirect["source"] == "/:path*"
        and redirect["destination"] == "https://openlyuseful.com/:path*"
        and redirect.get("has") == [{"type": "host", "value": "www.openlyuseful.com"}]
        for redirect in vercel["redirects"]
    )
    expected_canonical_redirects = {
        ("/publisher", "https://openlyuseful.org/publisher"),
        ("/publisher/:path*", "https://openlyuseful.org/publisher/:path*"),
        ("/legal/:path*", "https://openlyuseful.org/legal/:path*"),
        ("/security", "https://openlyuseful.org/security"),
        ("/support", "https://openlyuseful.org/support"),
    }
    actual_canonical_redirects = {
        (redirect["source"], redirect["destination"])
        for redirect in vercel["redirects"]
        if redirect.get("has") == [{"type": "host", "value": "openlyuseful.com"}]
        and redirect.get("permanent") is True
    }
    assert expected_canonical_redirects.issubset(actual_canonical_redirects)
    expected_rewrites = {
        ("/", "openlyuseful.com", "/studio"),
        ("/robots.txt", "openlyuseful.com", "/studio-robots.txt"),
        ("/sitemap.xml", "openlyuseful.com", "/studio-sitemap.xml"),
    }
    actual_rewrites = {
        (rewrite["source"], rewrite["has"][0]["value"], rewrite["destination"])
        for rewrite in vercel["rewrites"]
        if "has" in rewrite
    }
    assert expected_rewrites.issubset(actual_rewrites)
    assert [rewrite["source"] for rewrite in vercel["rewrites"]] == [
        "/",
        "/robots.txt",
        "/sitemap.xml",
        "/",
        "/robots.txt",
        "/sitemap.xml",
    ]
    assert {rewrite["source"]: rewrite["destination"] for rewrite in vercel["rewrites"] if "has" not in rewrite} == {
        "/": "/open-source",
        "/robots.txt": "/open-source-robots.txt",
        "/sitemap.xml": "/open-source-sitemap.xml",
    }
    print("Validated Openly Useful landing page")


if __name__ == "__main__":
    main()
