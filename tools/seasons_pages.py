#!/usr/bin/env python3
"""
Seasons album — interior pages.

The four covers (28-31) are laid out by tools/seasons_compose.py because a
series cover has to be millimetre-identical. The interior pages are the
opposite: each one gets its own Variation Engine recipe, so the model lays
them out and only the PAPER is forced to match.

This module holds the recipe table and compiles the 14 prompts. Every prompt
shares a byte-identical paper paragraph and a byte-identical avoid-list, so
the one thing that must not drift cannot drift.

    python3 tools/seasons_pages.py            # print all prompts
    python3 tools/seasons_pages.py --id 32    # print one
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

# Photos are served to the image model over HTTP from the repo.
PHOTO_BASE = "assets/seasons/photos"

# --------------------------------------------------------------------------
# Shared wording. Identical in all 14 prompts — this is the consistency floor.
# --------------------------------------------------------------------------

PAPER = (
    "Tall vertical 3:5 paper poster. The whole sheet is one piece of aged "
    "oat-white paper, a warm pale ivory that is slightly warmer and duller than "
    "pure white, with fine cotton-rag fibre and only the faintest even mottling. "
    "The paper tone is the same from corner to corner: no yellow patches, no "
    "brown staining, no dark edges, no tea-coloured wash, no cream-to-white "
    "gradient. Flat orthographic scanner-bed view, no border, no mockup, no "
    "paper shadow, no curl."
)

AVOID = (
    "Flat scanned-paper feeling, matte and absorbent, diffuse even light, low to "
    "medium contrast, no hard shadow, no depth of field, no 3D. Avoid: full-bleed "
    "photograph, the reference photo filling the sheet, commercial headline "
    "hierarchy, product advertisement layout, logo, CTA, glossy mockup, clean "
    "digital white background, cinematic lighting, neon, cyberpunk, cute cartoon, "
    "anime, fashion editorial drama, dense scrapbook collage, many colours, long "
    "clean paragraphs of text, stock-photo realism, yellowed or tea-stained paper."
)


def whitelist(strings: list[str]) -> str:
    """
    Enumerate the only permitted strings. Earlier sheets in this album printed
    prompt vocabulary into the artwork and duplicated words, so the permitted
    text is now stated as a closed set.
    """
    items = " / ".join(f'"{s}"' for s in strings)
    return (
        f"STRICT TEXT WHITELIST. The only text allowed anywhere on the sheet is: "
        f"{items}. Each string is printed once and once only, spelled exactly as "
        f"given, with no repeated word. Do not render any other word. Do not print "
        f"any word from these instructions. No caption, no signature, no username, "
        f"no social-media handle, no watermark, no date stamp, no page number, no "
        f"logo."
    )


@dataclass(frozen=True)
class Page:
    pid: int
    photo: str
    season: str
    title: str
    title_zh: str
    layout: str
    anchor: str
    typography: str
    texture: str
    mood: str
    accent: str  # plain-language hue, goes into the prompt
    accent_hex: str
    cluster: str  # paragraph 1: cluster size and placement
    subject: str  # paragraph 2: how the photo is used
    type_and_accent: str  # paragraph 3: type behaviour + the accent object
    text: list[str]  # the whitelist
    note: str


PAGES: tuple[Page, ...] = (
    # ---------------------------------------------------------------- SPRING
    Page(
        pid=32,
        photo="p02.jpeg",
        season="spring",
        title="it happened without us",
        title_zh="没人看着它也开了",
        layout="center-fragment",
        anchor="tiny faded photo",
        typography="almost textless, only a tiny caption",
        texture="film grain photo",
        mood="quiet",
        accent="magenta-pink",
        accent_hex="#E0357B",
        cluster=(
            "About 86% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 11% of the canvas, sitting slightly above the middle "
            "of the sheet, well away from every edge."
        ),
        subject=(
            "The cluster is the attached photograph reproduced very small, as a "
            "single rectangular print about one quarter of the sheet width, with a "
            "soft photocopied edge that sinks into the paper. Keep its subject "
            "exactly as given — one blossoming tree standing alone in a meadow "
            "under a wide sky — but printed faint and grainy, drained almost to "
            "grey, like a photograph reprinted in an old journal."
        ),
        type_and_accent=(
            "Under the photograph, one line of small serif type. The single "
            "high-chroma element is a solid, fully saturated magenta-pink "
            "risograph rectangle laid across the lower third of the photograph "
            "like a printer's colour bar, about 1.6% of the whole sheet and about "
            "20% of the cluster, opaque and clean-edged, misregistered a "
            "half-millimetre from the photo below it. Everything else on the sheet "
            "is paper tone and grey."
        ),
        text=["it happened without us"],
        note="花开这件事跟观众没关系。照片被印得几乎褪成灰，只有一条洋红色的印刷色条压在上面，像校色条——提醒你这是一张被复制过的图，不是现场。",
    ),
    Page(
        pid=33,
        photo="p03.jpeg",
        season="spring",
        title="the tree turned into weather",
        title_zh="树变成了天气",
        layout="irregular-cutout",
        anchor="torn-paper clipping",
        typography="fragmented floating letters",
        texture="risograph grain",
        mood="childhood",
        accent="cobalt blue",
        accent_hex="#1B4FD8",
        cluster=(
            "About 84% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 13% of the canvas, placed in the upper-middle area, "
            "clear of all four edges."
        ),
        subject=(
            "The cluster is the attached photograph torn out of a magazine — an "
            "irregular hand-torn paper shape with a visible white fibrous tear "
            "along its edge, laid slightly crooked on the sheet. Keep its subject "
            "exactly as given: a huge soft mass of white blossom dissolving into "
            "the sky so the tree reads more like cloud than like a tree. Printed "
            "with coarse risograph grain, low contrast, nearly grey."
        ),
        type_and_accent=(
            "A few small serif letters float loose around the torn clipping, "
            "broken apart and drifting, not set on a line. The single high-chroma "
            "element is a solid, fully saturated cobalt-blue risograph shape torn "
            "from the same magazine and overlapping the lower-left corner of the "
            "clipping, about 1.8% of the whole sheet and about 22% of the cluster, "
            "opaque and undiluted, printed slightly off register. No other colour."
        ),
        text=["the tree turned into weather"],
        note="白花团糊成一片，已经分不清是树还是云。撕下来的一角压着一块钴蓝——那是唯一还确定的东西。",
    ),
    Page(
        pid=34,
        photo="p09.jpeg",
        season="spring",
        title="almost nothing, for a week",
        title_zh="几乎什么都没有，持续一周",
        layout="lower-left-float",
        anchor="tiny faded photo",
        typography="archive microtext with date and weather",
        texture="xerox softness",
        mood="afternoon",
        accent="violet",
        accent_hex="#6B31C9",
        cluster=(
            "About 88% of the sheet is plain empty paper, almost all of it across "
            "the top. One small visual cluster occupies roughly 9% of the canvas, "
            "floating in the lower-left quadrant, not touching any edge. The "
            "emptiness is the subject: keep the sheet overwhelmingly bare."
        ),
        subject=(
            "The cluster is the attached photograph reproduced as a small "
            "photocopied print about one fifth of the sheet width and small on the "
            "page, its edges gone soft and its blacks gone grey the way a "
            "third-generation xerox looks. Keep its subject exactly as given: one "
            "pale pink blossoming tree standing alone in an open field."
        ),
        # Sizing the slab took two goes. "an underline that got far too thick"
        # produced a hairline the first time (0.657% of canvas, under the skill's
        # 0.8% floor); naming a fraction of the photograph's own height overshot
        # to 5.5%. Tying it to the photograph's height *and* naming a canvas
        # ceiling lands it at 1.34%.
        type_and_accent=(
            "To the right of the photograph, three lines of very small serif "
            "archive microtext, semi-legible, reading like a specimen label with a "
            "date and a weather note. The single high-chroma element is a violet "
            "printed bar sitting directly beneath the photograph, the same width "
            "as the photograph and only about one fifth of the photograph's "
            "height — a compact solid block, clearly thicker than a rule but "
            "SMALL on the sheet, covering no more than about 1.5% of the whole "
            "sheet and about 20% of the small cluster. It is flat opaque "
            "spot-colour violet, one uniform vivid tone edge to edge, fully "
            "saturated and dense, nothing showing through it: no paper texture, "
            "no halftone, no transparency, no gradient. Everything else is grey."
        ),
        text=["almost nothing, for a week", "APR 06  15:40  overcast, no wind"],
        note="花期短得像什么都没发生。左下角一小块，上面 88% 全是空纸——空的部分才是主角。",
    ),
    Page(
        pid=35,
        photo="p06.jpeg",
        season="spring",
        title="the field kept the small ones",
        title_zh="田野把小的那些留下了",
        layout="dot-orbit",
        anchor="object specimen",
        typography="diagonal scattered words",
        texture="halftone degradation",
        mood="slight surrealism",
        accent="lemon yellow",
        accent_hex="#F5C400",
        cluster=(
            "About 85% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 12% of the canvas, centred slightly low on the sheet, "
            "well inside all four edges."
        ),
        subject=(
            "The cluster is one single dandelion flower lifted out of the attached "
            "photograph and presented as a pressed botanical specimen, small and "
            "isolated on the paper, printed in coarse degraded halftone so the "
            "petals break into visible dots. A faint ring of tiny grey printed dots "
            "orbits it at a distance, like the other flowers in the field reduced "
            "to registration marks."
        ),
        type_and_accent=(
            "A handful of small serif words run diagonally across the lower right, "
            "scattered rather than set in a line. The single high-chroma element is "
            "the flower head itself, printed in solid, fully saturated lemon-yellow "
            "ink — opaque and vivid, not pale and not washed out — about 1.5% of the "
            "whole sheet and about 20% of the cluster. The orbiting dots, the type "
            "and the paper stay grey."
        ),
        text=["the field kept the small ones"],
        note="一整片蓝紫里只挑出一朵，其余的降级成印刷网点。黄色不是加上去的强调，黄色就是那朵花本身。",
    ),
    # ---------------------------------------------------------------- SUMMER
    Page(
        pid=36,
        photo="p04.jpeg",
        season="summer",
        title="the water never stopped to look",
        title_zh="水没停下来看一眼",
        layout="upper-right-block",
        anchor="tiny faded photo",
        typography="short phrase pressed against the image edge",
        texture="scan noise and paper fibers",
        mood="summer",
        accent="cyan",
        accent_hex="#00A6C8",
        cluster=(
            "About 85% of the sheet is plain empty paper, most of it across the "
            "bottom half. One small visual cluster occupies roughly 12% of the "
            "canvas, placed in the upper-right area, clear of the edges."
        ),
        subject=(
            "The cluster is the attached photograph reproduced as a small vertical "
            "print about one quarter of the sheet width, low contrast and grainy "
            "with visible scan noise and paper fibre over it. Keep its subject "
            "exactly as given: a tall waterfall dropping in a single white column "
            "into a pale pool, dark trees crowding both sides."
        ),
        type_and_accent=(
            "One short line of small serif type is pressed hard against the left "
            "edge of the photograph, so tight that the last letters almost touch "
            "the print. The single high-chroma element is a solid, fully saturated "
            "cyan block printed directly over the falling water, a clean opaque "
            "rectangle that turns the waterfall itself into colour, about 1.7% of "
            "the whole sheet and about 21% of the cluster. Nothing else is coloured."
        ),
        text=["the water never stopped to look"],
        note="瀑布本身被一块青色实心块盖住——水是唯一有颜色的东西，也是唯一不肯停的东西。",
    ),
    Page(
        pid=37,
        photo="p11.jpeg",
        season="summer",
        title="still going, nobody near",
        title_zh="还在喷，附近没有人",
        layout="single-specimen",
        anchor="object specimen",
        typography="almost textless, only a tiny caption",
        texture="letterpress ink bleed",
        mood="afternoon",
        accent="tomato red",
        accent_hex="#E03A24",
        cluster=(
            "About 88% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 10% of the canvas, standing alone in the middle of the "
            "sheet with a great deal of air above and below it."
        ),
        subject=(
            "The cluster is the stone fountain from the attached photograph, cut out "
            "from its background and presented as one isolated specimen on bare "
            "paper — a three-tiered basin fountain, small, printed as a soft grey "
            "letterpress illustration with visible ink bleed at the edges of the "
            "stone. No park, no trees, no people, no ground: the object floats on "
            "the paper by itself."
        ),
        type_and_accent=(
            "One tiny serif caption sits well below the object, small enough to read "
            "as a museum label. The single high-chroma element is a solid, fully "
            "saturated tomato-red disc printed at the base of the fountain where the "
            "water would pool, opaque and slightly bled into the paper fibre, a "
            "large disc about as wide as the widest basin of the fountain, about "
            "2.2% of the whole sheet and about 24% of the cluster, vivid enough to "
            "read as a colour event at thumbnail size. Nothing else carries colour."
        ),
        text=["still going, nobody near"],
        note="把喷泉从公园里抠出来，单独放在空纸上。水池换成一枚红色实心圆——机器还在运转，观众早就走了。",
    ),
    Page(
        pid=38,
        photo="p14.jpeg",
        season="summer",
        title="one tree stayed green longer",
        title_zh="有一棵绿得比别的久",
        layout="dual-panel",
        anchor="tiny faded photo beside a solid colour block",
        typography="text inside the colour block",
        texture="aged paper mottling",
        mood="quiet",
        accent="pear green",
        accent_hex="#5FA80F",
        cluster=(
            "About 83% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 14% of the canvas, sitting just below the middle of "
            "the sheet, away from all edges."
        ),
        subject=(
            "The cluster is two small panels side by side with a narrow gap between "
            "them. The left panel is the attached photograph reproduced small and "
            "grey and grainy — keep its subject exactly as given: one slender birch "
            "in full leaf standing in front of a darker treeline, grass in front of "
            "it. The right panel is the same height but narrower."
        ),
        type_and_accent=(
            "The right panel is the single high-chroma element: a solid, fully "
            "saturated pear-green printed block, opaque and even, about 2.0% of the "
            "whole sheet and about 24% of the cluster, with one short line of small "
            "serif type reversed out of it in the paper colour. The photograph, the "
            "gap and the rest of the sheet stay grey and paper-toned."
        ),
        text=["one tree stayed green longer"],
        note="左边是照片里那棵树的灰印，右边是一块纯绿。文字反白压在绿块里——颜色被从照片里抽出来，单独放到旁边。",
    ),
    Page(
        pid=39,
        photo="p13.jpeg",
        season="summer",
        title="the sky pressed down",
        title_zh="天压下来了",
        layout="type-led",
        anchor="flat silhouette",
        typography="headline-as-object with rough letterpress",
        texture="risograph grain",
        mood="slight surrealism",
        accent="ultramarine",
        accent_hex="#2331B8",
        cluster=(
            "About 82% of the sheet is plain empty paper. One visual cluster "
            "occupies roughly 15% of the canvas, sitting across the middle band of "
            "the sheet with clear paper above and below."
        ),
        subject=(
            "Typography is the main object here and the image is secondary. Beneath "
            "the type sits one small flat black silhouette taken from the attached "
            "photograph: a single low round bush alone on flat ground, reduced to a "
            "solid dark shape with no interior detail, no sky, no trees behind it."
        ),
        type_and_accent=(
            "The phrase is set large for this poster in rough letterpress serif "
            "capitals, ink-heavy and slightly broken, sitting directly above the "
            "silhouette and behaving like an object rather than a caption. The "
            "single high-chroma element is that headline itself, printed in solid, "
            "fully saturated ultramarine ink, opaque and undiluted, about 2.1% of "
            "the whole sheet and about 26% of the cluster. The silhouette and the "
            "paper stay grey."
        ),
        text=["THE SKY PRESSED DOWN"],
        note="这张反过来：字是主角，图退成一个黑色团块。群青的字压在灌木上方——天不是画出来的，是排出来的。",
    ),
    # ---------------------------------------------------------------- AUTUMN
    Page(
        pid=40,
        photo="p10.jpeg",
        season="autumn",
        title="it was already leaving",
        title_zh="它已经在走了",
        layout="single-specimen",
        anchor="object specimen",
        typography="archive microtext with date and weather",
        texture="film grain photo",
        mood="solitude",
        accent="orange",
        accent_hex="#E8681C",
        cluster=(
            "About 87% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 10% of the canvas, placed a little above centre, with "
            "a large empty field of paper beneath it."
        ),
        subject=(
            "The cluster is one dandelion seed head from the attached photograph, "
            "lifted out and presented as a single specimen on bare paper — the round "
            "grey sphere of seeds on its long thin stem, printed with fine film "
            "grain, soft and almost transparent at the edges where the seeds are "
            "coming loose. A few seeds have already detached and drift away to one "
            "side. No field, no background, no other plants."
        ),
        type_and_accent=(
            "Two lines of very small serif archive microtext sit low and to one "
            "side, semi-legible, like a herbarium slip. The single high-chroma "
            "element is a solid, fully saturated orange printed square sitting "
            "behind the seed head and offset from it, so the grey sphere overlaps "
            "the colour, about 1.6% of the whole sheet and about 20% of the cluster, "
            "opaque and clean-edged. No other colour anywhere."
        ),
        text=["it was already leaving", "SEP 21  17:05  dry"],
        note="蒲公英絮是这 14 张里唯一自带「秋」的东西——不是颜色变了，是结构在散。橙色方块放在它背后，像它正在离开的那个位置。",
    ),
    Page(
        pid=41,
        photo="p07.jpeg",
        season="autumn",
        title="the colour started to rust",
        title_zh="颜色开始生锈",
        layout="dual-panel",
        anchor="torn-paper clipping",
        typography="low-contrast grey ghost text",
        texture="halftone degradation",
        mood="memory",
        accent="cyan",
        accent_hex="#00A0B4",
        cluster=(
            "About 84% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 13% of the canvas, placed just left of centre and a "
            "little low, clear of every edge."
        ),
        subject=(
            "The cluster is two overlapping torn paper clippings. The larger one is "
            "the attached photograph — keep its subject exactly as given: a broad "
            "tree covered in dusty mauve-red blossom over green grass — printed in "
            "coarse degraded halftone with every trace of colour removed: no green "
            "grass, no mauve blossom, no blue sky survives — the whole clipping is "
            "grey newsprint dots and nothing else. The smaller clipping behind it "
            "is blank torn paper, slightly darker, showing only along one edge."
        ),
        type_and_accent=(
            "One line of low-contrast grey ghost type sits on the bare paper just "
            "below the torn edge, faint enough to be almost lost but never printed "
            "on top of the clipping. The single high-chroma element is a solid, "
            "fully saturated cyan printed bar running the full height of the right "
            "edge of the larger clipping, wide and opaque and cold against the grey "
            "halftone, about 2.2% of the whole sheet and about 24% of the cluster. "
            "It is the only colour anywhere on the sheet."
        ),
        text=["the colour started to rust"],
        note="花还在，但网点已经把颜色拆散了。右边压一条冷青——用一个不属于这个季节的颜色，把「褪」这件事标出来。",
    ),
    Page(
        pid=42,
        photo="p08.jpeg",
        season="autumn",
        title="too much of it at once",
        title_zh="一次给得太多了",
        layout="irregular-cutout",
        anchor="abstract texture window",
        typography="fragmented floating letters",
        texture="xerox softness",
        mood="slight surrealism",
        accent="lemon yellow",
        accent_hex="#EFC000",
        cluster=(
            "About 85% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 12% of the canvas, placed in the upper-left area, well "
            "inside the edges."
        ),
        subject=(
            "The cluster is an irregular organic paper cutout — a torn window shape "
            "with soft photocopied edges — and inside that window is a tight crop of "
            "the attached photograph used as pure texture rather than as a scene: "
            "the dense mass of small dark blossom, so close in that no tree, no sky "
            "and no horizon can be read, only an all-over pattern. Printed soft and "
            "grey with xerox wear."
        ),
        type_and_accent=(
            "Small serif letters float free around the cutout, broken apart and "
            "drifting, never forming a straight line. The single high-chroma element "
            "is a solid, fully saturated lemon-yellow shape torn to the same organic "
            "language as the window and butting against its lower edge, opaque and "
            "vivid, about 1.7% of the whole sheet and about 21% of the cluster. "
            "Everything else is grey."
        ),
        text=["too much of it at once"],
        note="凑得太近，花变成了没有主体的花纹。开得过头和烂掉之间只差几天，这张卡在那几天里。",
    ),
    # ---------------------------------------------------------------- WINTER
    Page(
        pid=43,
        photo="p01.jpeg",
        season="winter",
        title="the fog took the garden",
        title_zh="雾把花园收走了",
        layout="center-fragment",
        anchor="tiny faded photo",
        typography="short phrase pressed against the image edge",
        texture="aged paper mottling",
        mood="solitude",
        accent="tomato red",
        accent_hex="#D93A2B",
        cluster=(
            "About 87% of the sheet is plain empty paper. One small visual cluster "
            "occupies roughly 10% of the canvas, sitting dead centre with a wide "
            "margin of empty paper on every side."
        ),
        subject=(
            "The cluster is the attached photograph reproduced very small, about one "
            "fifth of the sheet width, faded almost to nothing so the image is "
            "barely holding together. Keep its subject exactly as given: an "
            "ornamental tiered fountain standing in thick haze with the hedge behind "
            "it dissolving away. Printed pale and soft with aged paper mottling "
            "showing through the image."
        ),
        type_and_accent=(
            "One short line of small serif type is pressed against the bottom edge "
            "of the photograph, touching it. The single high-chroma element is a "
            "solid, fully saturated tomato-red printed square placed just outside "
            "the top-right corner of the photograph, sitting on bare paper and not "
            "overlapping the image, roughly half as wide as the photograph itself, "
            "about 2.2% of the whole sheet and about 24% of the cluster, opaque and "
            "hard-edged against the haze. No other colour."
        ),
        text=["the fog took the garden"],
        note="照片淡到快要散掉，红色方块却硬得像钉子，钉在纸上。雾能吃掉花园，吃不掉油墨。",
    ),
    Page(
        pid=44,
        photo="p05.jpeg",
        season="winter",
        title="it looked like frost",
        title_zh="看上去像霜",
        layout="lower-left-float",
        anchor="translucent geometric overlay",
        typography="diagonal scattered words",
        texture="letterpress ink bleed",
        mood="memory",
        accent="cobalt blue",
        accent_hex="#1746C4",
        cluster=(
            "About 86% of the sheet is plain empty paper, nearly all of it above. "
            "One small visual cluster occupies roughly 11% of the canvas, floating "
            "low and to the left, not touching any edge."
        ),
        subject=(
            "The cluster is the attached photograph reproduced as a small print — "
            "keep its subject exactly as given: a white blossoming tree standing in "
            "a field under a violet-grey haze, the whole scene so pale and cold it "
            "reads as frost rather than as flowers. Printed grey and low contrast "
            "with letterpress ink bleed softening its edges."
        ),
        type_and_accent=(
            "A few small serif words run diagonally up and away from the print, "
            "scattered and unaligned. The single high-chroma element is a "
            "translucent geometric overlay: a solid, fully saturated cobalt-blue "
            "printed triangle laid across the upper half of the photograph so the "
            "tree shows faintly through it, opaque enough to stay vividly blue where "
            "it sits on bare paper, about 1.8% of the whole sheet and about 22% of "
            "the cluster. Nothing else on the sheet is coloured."
        ),
        text=["it looked like frost"],
        note="满树白花冷成了霜。一块钴蓝的三角斜压过去——不是天空，是玻璃，是隔着看的那层东西。",
    ),
    Page(
        pid=45,
        photo="p12.jpeg",
        season="winter",
        title="someone stood very still",
        title_zh="有人站着一动不动",
        layout="single-specimen",
        anchor="flat silhouette",
        typography="almost textless, only a tiny caption",
        texture="scan noise and paper fibers",
        mood="solitude",
        accent="orange",
        accent_hex="#F06A11",
        cluster=(
            "About 89% of the sheet is plain empty paper — this is the emptiest "
            "sheet in the set. One very small visual cluster occupies roughly 8% of "
            "the canvas, placed low and slightly right of centre, with an enormous "
            "field of blank paper above it."
        ),
        subject=(
            "The cluster is one standing human figure taken from the attached "
            "photograph and reduced to a small flat grey silhouette on bare paper — "
            "the blurred outline of a person facing forward, arms down, alone. No "
            "grass, no hills, no sky, no ground line: the figure stands on nothing. "
            "Printed with visible scan noise and paper fibre so the outline is soft "
            "and uncertain at its edges."
        ),
        type_and_accent=(
            "One tiny serif caption sits directly beneath the figure, small and "
            "quiet. The single high-chroma element is a solid, fully saturated "
            "orange printed square on the paper immediately to the right of the "
            "figure, at the same height as its head, opaque and clean, about as "
            "tall as the figure's head and shoulders together, about 2.2% of the "
            "whole sheet and about 24% of the cluster. It is the only colour on "
            "the sheet."
        ),
        text=["someone stood very still"],
        note="人被抽成一个模糊的灰影，脚下什么都没有。右边平齐头部放一枚橙色方块——是另一个人，还是他在等的东西，不说。",
    ),
)


def build(page: Page) -> str:
    """Compile one page into the skill's four-paragraph Standard Mode shape."""
    return "\n\n".join(
        [
            f"{PAPER} {page.cluster}",
            page.subject,
            f"{page.type_and_accent} {whitelist(page.text)}",
            AVOID,
        ]
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", type=int, help="print a single page")
    args = ap.parse_args()

    for p in PAGES:
        if args.id and p.pid != args.id:
            continue
        print("=" * 78)
        print(f"{p.pid}  {p.season:6s}  {p.title}   [{p.photo}]")
        print(f"recipe: {p.layout} / {p.anchor} / {p.typography} / "
              f"{p.accent} / {p.texture} / {p.mood}")
        print("=" * 78)
        print(build(p))
        print()


if __name__ == "__main__":
    main()
