from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"
GREEN = "#247a4b"
SHELL = "#f7f3e9"

MARK_U = "M20.5 34h7v4c0 3 1.5 4.5 4.5 4.5s4.5-1.5 4.5-4.5v-4h7v4c0 6.2-3.8 9.5-11.5 9.5S20.5 44.2 20.5 38v-4Z"
CHARACTER_U = "M20.5 40h7v4c0 3 1.5 4.5 4.5 4.5s4.5-1.5 4.5-4.5v-4h7v4c0 6.2-3.8 9.5-11.5 9.5S20.5 50.2 20.5 44v-4Z"


def parse(relative_path: str) -> ElementTree.Element:
    return ElementTree.parse(ROOT / relative_path).getroot()


def face_rects(root: ElementTree.Element, *, y: float) -> list[ElementTree.Element]:
    return sorted(
        [
            rect
            for rect in root.iter(f"{SVG}rect")
            if float(rect.get("y", "-1")) == y
            and float(rect.get("width", "-1")) == 7
            and float(rect.get("height", "-1")) == 9
        ],
        key=lambda rect: float(rect.get("x", "0")),
    )


def validate_face(
    relative_path: str,
    *,
    eye_y: float,
    u_path: str,
    u_top: float,
    u_bottom: float,
    counter_bottom: float,
    eye_color: str,
    u_color: str,
) -> None:
    root = parse(relative_path)
    assert root.get("shape-rendering") == "geometricPrecision", relative_path

    eyes = face_rects(root, y=eye_y)
    assert len(eyes) == 2, f"{relative_path}: expected two canonical eyes"
    centers = [float(eye.get("x", "0")) + float(eye.get("width", "0")) / 2 for eye in eyes]
    assert centers == [24, 40], f"{relative_path}: eyes must align to U stem centers"
    assert all(eye.get("fill") == eye_color for eye in eyes), relative_path

    eye_bottom = eye_y + 9
    assert u_top - eye_bottom == 4, f"{relative_path}: eye/U gap must remain four units"
    assert counter_bottom - u_bottom == 2.5, f"{relative_path}: U/O gap must remain 2.5 units"

    u_matches = [path for path in root.iter(f"{SVG}path") if path.get("d") == u_path]
    assert len(u_matches) == 1, f"{relative_path}: canonical filled U geometry missing"
    assert u_matches[0].get("fill") == u_color, relative_path
    assert u_matches[0].get("stroke") is None, f"{relative_path}: U must not use a stroked cap"


def validate_bot() -> None:
    root = parse("brand/ou-monitor-bot-v3.svg")
    face = next((group for group in root.iter(f"{SVG}g") if group.get("id") == "canonical-face"), None)
    assert face is not None, "Monitorfolk must contain the canonical face group"
    assert face.get("transform") == "translate(82 15) scale(4)"
    assert face.get("stroke") == "none"

    eyes = face_rects(face, y=21)
    assert len(eyes) == 2
    centers = [float(eye.get("x", "0")) + 3.5 for eye in eyes]
    assert centers == [24, 40], "Monitorfolk must reuse canonical eye centerlines"
    assert all(eye.get("fill") == SHELL for eye in eyes)

    u_matches = [path for path in face.iter(f"{SVG}path") if path.get("d") == MARK_U]
    assert len(u_matches) == 1, "Monitorfolk must reuse the canonical filled U path"
    assert u_matches[0].get("fill") == GREEN


def validate_profile_mark() -> None:
    canonical = parse("brand/ou-monitor-mark-v3.svg")
    profile = parse("brand/ou-profile-mark-v1.svg")
    canonical_shapes = [
        (element.tag.rsplit("}", 1)[-1], element.attrib)
        for element in canonical.iter()
        if element.tag.rsplit("}", 1)[-1] in {"path", "rect"}
    ]
    profile_shapes = [
        (element.tag.rsplit("}", 1)[-1], element.attrib)
        for element in profile.iter()
        if element.tag.rsplit("}", 1)[-1] in {"path", "rect"}
        and not (element.get("width") == "64" and element.get("height") == "64")
    ]
    assert profile_shapes == canonical_shapes, "Profile mark must embed the institutional shapes unchanged"


def validate_brand_geometry() -> None:
    validate_face(
        "brand/ou-monitor-mark-v3.svg",
        eye_y=21,
        u_path=MARK_U,
        u_top=34,
        u_bottom=47.5,
        counter_bottom=50,
        eye_color=GREEN,
        u_color=GREEN,
    )
    validate_face(
        "brand/ou-monitor-reverse-v3.svg",
        eye_y=21,
        u_path=MARK_U,
        u_top=34,
        u_bottom=47.5,
        counter_bottom=50,
        eye_color=SHELL,
        u_color=SHELL,
    )
    validate_face(
        "favicon-v3.svg",
        eye_y=21,
        u_path=MARK_U,
        u_top=34,
        u_bottom=47.5,
        counter_bottom=50,
        eye_color=GREEN,
        u_color=GREEN,
    )
    validate_face(
        "brand/ou-profile-mark-v1.svg",
        eye_y=21,
        u_path=MARK_U,
        u_top=34,
        u_bottom=47.5,
        counter_bottom=50,
        eye_color=GREEN,
        u_color=GREEN,
    )
    validate_face(
        "brand/ou-monitor-character-v3.svg",
        eye_y=27,
        u_path=CHARACTER_U,
        u_top=40,
        u_bottom=53.5,
        counter_bottom=56,
        eye_color=SHELL,
        u_color=GREEN,
    )
    validate_bot()
    validate_profile_mark()


def main() -> None:
    validate_brand_geometry()
    print("Validated Openly Useful brand geometry")


if __name__ == "__main__":
    main()
