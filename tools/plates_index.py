#!/usr/bin/env python3
"""Fold the Plates sheets (52-57) into posters/index.json.

Same six photographs and the same six phrases as Colorful Journey (46-51), but
printed as photographic plates instead of being reduced to an anchor. The two
series are kept side by side on purpose so the treatments can be compared.

Everything numbered 51 and below is left exactly as it is, so this script,
tools/journey_index.py and tools/seasons_index.py can be run in any order.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from plates_pages import PLATES, build  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "posters" / "index.json"

SOURCE = (
    "series — Plates；底图与 Colorful Journey 同源，六张用户旅行照片，"
    "同样的六句话。区别在策略：照片按「图版」整幅印上纸，不再拆成 anchor。"
    "这是对 gc-minimal-zine-poster-v0-1 的一次明确越界——"
    "skill 的 Image Anchor 词表八项全部是减法，"
    "本组放弃了 Color Engine「主色占版面 0.8%-2.5%」那条数值规则，"
    "图版实测占版面 27.9%-41.4%。"
    "依据是 skill 自己写的 Prefer a colored ... image panel，"
    "以及禁止项只禁 full-bleed（出血），不禁尺寸。"
    "保留的部分：近白纸、平扫视角、极简排字、印刷瑕疵、单一主色。"
)

SERIES_NOTE = (
    "六张，与 46-51 一一对应、同照片同句子，但把照片当图版印。"
    "六张纸白点实测 249-253，R−B +1 到 +4，全部中性白。"
    "每张一个色相：52 品红、53 钴蓝、54 琥珀、55 番茄红、56 紫、57 青。"
    "55 是唯一的灰底单点色（红浮标按真实大小印，不放大）；"
    "57 是严格双色版，实测 100% 有彩像素落在青色相 180-210° 区间，雪就是未印的纸。"
    "刻意放弃了 skill 的 0.8%-2.5% 色块上限，这是策略差异，不是踩线，文档里如实记录。"
)


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def filename(plate) -> str:
    return f"{plate.pid}-{plate.fslug}-{slug(plate.title)}.jpeg"


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    posters = [p for p in data["posters"] if p["id"] <= 51]

    for plate in PLATES:
        entry = {
            "id": plate.pid,
            "series": "plates",
            "role": "single",
            "place": plate.place,
            "file": f"img/{filename(plate)}",
            "title": plate.title,
            "title_zh": plate.title_zh,
            "recipe": {
                "layout": plate.geometry,
                "anchor": plate.treatment,
                "typography": plate.typography,
                "accent": plate.accent,
                "texture": plate.texture,
                "mood": plate.mood,
            },
            "accent_hex": plate.accent_hex,
            "source": SOURCE,
            "photo": f"assets/journey/photos/{plate.photo}",
            "note": plate.note,
            "prompt": build(plate),
        }
        target = REPO / "posters" / entry["file"]
        if not target.exists():
            raise SystemExit(f"missing image: {entry['file']}")
        posters.append(entry)

    posters.sort(key=lambda p: p["id"])
    data["posters"] = posters

    series = data.get("series", {})
    series["plates"] = {
        "label": "Plates",
        "label_zh": "整版照片",
        "count": len(PLATES),
        "note": SERIES_NOTE,
    }
    data["series"] = series

    INDEX.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"posters: {len(posters)}")
    for plate in PLATES:
        print(f"  {plate.pid}  {plate.accent_hex}  {plate.place:<11}{plate.title}")


if __name__ == "__main__":
    main()
