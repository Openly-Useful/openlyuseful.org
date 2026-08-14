from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_SURFACES = [
    "index.html",
    "design-system/index.html",
    "brand/brandkit.html",
    "brand/og-card.html",
]

DEPRECATED_PUBLIC_PATHS = [
    "/brand/ou-monitor-mark.svg",
    "/brand/ou-monitor-reverse.svg",
    "/brand/ou-monitor-character.svg",
    "/brand/ou-monitor-bot.svg",
    "/brand/open-shell-mark.svg",
    "/brand/open-shell-reverse.svg",
    "/brand/shellfolk-builder.svg",
    "/brand/brandkit-open-monitor.png",
    "/favicon.svg",
    "/og.png",
    "/og-v2.png",
    "/og-v3.png",
    "/og-v4.png",
]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def lockup_count(html: str) -> int:
    return len(re.findall(r'class="[^"]*\bou-lockup\b[^"]*"', html))


def component_text(html: str, class_name: str) -> list[str]:
    pattern = rf'<[^>]+class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>([^<]+)</[^>]+>'
    return [value.strip() for value in re.findall(pattern, html)]


def validate_brand_system() -> None:
    manifest = json.loads(read("brand/manifest.json"))
    assert manifest["brandVersion"] == "3.0.0"
    assert manifest["canonicalName"] == "Openly Useful"
    assert manifest["canonicalTagline"] == "Useful things, openly made."

    assets = manifest["assets"]
    for public_path in assets.values():
        assert public_path.startswith("/")
        assert (ROOT / public_path.removeprefix("/")).is_file(), public_path

    active_text = "\n".join(read(path) for path in ACTIVE_SURFACES)
    for deprecated in DEPRECATED_PUBLIC_PATHS:
        assert deprecated not in active_text, f"Deprecated brand path remains active: {deprecated}"
    assert set(component_text(active_text, "ou-lockup__wordmark")) == {manifest["canonicalName"]}
    assert set(component_text(active_text, "ou-lockup__tagline")) == {manifest["canonicalTagline"]}

    institutional = assets["institutional"]
    reverse = assets["reverse"]
    character = assets["character"]
    monitorfolk = assets["monitorfolk"]

    home = read("index.html")
    assert lockup_count(home) == 3
    assert home.count(institutional) == 2
    assert home.count(reverse) == 1
    assert home.count(monitorfolk) == 1
    assert home.count('class="ou-lockup__wordmark"') == 3
    assert home.count('class="ou-lockup__tagline"') == 1

    specimen = read("design-system/index.html")
    assert lockup_count(specimen) == 4
    assert institutional in specimen
    assert reverse in specimen
    assert character in specimen
    assert assets["brandBoard"] in specimen

    board = read("brand/brandkit.html")
    assert lockup_count(board) == 1
    assert board.count(institutional) == 7
    assert board.count(character) == 1

    social = read("brand/og-card.html")
    assert social.count('class="identity ou-lockup ou-lockup--stacked ou-lockup--social"') == 1
    assert social.count(institutional) == 1

    brand_css = read("design-system/brand.css")
    tokens = read("design-system/tokens.css")
    for required in [
        "@font-face",
        ".ou-lockup--horizontal",
        ".ou-lockup--stacked",
        ".ou-lockup__wordmark",
        ".ou-lockup__tagline",
    ]:
        assert required in brand_css
    for required in [
        "--ou-brand-wordmark-weight: 780",
        "--ou-brand-wordmark-tracking: -.062em",
        "--ou-brand-tagline-weight: 700",
        "--ou-brand-tagline-tracking: -.035em",
        "--ou-brand-horizontal-compensation: 2.25rem",
    ]:
        assert required in tokens

    other_css = read("styles.css") + board + social
    assert not re.search(r"\.ou-lockup__wordmark\s*\{", other_css)
    assert not re.search(r"\.ou-lockup__tagline\s*\{", other_css)

    fonts = manifest["fonts"]
    for public_path in fonts.values():
        assert public_path.startswith("/")
        assert (ROOT / public_path.removeprefix("/")).is_file(), public_path
    for key in ["wordmark", "technical"]:
        assert (ROOT / fonts[key].removeprefix("/")).stat().st_size > 20_000

    vercel = read("vercel.json")
    for deprecated in DEPRECATED_PUBLIC_PATHS:
        assert f'"source": "{deprecated}"' in vercel, f"Missing compatibility redirect: {deprecated}"


def main() -> None:
    validate_brand_system()
    print("Validated Openly Useful brand system")


if __name__ == "__main__":
    main()
