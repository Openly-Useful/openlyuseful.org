from __future__ import annotations

import hashlib
import json
from pathlib import Path
from struct import unpack
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_KEYS = {
    "openGraph",
    "githubPreview",
    "linkedinShare",
    "communityHeader",
    "linkedinCover",
    "instagramSquare",
    "instagramPortrait",
    "storyReel",
    "youtubeBanner",
    "youtubeThumbnail",
    "presentationCover",
    "documentCover",
    "emailSignature",
    "pressMarkPrimary",
    "pressMarkReverse",
    "pressLockupPrimary",
    "pressLockupReverse",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_header(path: Path) -> tuple[int, int, int]:
    with path.open("rb") as image:
        assert image.read(8) == b"\x89PNG\r\n\x1a\n", path
        assert image.read(4) == b"\x00\x00\x00\r", path
        assert image.read(4) == b"IHDR", path
        width, height, bit_depth, color_type = unpack(">IIBB", image.read(10))
        assert bit_depth == 8, path
        return width, height, color_type


def local_tag(element: ElementTree.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def path_data(element: ElementTree.Element) -> list[str]:
    return [
        descendant.get("d", "")
        for descendant in element.iter()
        if local_tag(descendant) == "path"
    ]


def validate_embedded_sources(root: ElementTree.Element, source_path: Path) -> None:
    embedded = [element for element in root.iter() if element.get("data-source")]
    assert embedded, f"{source_path}: no canonical vector source recorded"
    for group in embedded:
        public_path = group.get("data-source", "")
        assert public_path.startswith("/brand/"), (source_path, public_path)
        canonical = ROOT / public_path.removeprefix("/")
        assert canonical.is_file(), (source_path, public_path)
        assert group.get("data-source-sha256") == sha256(canonical), (
            source_path,
            public_path,
            "source hash drift",
        )
        canonical_root = ElementTree.parse(canonical).getroot()
        assert path_data(group) == path_data(canonical_root), (
            source_path,
            public_path,
            "embedded logo paths diverged",
        )


def validate_svg(path: Path, width: int, height: int) -> None:
    root = ElementTree.parse(path).getroot()
    assert root.get("width") == str(width), path
    assert root.get("height") == str(height), path
    assert root.get("viewBox") == f"0 0 {width} {height}", path
    assert root.get("shape-rendering") == "geometricPrecision", path
    forbidden = {"script", "foreignObject", "text"}
    assert not any(local_tag(element) in forbidden for element in root.iter()), path
    validate_embedded_sources(root, path)
    for element in root.iter():
        raster = element.get("data-raster-source")
        if raster:
            assert raster.startswith("/brand/"), (path, raster)
            assert (ROOT / raster.removeprefix("/")).is_file(), (path, raster)
            assert element.get("href", "").startswith("data:image/png;base64,"), (path, raster)


def validate_brand_exports() -> None:
    manifest_path = ROOT / "brand/social/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schemaVersion"] == 1
    assert manifest["kitVersion"] == "1.0.0"
    assert manifest["brandVersion"] == "3.1.0"
    assert manifest["canonicalProfileAsset"] == "/brand/ou-profile-mark-v1.png"
    assert manifest["canonicalTagline"] == "Useful things, openly made."
    assert manifest["platformSpecsVerified"] == "2026-08-14"

    exports = manifest["exports"]
    assert {export["key"] for export in exports} == EXPECTED_KEYS
    assert len(exports) == len(EXPECTED_KEYS)

    by_key = {export["key"]: export for export in exports}
    for export in exports:
        width = export["width"]
        height = export["height"]
        source = export["source"]
        output = export["output"]
        assert source.startswith("/brand/") and source.endswith(".svg"), source
        assert output.startswith("/brand/") and output.endswith(".png"), output
        source_path = ROOT / source.removeprefix("/")
        output_path = ROOT / output.removeprefix("/")
        assert source_path.is_file(), source
        assert output_path.is_file(), output
        validate_svg(source_path, width, height)
        png_width, png_height, color_type = png_header(output_path)
        assert (png_width, png_height) == (width, height), output
        assert color_type == (2 if export["opaque"] else 6), output
        assert output_path.stat().st_size > 4_000, output
        assert export["sha256"] == sha256(output_path), output
        safe_x, safe_y, safe_width, safe_height = export["safe_area"]
        assert 0 <= safe_x < width and 0 <= safe_y < height, export["key"]
        assert safe_width > 0 and safe_height > 0, export["key"]
        assert safe_x + safe_width <= width, export["key"]
        assert safe_y + safe_height <= height, export["key"]
        assert export["platforms"], export["key"]

    assert (ROOT / by_key["githubPreview"]["output"].removeprefix("/")).stat().st_size < 1_000_000
    for key in ["linkedinShare", "linkedinCover"]:
        assert (ROOT / by_key[key]["output"].removeprefix("/")).stat().st_size < 3_000_000
    assert (ROOT / by_key["youtubeBanner"]["output"].removeprefix("/")).stat().st_size < 6_000_000
    assert (ROOT / by_key["communityHeader"]["output"].removeprefix("/")).stat().st_size < 2_000_000

    brand_manifest = json.loads((ROOT / "brand/manifest.json").read_text(encoding="utf-8"))
    kits = brand_manifest["exportKits"]
    assert kits["social"]["version"] == manifest["kitVersion"]
    assert kits["social"]["manifest"] == "/brand/social/manifest.json"
    assert kits["mediaKit"] == "/brand/media-kit.html"
    assert (ROOT / kits["mediaKit"].removeprefix("/")).is_file()
    for kit in [kits["social"], kits["press"], kits["templates"]]:
        for public_path in kit.values():
            if not isinstance(public_path, str) or not public_path.startswith("/"):
                continue
            assert (ROOT / public_path.removeprefix("/")).is_file(), public_path


def main() -> None:
    validate_brand_exports()
    print("Validated Openly Useful brand exports")


if __name__ == "__main__":
    main()
