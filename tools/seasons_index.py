#!/usr/bin/env python3
"""Fold the Seasons interior sheets (32-45) into posters/index.json.

The four covers (28-31) get role="cover"; the fourteen sheets built from the
photographs get role="interior" plus the season they belong to. Nothing else
in the file is touched -- singles 01-27 are left exactly as they are, and so is
anything numbered above 45 (Colorful Journey, written by tools/journey_index.py).
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from seasons_pages import PAGES, build  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "posters" / "index.json"

COVER_SEASON = {28: "spring", 29: "summer", 30: "autumn", 31: "winter"}

SEASON_LABEL = {
    "spring": ("Spring", "春"),
    "summer": ("Summer", "夏"),
    "autumn": ("Autumn", "秋"),
    "winter": ("Winter", "冬"),
}

SOURCE = (
    "series — Seasons 内页；底图是用户提供的照片（已裁掉水印条），"
    "按 gc-minimal-zine-poster-v0-1 Standard Mode 重做；"
    "出图后由 tools/paper_normalize.py 把墨重印到封面同一张纸上"
)


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    # Everything this script owns lives in 32-45. Keep the rest untouched:
    # 01-27 are the singles, 46+ belong to another series' index writer.
    posters = [p for p in data["posters"] if p["id"] <= 31 or p["id"] > 45]

    for p in posters:
        if p["id"] in COVER_SEASON:
            p["role"] = "cover"
            p["season"] = COVER_SEASON[p["id"]]
            p["plate"] = "plates/" + p["file"].split("/", 1)[1]

    for page in PAGES:
        posters.append(
            {
                "id": page.pid,
                "series": "seasons",
                "role": "interior",
                "season": page.season,
                "file": f"img/{page.pid}-{page.season}-{slug(page.title)}.jpeg",
                "plate": f"plates/{page.pid}-{page.season}-{slug(page.title)}.jpeg",
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
                "photo": f"assets/seasons/photos/{page.photo}",
                "note": page.note,
                "prompt": build(page),
            }
        )

    posters.sort(key=lambda p: p["id"])
    data["posters"] = posters

    series = data.get("series", {})
    series.update({
        "singles": {"label": "Singles", "label_zh": "单张", "count": 27},
        "seasons": {
            "label": "Seasons",
            "label_zh": "四季",
            "count": 18,
            "note": (
                "一册四章，十八张。四张封面（28–31）由 tools/seasons_compose.py "
                "用同一张几何表合成，除照片和色块外逐像素相同；十四张内页（32–45）"
                "回到 skill 的 Variation Engine，每张换一套配方，出图后由 "
                "tools/paper_normalize.py 把墨重印到封面同一张纸上，"
                "十八张纸白点统一在 229/221/203。"
            ),
        },
    })
    data["series"] = series

    chapters = []
    for key in ("spring", "summer", "autumn", "winter"):
        label, label_zh = SEASON_LABEL[key]
        cover = next(p["id"] for p in posters if p.get("season") == key
                     and p.get("role") == "cover")
        pages = [p["id"] for p in posters if p.get("season") == key
                 and p.get("role") == "interior"]
        chapters.append(
            {
                "season": key,
                "label": label,
                "label_zh": label_zh,
                "cover": cover,
                "pages": pages,
            }
        )
    data["chapters"] = chapters

    INDEX.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"posters: {len(posters)}")
    for ch in chapters:
        print(f"  {ch['label_zh']}  cover {ch['cover']}  pages {ch['pages']}")


if __name__ == "__main__":
    main()
