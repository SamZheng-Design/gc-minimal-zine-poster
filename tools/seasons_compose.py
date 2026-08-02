#!/usr/bin/env python3
"""
Seasons series compositor.

The four Seasons sheets are NOT laid out by the image model. The model only
produces the square photographic plate for each season; every millimetre of the
page — paper, plate position, type, rule, colour chop, print defects — is placed
here in code, from one shared geometry table.

That is what makes the series consistent: the four sheets are not "similar",
they are pixel-identical everywhere except the photograph and the one accent
colour.

Inputs  : assets/seasons/paper.jpeg          shared aged-paper background
          assets/seasons/plate-<season>.jpeg square duotone photograph
Outputs : posters/img/<id>-seasons-<season>.jpeg

Usage   : python3 tools/seasons_compose.py [--out DIR] [--full]
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --------------------------------------------------------------------------
# Sheet geometry — one table, shared by all four sheets. Fractions of the
# sheet width (W) or height (H) so the design is resolution independent.
# --------------------------------------------------------------------------

W, H = 1536, 2752  # 9:16 working canvas, matches the rest of the album

PLATE_SIDE = 0.560  # of W  -> square photographic plate
PLATE_TOP = 0.200  # of H  -> top edge of the plate

WORD_TOP = 0.575  # of H  -> cap-height top of the season word
WORD_SIZE = 0.042  # of H
WORD_TRACK = 0.34  # extra letterspacing, in em

HANZI_TOP = 0.618  # of H
HANZI_SIZE = 0.030  # of H

RULE_Y = 0.668  # of H  -> hairline rule, spans the plate width
RULE_W = 2  # px

INDEX_TOP = 0.682  # of H  -> left-aligned to the plate, clear of the chop
INDEX_SIZE = 0.0115  # of H
INDEX_TRACK = 0.22  # em

CHOP_AREA = 0.016  # of the whole canvas (spec band: 0.008-0.025)
CHOP_MISREG = (7, -5)  # px offset of the grey ghost behind the chop

# --------------------------------------------------------------------------
# Ink palette — shared. Only ACCENT changes between sheets.
# --------------------------------------------------------------------------

INK_TEXT = (74, 68, 60)  # warm dark grey, the only type colour
INK_RULE = (150, 141, 127)  # lighter warm grey
INK_GHOST = (176, 168, 155)  # misregistration ghost behind the chop

DUOTONE_HI = (240, 233, 218)  # plate highlight -> just off the paper tone
DUOTONE_LO = (72, 62, 50)  # plate shadow -> warm sepia black

FONT_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_CJK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Light.ttc"
FONT_CJK_INDEX = 2  # SC face inside the .ttc


@dataclass(frozen=True)
class Season:
    n: int  # 1..4, drives the index line
    poster_id: int  # id in posters/index.json
    key: str  # spring / summer / ...
    word: str  # SPRING
    hanzi: str  # 春
    accent: str  # #EE4C7C


SEASONS = (
    Season(1, 28, "spring", "SPRING", "春", "#EE4C7C"),
    Season(2, 29, "summer", "SUMMER", "夏", "#12A150"),
    Season(3, 30, "autumn", "AUTUMN", "秋", "#E8541C"),
    Season(4, 31, "winter", "WINTER", "冬", "#00A9DE"),
)


def hex_rgb(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


# --------------------------------------------------------------------------
# Pieces
# --------------------------------------------------------------------------


def load_paper(path: str) -> Image.Image:
    """Shared background, cropped to the working canvas. Identical every time."""
    paper = Image.open(path).convert("RGB")
    scale = max(W / paper.width, H / paper.height)
    paper = paper.resize(
        (round(paper.width * scale), round(paper.height * scale)), Image.LANCZOS
    )
    left = (paper.width - W) // 2
    top = (paper.height - H) // 2
    return paper.crop((left, top, left + W, top + H))


def duotone(plate: Image.Image, side: int) -> Image.Image:
    """
    Force the photograph onto one shared warm grey-sepia ramp.

    The model is asked for a duotone, but it never lands on exactly the same
    hue twice. Remapping here means the four plates cannot drift apart: the
    base-plate colour is literally the same ramp for all of them.
    """
    plate = plate.convert("RGB").resize((side, side), Image.LANCZOS)
    lum = np.asarray(plate.convert("L")).astype(np.float32) / 255.0

    # gentle S-curve: keep it low-contrast, no crushed blacks, no blown whites
    lum = np.clip(lum, 0.0, 1.0)
    lum = 0.10 + 0.82 * (lum ** 1.05)

    lo = np.array(DUOTONE_LO, dtype=np.float32)
    hi = np.array(DUOTONE_HI, dtype=np.float32)
    out = lo + (hi - lo) * lum[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def soft_edge_mask(side: int, feather: int = 5) -> Image.Image:
    """Ink bleed: the plate edge is soft, not a crisp digital cut."""
    m = Image.new("L", (side, side), 0)
    ImageDraw.Draw(m).rectangle(
        (feather, feather, side - 1 - feather, side - 1 - feather), fill=255
    )
    return m.filter(ImageFilter.GaussianBlur(feather * 0.9))


def draw_tracked(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    track_px: float,
    cx: int,
    top: int,
    fill: tuple[int, int, int],
) -> None:
    """Letterspaced, centred on cx. Drawn glyph by glyph so tracking is exact."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + track_px * (len(text) - 1)
    x = cx - total / 2.0
    for ch, w in zip(text, widths):
        draw.text((x, top), ch, font=font, fill=fill, anchor="lt")
        x += w + track_px


