#!/usr/bin/env python3
"""Fold the Colorful Journey sheets (46-51) into posters/index.json.

Six single sheets, one per photograph, no covers and no chapters -- the series
is a flat run. Everything numbered 45 and below is left exactly as it is, so
this script and tools/seasons_index.py can be run in either order.

The prompt stored for each sheet is the one that actually produced the shipped
image, which is why journey_pages.Page carries `wl` (which whitelist wording was
used) and `shipped` (a verbatim prompt for the one sheet that diverged).
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from journey_pages import PAGES, build  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "posters" / "index.json"

SOURCE = (
    "series — Colorful Journey；底图是用户提供的旅行照片，"
    "按 gc-minimal-zine-poster-v0-1 Standard Mode 重做。"
    "两处按用户要求的偏离：纸底改为近白（实测 250-253，R−B 4-6，"
    "对照 Seasons 的 229/221/203），色块目标放宽到 3-6%（skill 原上限 2.5%）。"
    "未经 paper_normalize 重印，六张各自出白。"
)

SERIES_NOTE = (
    "六张，一张照片一张纸。相对 skill 默认值有两处刻意偏离，都是按用户要求做的："
    "一是纸底换成近白棉纸，六张纸白点落在 250-253、R−B 4-6；"
    "二是保留下来的彩色面积放大，实测占版面 1.4%-7.9%，其中四张高于 skill "
    "0.8-2.5% 的上限。色块仍然是单一色相、满饱和、不透明，"
    "六张各用一个色，缩到 64px 宽仍然一眼可见。"
)


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def filename(page) -> str:
    return f"{page.pid}-{page.fslug or page.place.lower()}-{slug(page.title)}.jpeg"


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    posters = [p for p in data["posters"] if p["id"] <= 45 or p["id"] > 51]

    for page in PAGES:
        entry = {
            "id": page.pid,
            "series": "colorful-journey",
            "role": "single",
            "place": page.place,
            "file": f"img/{filename(page)}",
            "title": page.title,
            "title_zh": page.title_zh,
            "recipe": {
                "layout": page.layout,
                "anchor": page.anchor,
                "typography": page.typography,
                "accent": page.accent,
                "texture": page.texture,
                "mood": page.mood,
            },
            "accent_hex": page.accent_hex,
            "source": SOURCE,
            "photo": f"assets/journey/photos/{page.photo}",
            "note": page.note,
            "prompt": build(page),
        }
        missing = REPO / "posters" / entry["file"]
        if not missing.exists():
            raise SystemExit(f"missing image: {entry['file']}")
        posters.append(entry)

    posters.sort(key=lambda p: p["id"])
    data["posters"] = posters

    series = data.get("series", {})
    series["colorful-journey"] = {
        "label": "Colorful Journey",
        "label_zh": "旅程留色",
        "count": len(PAGES),
        "note": SERIES_NOTE,
    }
    data["series"] = series

    INDEX.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"posters: {len(posters)}")
    for page in PAGES:
        print(f"  {page.pid}  {page.accent_hex}  {page.place:<11}{page.title}")


if __name__ == "__main__":
    main()
