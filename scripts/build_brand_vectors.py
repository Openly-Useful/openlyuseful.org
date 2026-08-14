from __future__ import annotations

from dataclasses import dataclass
from html import escape
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.roundingPen import RoundingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]

INK = "#171a18"
GREEN = "#247a4b"
GREEN_STRONG = "#185f39"
GREEN_LIGHT = "#7ec693"
SHELL = "#f7f3e9"


@dataclass(frozen=True)
class Outline:
    paths: tuple[str, ...]
    width: float
    height: float


def number(value: float) -> str:
    rounded = round(value, 3)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.3f}".rstrip("0").rstrip(".")


def outlined_text(
    font_path: Path,
    text: str,
    *,
    weight: int,
    tracking: int,
    scale_x: float = 1,
) -> Outline:
    source_font = TTFont(font_path)
    source_font.flavor = None
    buffer = BytesIO()
    source_font.save(buffer)

    face = hb.Face(buffer.getvalue())
    shaped_font = hb.Font(face)
    shaped_font.scale = (face.upem, face.upem)
    shaped_font.set_variations({"wght": weight})
    shaped = hb.Buffer()
    shaped.add_str(text)
    shaped.guess_segment_properties()
    hb.shape(shaped_font, shaped, {"kern": True})

    static_font = instantiateVariableFont(source_font, {"wght": weight}, inplace=False)
    glyph_set = static_font.getGlyphSet()
    glyph_order = static_font.getGlyphOrder()

    bounds = BoundsPen(glyph_set)
    cursor_x = 0
    shaped_glyphs = list(zip(shaped.glyph_infos, shaped.glyph_positions))
    for index, (info, position) in enumerate(shaped_glyphs):
        transform = TransformPen(
            bounds,
            (
                scale_x,
                0,
                0,
                -1,
                scale_x * (cursor_x + position.x_offset),
                -position.y_offset,
            ),
        )
        glyph_set[glyph_order[info.codepoint]].draw(transform)
        cursor_x += position.x_advance
        if index < len(shaped_glyphs) - 1:
            cursor_x += tracking

    if bounds.bounds is None:
        raise RuntimeError(f"No outline generated for {text!r}")
    left, top, right, bottom = bounds.bounds

    paths: list[str] = []
    cursor_x = 0
    for index, (info, position) in enumerate(shaped_glyphs):
        path_pen = SVGPathPen(glyph_set)
        rounded_pen = RoundingPen(path_pen, roundFunc=lambda value: round(value, 3))
        transform = TransformPen(
            rounded_pen,
            (
                scale_x,
                0,
                0,
                -1,
                scale_x * (cursor_x + position.x_offset) - left,
                -position.y_offset - top,
            ),
        )
        glyph_set[glyph_order[info.codepoint]].draw(transform)
        paths.append(path_pen.getCommands())
        cursor_x += position.x_advance
        if index < len(shaped_glyphs) - 1:
            cursor_x += tracking

    return Outline(tuple(paths), right - left, bottom - top)


def paths_fragment(outline: Outline, fill: str, *, indent: str = "  ") -> str:
    return "\n".join(
        f'{indent}<path fill="{fill}" d="{escape(path)}"/>' for path in outline.paths
    )


def mark_fragment(fill: str, *, transform: str, indent: str = "  ") -> str:
    root = ElementTree.parse(ROOT / "brand/ou-monitor-mark-v3.svg").getroot()
    shapes = []
    for element in root:
        tag = element.tag.rsplit("}", 1)[-1]
        if tag not in {"path", "rect"}:
            continue
        attributes = dict(element.attrib)
        if "fill" in attributes:
            attributes["fill"] = fill
        serialized = " ".join(
            f'{key}="{escape(value)}"' for key, value in attributes.items()
        )
        shapes.append(f"{indent}  <{tag} {serialized}/>")
    return f'{indent}<g transform="{transform}">\n' + "\n".join(shapes) + f"\n{indent}</g>"


def svg_document(
    *,
    title: str,
    description: str,
    width: float,
    height: float,
    body: str,
) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {number(width)} {number(height)}" role="img" '
        'aria-labelledby="title desc" shape-rendering="geometricPrecision">\n'
        f'  <title id="title">{escape(title)}</title>\n'
        f'  <desc id="desc">{escape(description)}</desc>\n'
        f"{body}\n"
        "</svg>\n"
    )


def write(relative_path: str, content: str) -> None:
    (ROOT / relative_path).write_text(content, encoding="utf-8")


