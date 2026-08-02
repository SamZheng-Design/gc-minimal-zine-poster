#!/usr/bin/env python3
"""Package the captioned Seasons album into a single ZIP for handing to someone.

The point of the captioned edition is that a set of files can travel on its own,
so the archive is built to be read straight out of the folder:

  * files are numbered in *reading* order (each season's cover, then its pages),
    because alphabetical order is the only order a file browser guarantees;
  * the archive id is kept in the name too, so a sheet can still be traced back
    to posters/index.json;
  * a contents file carries the titles and notes as text, for anyone who wants
    to quote them without retyping off the image;
  * a print-ready A4 PDF rides along, so the album can go to paper without the
    recipient having to impose eighteen files by hand;
  * filenames stay ASCII. Chinese names in ZIP entries still break on some
    Windows extractors, and a filename is not the place to put the poetry.

Usage:
    python3 tools/seasons_pack.py                 # -> dist/seasons-album-plates.zip
    python3 tools/seasons_pack.py --edition img   # the plain sheets, no captions
    python3 tools/seasons_pack.py --no-pdf        # images and contents only
    python3 tools/seasons_pack.py --out /tmp/x.zip
"""

import argparse
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "posters" / "index.json"
SERIES = "seasons"


def reading_order(data):
    """Each chapter's cover, then its pages — the same order the viewer uses."""
    by_id = {p["id"]: p for p in data["posters"]}
    out, seen = [], set()
    for ch in data.get("chapters", []):
        for pid in [ch["cover"], *ch.get("pages", [])]:
            if pid in by_id and pid not in seen:
                out.append(by_id[pid])
                seen.add(pid)
    # anything filed under the series but not in a chapter still ships
    for p in data["posters"]:
        if p.get("series") == SERIES and p["id"] not in seen:
            out.append(p)
            seen.add(p["id"])
    return out


def contents(pages, data, edition):
    """A plain-text table of contents, in the album's own voice."""
    label = {"plates": "题注版（标题与介绍已印在纸上）",
             "img": "无字版（纯画面）"}[edition]
    ch_of = {}
    for ch in data.get("chapters", []):
        for pid in [ch["cover"], *ch.get("pages", [])]:
            ch_of[pid] = ch

    lines = [
        "四季影集  THE SEASONS",
        f"{len(pages)} 张 · {label}",
        "",
        "文件名前两位是阅读顺序，后面的两位数字是归档编号，",
        "与 posters/index.json 里的 id 一一对应。",
        "",
        "包内另附一份 A4 打印版 PDF（含扇页，共 19 页）：图版按 300 dpi 原生",
        "尺寸居中落位（119.0 × 243.9 mm），不缩放不重采样，四周留白便于裁切。",
        "",
        "=" * 64,
        "",
    ]
    current = None
    for n, p in enumerate(pages, 1):
        ch = ch_of.get(p["id"])
        if ch and ch is not current:
            current = ch
            lines += ["", f"── {ch['label_zh']}  {ch['label'].upper()} " + "─" * 28, ""]
        role = "封面" if p.get("role") == "cover" else "内页"
        lines += [
            f"{n:02d}  [{role}]  no.{p['id']:02d}",
            f"    {p['title']}",
            f"    {p.get('title_zh', '')}",
            f"    {p.get('note', '')}",
            "",
        ]
    lines += [
        "=" * 64,
        "",
        "海报由 gc-minimal-zine-poster-v0-1 生成，逐张过 16 项 Quality Gate。",
        "18 张共用同一张纸：内页纸色经 tools/paper_normalize.py 归一到封面白点。",
        "题注版由 tools/caption_plates.py 排版 —— 图版原尺寸裱贴，不缩放、不压字。",
        "",
        "MIT License.",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", choices=["plates", "img"], default="plates")
    ap.add_argument("--out")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    data = json.loads(INDEX.read_text(encoding="utf-8"))
    pages = [p for p in reading_order(data) if p.get("series") == SERIES]
    if not pages:
        raise SystemExit("no seasons pages found in index.json")

    key = "plate" if args.edition == "plates" else "file"
    missing = [p["id"] for p in pages if not p.get(key)]
    if missing:
        raise SystemExit(f"missing {key} for ids {missing}")

    stem = f"seasons-album-{args.edition}"
    out = Path(args.out) if args.out else ROOT / "dist" / f"{stem}.zip"
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w") as z:
        # text compresses; JPEG does not, so don't burn time pretending it does
        z.writestr(
            f"{stem}/目录 CONTENTS.txt",
            contents(pages, data, args.edition),
            compress_type=zipfile.ZIP_DEFLATED,
        )
        for n, p in enumerate(pages, 1):
            src = ROOT / "posters" / p[key]
            if not src.exists():
                raise SystemExit(f"missing file: {src}")
            tail = src.name.split("-", 1)[1]          # drop the archive id prefix
            name = f"{stem}/{n:02d}_{p['id']:02d}-{tail}"
            z.write(src, name, compress_type=zipfile.ZIP_STORED)

        if not args.no_pdf:
            # built fresh rather than trusting whatever is lying in dist/, so the
            # PDF in the archive always matches the images beside it
            import seasons_pdf

            pdf = seasons_pdf.build(args.edition)
            z.write(pdf, f"{stem}/四季影集-A4-打印版.pdf",
                    compress_type=zipfile.ZIP_STORED)

    size = out.stat().st_size
    print(f"{out.relative_to(ROOT)}  {len(pages)} sheets  {size / 1e6:.1f} MB")
    return out


if __name__ == "__main__":
    main()
