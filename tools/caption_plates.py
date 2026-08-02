#!/usr/bin/env python3
"""Print each Seasons sheet's title and note onto the sheet itself.

The poster is never touched and never resized. It is mounted at full size on a
larger sheet of the covers' paper, with a mat on all four sides, and the caption
is set on the paper below it — the way a plate is tipped into a book.

The mat is not decoration. Every sheet carries the printing vignette the skill
asks for, so its bottom edge is about 13 levels darker than bare paper; butting
a caption straight onto it would read as a seam. Surrounding the plate turns
that edge into what it actually is: the edge of the plate.

    python3 tools/caption_plates.py            # all of 28-45
    python3 tools/caption_plates.py --id 32    # one sheet
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "posters" / "index.json"
IMGDIR = REPO / "posters" / "img"
PAPER = REPO / "assets" / "seasons" / "paper.jpeg"
OUTDIR = REPO / "posters" / "plates"
COVER_REF = IMGDIR / "28-seasons-spring.jpeg"

PLATE_W = 1200                # archive width, mounted 1:1, never rescaled
MAT = 103                     # paper margin on the left, right and top
W = PLATE_W + 2 * MAT         # sheet width -> 1406
COL_X = MAT                   # caption aligns to the plate's left edge
COL_W = round(0.560 * PLATE_W)  # cover column width -> 672

GRAIN_STRENGTH = 0.22         # identical to seasons_compose.py
WHITE_PERCENTILE = 85.0

INK_TEXT = (74, 68, 60)       # cover body ink
INK_RULE = (150, 141, 127)
INK_FAINT = (163, 154, 141)

F_CJK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Light.ttc"
F_CJK_I = 2                   # SC face inside the .ttc
F_LAT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

PAD_TOP = 96                  # blank paper between image and caption
SWATCH = 11
GAP_SWATCH = 36
ZH_SIZE, ZH_TRACK = 46, 0.06
GAP_ZH = 32
EN_SIZE, EN_TRACK = 19, 0.26
GAP_EN = 48
RULE_W, GAP_RULE = 56, 48
NOTE_SIZE, NOTE_LEAD = 24, 1.95
GAP_NOTE = 62
FOOT_SIZE, FOOT_TRACK = 15, 0.24
PAD_BOTTOM = 104

# Chinese line-breaking: these may never open a line.
NO_START = set("，。、；：？！）〕］｝〉》」』】’”%…ー～")
NO_END = set("（〔［｛〈《「『【‘“")
# Full-width stops carry roughly half an em of built-in space on the right.
# Leaving it be is what makes machine-set Chinese look loose, so it is taken
# back here, and the same rule feeds line measurement.
SQUEEZE = set("，。、；：！？")
SQUEEZE_AMT = 0.26
SEASON_EN = {"spring": "SPRING", "summer": "SUMMER",
             "autumn": "AUTUMN", "winter": "WINTER"}
SEASON_ZH = {"spring": "春", "summer": "夏", "autumn": "秋", "winter": "冬"}


def white_point(arr):
    lum = arr @ (0.299, 0.587, 0.114)
    sel = arr[lum >= np.percentile(lum, WHITE_PERCENTILE)]
    return np.median(sel, axis=0)


def target_white():
    return white_point(np.asarray(Image.open(COVER_REF).convert("RGB"), float))


def sheet_paper(height, plate_box, aim):
    """One sheet of the covers' stock, toned to `aim` on the visible paper.

    The gain is measured on the paper that stays visible — the mat and the
    caption area — rather than on the whole sheet, because the stock is not
    perfectly even at large scale and the part hidden behind the plate would
    otherwise drag the result off by a few levels.
    """
    stock = np.asarray(
        Image.open(PAPER).convert("RGB").resize((W, height), Image.LANCZOS), float)
    grain = stock.mean(axis=2) / 255.0
    grain = 1.0 - (1.0 - grain) * GRAIN_STRENGTH
    out = stock * grain[..., None]

    # gain is set on the caption area, the largest unbroken run of bare paper.
    # The mat stays a touch darker because paper.jpeg carries its own scan
    # vignette at the sheet edges, which is what real paper does.
    band_top = plate_box[3]
    out *= aim / np.maximum(white_point(out[band_top:]), 1.0)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def advance(draw, ch, font, squeeze):
    w = draw.textlength(ch, font=font)
    if squeeze and ch in SQUEEZE:
        w -= SQUEEZE_AMT * font.size
    return w


def tracked(draw, xy, text, font, fill, track, squeeze=False):
    """Draw with letterspacing in em, optionally squeezing full-width stops."""
    x, y = xy
    extra = track * font.size
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += advance(draw, ch, font, squeeze) + extra
    return x - extra - xy[0]


def tracked_width(draw, text, font, track, squeeze=False):
    if not text:
        return 0
    return (sum(advance(draw, c, font, squeeze) for c in text)
            + track * font.size * (len(text) - 1))


def units(text):
    """Split into break units: ASCII runs stay whole, CJK breaks per char."""
    out, buf = [], ""
    for ch in text:
        if ch.isascii() and not ch.isspace():
            buf += ch
            continue
        if buf:
            out.append(buf)
            buf = ""
        if ch == "—" and out and out[-1] == "—":
            out[-1] = "——"          # keep the dash pair together
        elif not ch.isspace():
            out.append(ch)
    if buf:
        out.append(buf)
    return out


def wrap_cjk(draw, text, font, width):
    def run_w(s):
        return sum(advance(draw, c, font, True) for c in s)

    lines, cur = [], ""
    for u in units(text):
        trial = cur + u
        if cur and run_w(trial) > width:
            lines.append(cur)
            cur = u
        else:
            cur = trial
    if cur:
        lines.append(cur)
    # kinsoku: pull a forbidden opener back onto the line above
    for i in range(1, len(lines)):
        while lines[i] and lines[i][0] in NO_START:
            lines[i - 1] += lines[i][0]
            lines[i] = lines[i][1:]
        while lines[i - 1] and lines[i - 1][-1] in NO_END:
            lines[i] = lines[i - 1][-1] + lines[i]
            lines[i - 1] = lines[i - 1][:-1]
    return [ln for ln in lines if ln]


def mix(ink, paper, amount):
    return tuple(round(p + (i - p) * amount) for i, p in zip(ink, paper))


def face(font, sample):
    """(top offset, height) of the printed face, not the em box.

    PIL draws from the ascender, which sits well above the top of a CJK
    glyph. Measuring the face means the gaps in the layout table are the
    gaps you actually see.
    """
    box = font.getbbox(sample)
    return box[1], box[3] - box[1]


def metrics(fonts):
    zh_t, zh_h = face(fonts["zh"], "汉字")
    en_t, en_h = face(fonts["en"], "HAMBURG")
    nt_t, nt_h = face(fonts["note"], "汉字")
    ft_t, ft_h = face(fonts["foot"], "SPRING春")
    return {"zh": (zh_t, zh_h), "en": (en_t, en_h),
            "note": (nt_t, nt_h), "foot": (ft_t, ft_h),
            "lead": round(NOTE_SIZE * NOTE_LEAD)}


def band_height(draw, entry, fonts, m):
    note_lines = wrap_cjk(draw, entry["note"], fonts["note"], COL_W)
    block = m["lead"] * (len(note_lines) - 1) + m["note"][1]
    h = PAD_TOP + SWATCH + GAP_SWATCH
    h += m["zh"][1] + GAP_ZH
    h += m["en"][1] + GAP_EN
    h += 1 + GAP_RULE
    h += block + GAP_NOTE
    h += m["foot"][1] + PAD_BOTTOM
    return h, note_lines, block


def build(entry, fonts, m, band_fixed=None):
    poster = Image.open(IMGDIR / pathlib.Path(entry["file"]).name).convert("RGB")
    if poster.width != PLATE_W:
        poster = poster.resize(
            (PLATE_W, round(poster.height * PLATE_W / poster.width)),
            Image.LANCZOS)

    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    band, note_lines, note_block = band_height(probe, entry, fonts, m)
    if band_fixed:
        band = band_fixed      # one book, one page size

    # the plate's own paper is the reference, so the mat cannot drift from it
    aim = white_point(np.asarray(poster, float))
    plate_box = (MAT, MAT, MAT + poster.width, MAT + poster.height)
    sheet = sheet_paper(MAT + poster.height + band, plate_box, aim)
    sheet.paste(poster, (MAT, MAT))
    d = ImageDraw.Draw(sheet)
    paper_rgb = tuple(int(v) for v in aim)

    y = MAT + poster.height + PAD_TOP

    accent = entry.get("accent_hex")
    if accent:
        rgb = tuple(int(accent.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        d.rectangle([COL_X, y, COL_X + SWATCH - 1, y + SWATCH - 1], fill=rgb)
    y += SWATCH + GAP_SWATCH

    tracked(d, (COL_X, y - m["zh"][0]), entry["title_zh"], fonts["zh"],
            INK_TEXT, ZH_TRACK)
    y += m["zh"][1] + GAP_ZH

    en = entry["title"].replace(" \u2014 ", " \u00b7 ").upper()
    tracked(d, (COL_X, y - m["en"][0]), en, fonts["en"],
            mix(INK_TEXT, paper_rgb, 0.70), EN_TRACK)
    y += m["en"][1] + GAP_EN

    d.rectangle([COL_X, y, COL_X + RULE_W, y], fill=INK_RULE)
    y += 1 + GAP_RULE

    note_ink = mix(INK_TEXT, paper_rgb, 0.82)
    for i, ln in enumerate(note_lines):
        tracked(d, (COL_X, y + i * m["lead"] - m["note"][0]), ln,
                fonts["note"], note_ink, 0.0, squeeze=True)
    # The folio is pinned to the foot of the page, not to the end of the note,
    # so it lands on the same line on all eighteen plates.
    season = entry.get("season", "")
    left = f"{SEASON_EN.get(season, season.upper())} \u00b7 {SEASON_ZH.get(season, '')}"
    fy = sheet.height - PAD_BOTTOM - m["foot"][1] - m["foot"][0]
    tracked(d, (COL_X, fy), left, fonts["foot"], INK_FAINT, FOOT_TRACK)
    right = f"{entry['id']:02d}"
    rw = tracked_width(d, right, fonts["foot"], FOOT_TRACK)
    tracked(d, (COL_X + COL_W - rw, fy), right, fonts["foot"], INK_FAINT,
            FOOT_TRACK)
    return sheet


def load_fonts():
    return {
        "zh": ImageFont.truetype(F_CJK, ZH_SIZE, index=F_CJK_I),
        "en": ImageFont.truetype(F_LAT, EN_SIZE),
        "note": ImageFont.truetype(F_CJK, NOTE_SIZE, index=F_CJK_I),
        "foot": ImageFont.truetype(F_CJK, FOOT_SIZE, index=F_CJK_I),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=int, action="append",
                    help="only these poster ids (default: all of 28-45)")
    ap.add_argument("--outdir", default=str(OUTDIR))
    ap.add_argument("--quality", type=int, default=88)
    args = ap.parse_args()

    data = json.loads(INDEX.read_text())
    want = set(args.id or range(28, 46))
    fonts = load_fonts()
    m = metrics(fonts)
    out = pathlib.Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    entries = [e for e in data["posters"] if e["id"] in want]

    # A set of plates is one book: every page the same size. The tallest
    # caption sets the band, the shorter ones take the slack as bottom margin.
    #
    # The band is measured over the WHOLE book, never over the subset being
    # rendered. Re-running with --id would otherwise re-cut that one page to a
    # different height and quietly break the set: regenerating sheet 34 alone
    # produced 2834 against the book's 2881.
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    book = [e for e in data["posters"] if e.get("plate")]
    band_fixed = max(band_height(probe, e, fonts, m)[0] for e in book)

    for entry in entries:
        sheet = build(entry, fonts, m, band_fixed)
        dst = out / pathlib.Path(entry["file"]).name
        sheet.save(dst, quality=args.quality, optimize=True, progressive=True)
        print(f"{entry['id']:>3}  {sheet.width}x{sheet.height}  "
              f"{dst.stat().st_size // 1024:>4}KB  {dst.name}")


if __name__ == "__main__":
    main()