def build_lockups(wordmark: Outline, tagline: Outline) -> None:
    # Horizontal lockup uses the same proportions as the former 34 px mark,
    # 18 px wordmark, and 10 px gap, but freezes those relationships in paths.
    horizontal_height = 64
    horizontal_word_scale = (18 / 34) * horizontal_height / 1000
    horizontal_gap = (10 / 34) * horizontal_height
    horizontal_word_width = wordmark.width * horizontal_word_scale
    horizontal_word_height = wordmark.height * horizontal_word_scale
    horizontal_word_x = horizontal_height + horizontal_gap
    horizontal_word_y = (horizontal_height - horizontal_word_height) / 2
    horizontal_width = horizontal_word_x + horizontal_word_width

    for reverse in (False, True):
        mark_fill = SHELL if reverse else GREEN
        word_fill = SHELL if reverse else INK
        suffix = "-reverse" if reverse else ""
        body = "\n".join(
            [
                mark_fragment(mark_fill, transform="scale(1)"),
                f'  <g transform="translate({number(horizontal_word_x)} {number(horizontal_word_y)}) scale({number(horizontal_word_scale)})">',
                paths_fragment(wordmark, word_fill, indent="    "),
                "  </g>",
            ]
        )
        write(
            f"brand/ou-lockup-horizontal{suffix}-v4.svg",
            svg_document(
                title="Openly Useful horizontal lockup",
                description="The Open Monitor mark and the Openly Useful wordmark in one fixed vector composition.",
                width=horizontal_width,
                height=horizontal_height,
                body=body,
            ),
        )

    # Stacked lockup is built on the established 1,000-unit component scale.
    # All three pieces, including their clear space, now scale as one asset.
    unit = 1000
    mark_box = 4 * unit
    word_scale = 1.047619
    word_gap = 0.321429 * unit
    tagline_scale = 0.261905
    tagline_gap = 0.238095 * unit
    stacked_width = wordmark.width * word_scale
    word_height = wordmark.height * word_scale
    tagline_width = tagline.width * tagline_scale
    tagline_height = tagline.height * tagline_scale
    word_y = mark_box + word_gap
    tagline_y = word_y + word_height + tagline_gap
    stacked_height = tagline_y + tagline_height
    mark_x = (stacked_width - mark_box) / 2
    tagline_x = (stacked_width - tagline_width) / 2

    for reverse in (False, True):
        mark_fill = SHELL if reverse else GREEN
        word_fill = SHELL if reverse else INK
        tagline_fill = GREEN_LIGHT if reverse else GREEN_STRONG
        suffix = "-reverse" if reverse else ""
        body = "\n".join(
            [
                mark_fragment(
                    mark_fill,
                    transform=f"translate({number(mark_x)} 0) scale({number(mark_box / 64)})",
                ),
                f'  <g transform="translate(0 {number(word_y)}) scale({number(word_scale)})">',
                paths_fragment(wordmark, word_fill, indent="    "),
                "  </g>",
                f'  <g transform="translate({number(tagline_x)} {number(tagline_y)}) scale({number(tagline_scale)})">',
                paths_fragment(tagline, tagline_fill, indent="    "),
                "  </g>",
            ]
        )
        write(
            f"brand/ou-lockup-stacked{suffix}-v4.svg",
            svg_document(
                title="Openly Useful stacked lockup",
                description="The Open Monitor mark, Openly Useful wordmark, and Useful things, openly made tagline in one fixed vector composition.",
                width=stacked_width,
                height=stacked_height,
                body=body,
            ),
        )


def main() -> None:
    wordmark = outlined_text(
        ROOT / "design-system/fonts/AtkinsonHyperlegibleNext-variable.woff2",
        "Openly Useful",
        weight=780,
        tracking=-62,
        scale_x=1.34,
    )
    tagline = outlined_text(
        ROOT / "design-system/fonts/IBMPlexMono-variable-latin1.woff2",
        "Useful things, openly made.",
        weight=700,
        tracking=-35,
    )

    write(
        "brand/ou-wordmark-v4.svg",
        svg_document(
            title="Openly Useful wordmark",
            description="The canonical Openly Useful wordmark converted to fixed vector outlines.",
            width=wordmark.width,
            height=wordmark.height,
            body=paths_fragment(wordmark, INK),
        ),
    )
    write(
        "brand/ou-wordmark-reverse-v4.svg",
        svg_document(
            title="Openly Useful reverse wordmark",
            description="The canonical Openly Useful wordmark in the light reverse color.",
            width=wordmark.width,
            height=wordmark.height,
            body=paths_fragment(wordmark, SHELL),
        ),
    )
    write(
        "brand/ou-tagline-v4.svg",
        svg_document(
            title="Useful things, openly made",
            description="The canonical Openly Useful tagline converted to fixed vector outlines.",
            width=tagline.width,
            height=tagline.height,
            body=paths_fragment(tagline, GREEN_STRONG),
        ),
    )
    write(
        "brand/ou-tagline-reverse-v4.svg",
        svg_document(
            title="Useful things, openly made reverse tagline",
            description="The canonical Openly Useful tagline in the light reverse color.",
            width=tagline.width,
            height=tagline.height,
            body=paths_fragment(tagline, GREEN_LIGHT),
        ),
    )
    build_lockups(wordmark, tagline)
    print("Built outlined Openly Useful brand vectors")


if __name__ == "__main__":
    main()
