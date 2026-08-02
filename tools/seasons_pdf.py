#!/usr/bin/env python3
"""Impose the captioned Seasons album onto A4 pages for printing.

Design decisions, and why:

  * The plates are placed at their NATIVE pixel density (300 dpi), not scaled to
    fill the page. 1406x2881 px at 300 dpi is 119.0 x 243.9 mm, which sits inside
    A4 with a 45.5 mm side margin and a 26.5 mm head and foot. Scaling to fill
    would resample every sheet for no gain — the paper grain and the halftone are
    the artwork, and resampling softens exactly those.

  * The page around the plate is left unprinted. Each plate already carries its
    own sheet of paper; printing a second paper tone around it would read as a
    picture of paper sitting on paper. Unprinted margin also gives something to
    hold and something to trim.

  * The title page is rendered by the same engine as the plates
    (tools/caption_plates.py), at the same sheet size, on the same paper, in the
    same inks, on the same left axis — so it is a sheet in the book rather than a
    cover bolted onto it. reportlab cannot embed the CFF-outlined Noto Serif CJK
    anyway, and drawing the page with PIL is the answer that also buys
    consistency.

Usage:
    python3 tools/seasons_pdf.py                     # -> dist/seasons-album-a4.pdf
    python3 tools/seasons_pdf.py --edition img       # the plain sheets
    python3 tools/seasons_pdf.py --out /tmp/x.pdf
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

import caption_plates as cp

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "posters" / "index.json"
SERIES = "seasons"

DPI = 300.0
PAGE_W, PAGE_H = A4

TITLE_LINES = [
    "一棵树站在空地上，一年只被拍四次。",
    "四张封面是它最满、最盛、最锈、最空的时候，",
    "十四张内页是那四次之间落下来的东西。",
]
COLOPHON = [
    "海报由 gc-minimal-zine-poster-v0-1 生成，逐张过 16 项 Quality Gate。",
    "十八张共用同一张纸：内页纸色经 tools/paper_normalize.py 归一到封面白点。",
    "题注由 tools/caption_plates.py 排版，图版原尺寸裱贴，不缩放、不压字。",
    "本册由 tools/seasons_pdf.py 拼版，图版按 300 dpi 原生尺寸落位。",
    "MIT License.",
]


def reading_order(data):
    by_id = {p["id"]: p for p in data["posters"]}
    out, seen = [], set()
    for ch in data.get("chapters", []):
        for pid in [ch["cover"], *ch.get("pages", [])]:
            if pid in by_id and pid not in seen:
                out.append(by_id[pid])
                seen.add(pid)
    for p in data["posters"]:
        if p.get("series") == SERIES and p["id"] not in seen:
            out.append(p)
            seen.add(p["id"])
    return out


def plate_box(path):
    """Native-size placement box, centred on the page."""
    with Image.open(path) as im:
        w, h = im.size
    pw = w / DPI * 72.0
    ph = h / DPI * 72.0
    return (PAGE_W - pw) / 2.0, (PAGE_H - ph) / 2.0, pw, ph


def title_sheet(height, edition, dst):
    """A title page that is a sheet of the book, not a cover bolted onto it.

    Same size, same stock, same inks, same left axis as the eighteen plates,
    drawn with the plates' own helpers so nothing can drift between them.
    """
    fonts = {
        "big": ImageFont.truetype(cp.F_CJK, 78, index=cp.F_CJK_I),
        "en": ImageFont.truetype(cp.F_LAT, 26),
        "sub": ImageFont.truetype(cp.F_CJK, 26, index=cp.F_CJK_I),
        "body": ImageFont.truetype(cp.F_CJK, 27, index=cp.F_CJK_I),
        "small": ImageFont.truetype(cp.F_CJK, 17, index=cp.F_CJK_I),
    }
    # no plate on this sheet, so the paper gain is measured below the top margin
    sheet = cp.sheet_paper(height, (0, 0, 0, cp.MAT), cp.target_white())
    d = ImageDraw.Draw(sheet)
    x = cp.COL_X

    y = round(height * 0.26)
    t, h = cp.face(fonts["big"], "四季影集")
    cp.tracked(d, (x, y - t), "四季影集", fonts["big"], cp.INK_TEXT, 0.10)
    y += h + 54

    t, h = cp.face(fonts["en"], "HAMBURG")
    cp.tracked(d, (x, y - t), "THE SEASONS", fonts["en"], cp.INK_TEXT, 0.34)
    y += h + 46

    d.line([(x, y), (x + cp.RULE_W, y)], fill=cp.INK_RULE, width=1)
    y += 46

    label = "题注版" if edition == "plates" else "无字版"
    t, h = cp.face(fonts["sub"], "汉字")
    cp.tracked(d, (x, y - t), f"十八幅 · 四章 · {label}", fonts["sub"],
               cp.INK_TEXT, 0.10, squeeze=True)
    y += h + 96

    t, h = cp.face(fonts["body"], "汉字")
    for ln in TITLE_LINES:
        cp.tracked(d, (x, y - t), ln, fonts["body"], cp.INK_TEXT, 0.03, squeeze=True)
        y += round(27 * 1.95)

    t, h = cp.face(fonts["small"], "汉字")
    y = height - cp.PAD_BOTTOM - (len(COLOPHON) - 1) * round(17 * 2.0) - h
    for ln in COLOPHON:
        cp.tracked(d, (x, y - t), ln, fonts["small"], cp.INK_FAINT, 0.02, squeeze=True)
        y += round(17 * 2.0)

    sheet.save(dst, quality=94, optimize=True, progressive=True)
    return dst


def build(edition="plates", out=None, quiet=False):
    """Impose the album and return the PDF path."""
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    pages = [p for p in reading_order(data) if p.get("series") == SERIES]
    key = "plate" if edition == "plates" else "file"
    missing = [p["id"] for p in pages if not p.get(key)]
    if missing:
        raise SystemExit(f"missing {key} for ids {missing}")

    out = Path(out) if out else ROOT / "dist" / f"seasons-album-a4-{edition}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle("四季影集 THE SEASONS")
    c.setAuthor("gc-minimal-zine-poster")
    c.setSubject("18 plates, four chapters")

    first = ROOT / "posters" / pages[0][key]
    with Image.open(first) as im:
        sheet_h = im.height
    tmp = out.parent / f".title-{edition}.jpeg"
    title_sheet(sheet_h, edition, tmp)
    bx, by, bw, bh = plate_box(tmp)
    c.drawImage(str(tmp), bx, by, width=bw, height=bh)
    c.showPage()

    for p in pages:
        src = ROOT / "posters" / p[key]
        if not src.exists():
            raise SystemExit(f"missing file: {src}")
        bx, by, bw, bh = plate_box(src)
        # JPEG is embedded as-is; no resampling, no re-encoding
        c.drawImage(str(src), bx, by, width=bw, height=bh)
        c.showPage()

    c.save()
    tmp.unlink(missing_ok=True)
    if not quiet:
        print(f"{out.relative_to(ROOT)}  {len(pages) + 1} pages  "
              f"{out.stat().st_size / 1e6:.1f} MB")
        print(f"plate placed at {bw / mm:.1f} x {bh / mm:.1f} mm "
              f"(margins {bx / mm:.1f} mm side, {by / mm:.1f} mm head/foot)")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", choices=["plates", "img"], default="plates")
    ap.add_argument("--out")
    args = ap.parse_args()
    build(args.edition, args.out)


if __name__ == "__main__":
    main()