def paper_grain(img: Image.Image, paper: Image.Image) -> Image.Image:
    """Pull the shared paper fibre back over the printed elements."""
    grain = np.asarray(paper.convert("L")).astype(np.float32) / 255.0
    grain = 1.0 - (1.0 - grain) * 0.22  # very light multiply
    base = np.asarray(img).astype(np.float32)
    return Image.fromarray(
        np.clip(base * grain[..., None], 0, 255).astype(np.uint8), "RGB"
    )


# --------------------------------------------------------------------------
# Compose
# --------------------------------------------------------------------------


def compose(season: Season, src: str, paper: Image.Image) -> Image.Image:
    sheet = paper.copy()

    # ---- square photographic plate -------------------------------------
    side = round(PLATE_SIDE * W)
    px = (W - side) // 2  # horizontally centred, always
    py = round(PLATE_TOP * H)
    plate = duotone(Image.open(os.path.join(src, f"plate-{season.key}.jpeg")), side)
    sheet.paste(plate, (px, py), soft_edge_mask(side))

    draw = ImageDraw.Draw(sheet)
    cx = W // 2

    # ---- type block ------------------------------------------------------
    word_font = ImageFont.truetype(FONT_SERIF, round(WORD_SIZE * H))
    draw_tracked(
        draw,
        season.word,
        word_font,
        WORD_TRACK * WORD_SIZE * H,
        cx,
        round(WORD_TOP * H),
        INK_TEXT,
    )

    hanzi_font = ImageFont.truetype(FONT_CJK, round(HANZI_SIZE * H), index=FONT_CJK_INDEX)
    draw.text(
        (cx, round(HANZI_TOP * H)), season.hanzi, font=hanzi_font, fill=INK_TEXT, anchor="mt"
    )

    # ---- hairline rule, exactly the plate width --------------------------
    ry = round(RULE_Y * H)
    draw.rectangle((px, ry, px + side, ry + RULE_W - 1), fill=INK_RULE)

    # ---- index line ------------------------------------------------------
    # Left-aligned to the plate edge so the chop can own the right end of the
    # rule without ever printing over type.
    index_font = ImageFont.truetype(FONT_SERIF, round(INDEX_SIZE * H))
    index_track = INDEX_TRACK * INDEX_SIZE * H
    index_text = f"SEASONS 0{season.n} / 04"
    index_w = (
        sum(draw.textlength(ch, font=index_font) for ch in index_text)
        + index_track * (len(index_text) - 1)
    )
    draw_tracked(
        draw,
        index_text,
        index_font,
        index_track,
        round(px + index_w / 2),
        round(INDEX_TOP * H),
        INK_RULE,
    )

    # ---- the one high-chroma accent --------------------------------------
    # Solid square chop resting on the right end of the rule. Its side is
    # derived from the target area so the accent lands inside the spec band
    # by construction rather than by luck.
    chop = round((CHOP_AREA * W * H) ** 0.5)
    x1 = px + side
    x0 = x1 - chop
    y0 = ry - chop // 2
    y1 = y0 + chop

    dx, dy = CHOP_MISREG
    draw.rectangle((x0 + dx, y0 + dy, x1 + dx, y1 + dy), fill=INK_GHOST)  # misregistration
    draw.rectangle((x0, y0, x1, y1), fill=hex_rgb(season.accent))

    return paper_grain(sheet, paper)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="posters/img")
    ap.add_argument("--src", default="assets/seasons")
    ap.add_argument("--full", action="store_true", help="keep full 1536px width")
    args = ap.parse_args()

    paper = load_paper(os.path.join(args.src, "paper.jpeg"))
    os.makedirs(args.out, exist_ok=True)

    for s in SEASONS:
        sheet = compose(s, args.src, paper)
        if not args.full:
            nh = round(sheet.height * 1200 / sheet.width)
            sheet = sheet.resize((1200, nh), Image.LANCZOS)
        path = os.path.join(args.out, f"{s.poster_id}-seasons-{s.key}.jpeg")
        sheet.save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"wrote {path}  {sheet.width}x{sheet.height}")


if __name__ == "__main__":
    main()
