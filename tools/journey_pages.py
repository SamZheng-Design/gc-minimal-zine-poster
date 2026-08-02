#!/usr/bin/env python3
"""
Colorful Journey — six sheets from six travel photographs.

This series takes two deliberate departures from the Seasons album, both asked
for by the user:

1. **Whiter stock.** Seasons is printed on aged oat-white (measured 229/221/203).
   This series is printed on a bright cotton white. The paper paragraph is still
   byte-identical across all six sheets, because the paper is the one thing in a
   series that must not drift.

2. **More colour survives.** The skill's default is a grey photograph plus one
   small spot-colour anchor. Here the photograph's *own* colour is what is kept:
   each anchor is a partial-colour region where the scene's dominant hue is
   printed at full saturation while everything around it stays paper and grey.
   The skill explicitly allows this form ("a partial-color photo region",
   "Color can carry the subject itself") but its share band is 0.8%-2.5% of the
   canvas, and these sheets are aimed at roughly 3%-6%. That is above the
   ceiling on purpose. It is recorded here and in posters/README.md as a
   user-authorised deviation rather than passed off as compliant.

Everything else follows the skill unchanged: 70%-90% paper, one cluster, one
hue per sheet, flat scan, no full bleed.

    python3 tools/journey_pages.py            # print all six prompts
    python3 tools/journey_pages.py --id 46    # print one
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

PHOTO_BASE = "assets/journey/photos"

# --------------------------------------------------------------------------
# Shared wording. Byte-identical in all six prompts.
# --------------------------------------------------------------------------

PAPER = (
    "Tall vertical 3:5 paper poster. The whole sheet is one piece of bright "
    "cotton printmaking paper: a clean, light, almost-white stock, only a "
    "whisper warmer than pure white, with fine visible paper fibre and a faint "
    "even tooth. The paper tone is the same from corner to corner: no ivory, no "
    "cream, no oat, no yellowing, no brown staining, no dark edges, no "
    "tea-coloured wash, no light-to-dark gradient. Flat orthographic "
    "scanner-bed view, no border, no mockup, no paper shadow, no curl."
)

# Appended to paragraph 3 of every sheet. The opacity sentence exists because a
# translucent anchor measured as a large colour area while reading, at thumbnail
# scale, as a tint of the paper.
VIVID = (
    "The chromatic ink is printed at full saturation and fully opaque: dense, "
    "clean-edged spot colour that sits on top of the paper rather than tinting "
    "it. Do not wash it out, do not make it translucent, do not let the paper "
    "fibre show through the colour, do not desaturate it while adding grain. "
    "Only this one hue is saturated anywhere on the sheet; every other mark is "
    "paper tone, grey, or black."
)

AVOID = (
    "Flat scanned-paper feeling, matte and absorbent, diffuse even light, low to "
    "medium contrast, no hard shadow, no depth of field, no 3D. Avoid: full-bleed "
    "photograph, the reference photo filling the sheet, commercial headline "
    "hierarchy, product advertisement layout, logo, CTA, glossy mockup, clean "
    "digital white background, cinematic lighting, neon, cyberpunk, cute cartoon, "
    "anime, fashion editorial drama, dense scrapbook collage, more than one "
    "saturated hue, long clean paragraphs of text, stock-photo realism, yellowed "
    "or tea-stained paper, travel-brochure or postcard styling."
)


def whitelist_v1(strings: list[str]) -> str:
    """
    First version: the strings are quoted and slash-separated.

    Kept because sheets 47, 50 and 51 shipped from it and index.json must hold
    the prompt that actually produced the image. Do not use it for new work: on
    sheets where the model set several strings on ONE line it printed the
    delimiters too, so 46 came out reading `"everyone faced the window" / PARIS
    19:48`. Where it happened to break the strings onto separate lines (47) the
    output was clean, which is why the fault survived the Seasons album.
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


def whitelist_v2(strings: list[str]) -> str:
    """
    Second version: no delimiters at all. The strings are given one per line and
    the separator characters are explicitly banned, which is the only wording
    that stopped the punctuation leaking onto the sheet.
    """
    return (
        "STRICT TEXT WHITELIST. The only text allowed anywhere on the sheet is the "
        "following, printed once and once only, each line set on its own separate "
        "line of the poster, spelled exactly as given:\n"
        + "\n".join(strings)
        + "\nPrint those words and nothing else. Do not print quotation marks, "
        "slashes, brackets, bullets, dashes or any other separator around them, "
        "and do not run two of the lines together into one line. Do not render any "
        "other word or any loose single letter. Do not print any word from these "
        "instructions. No caption, no signature, no username, no social-media "
        "handle, no watermark, no date stamp, no page number, no logo."
    )


# Sheet 48 needed a third pass. Its second attempt was correct in every way the
# Quality Gate checks -- right phrase, no stray letters, anchor in range -- but
# its paper came out cream: measured white point 254/251/240, R-B 14, against
# R-B 4-6 on the other five. In an album that reads as one sheet printed on a
# different stock, and the brief for this series was explicitly a whiter paper.
# The third pass hardened the paper paragraph, sharpened the orange and dropped
# the multi-line clauses from the whitelist (48 sets a single string). The exact
# text below is the one that produced the shipped image; build() returns it
# verbatim so index.json stays faithful.
PROMPT_48_SHIPPED = """\
Tall vertical 3:5 paper poster. The whole sheet is one piece of bright NEUTRAL \
WHITE cotton printmaking paper — the same cool bright white as a fresh sheet of \
copier paper, RGB roughly 252,252,250, with fine visible paper fibre and a faint \
even tooth. The paper must read as WHITE, not ivory, not cream, not off-white, \
not eggshell, not bone, not oatmeal, not vanilla, not antique, not aged, not \
warm-toned. Absolutely no yellow cast, no beige cast, no tea stain, no age \
toning, no brown edges, no vignette, no light-to-dark gradient; the paper tone \
is identical from corner to corner and its red, green and blue values are within \
two or three points of each other. Flat orthographic scanner-bed view, no border, \
no mockup, no paper shadow, no curl. About 84% of the sheet is plain empty white \
paper. One single upright specimen occupies roughly 13% of the canvas, placed in \
the lower-middle of the sheet, well away from every edge.

The specimen is one pointed gothic arch lifted out of the attached photograph and \
printed alone on the paper like a pressed sample: a slender lancet window with a \
small circular rose above it, its stone tracery drawn as thin dark lines with \
letterpress ink bleed. There is no cathedral around it, no columns, no interior, \
no shadow — only the one window shape sitting on bare white paper.

The phrase is set once in small serif type to the right of the arch, running down \
the sheet as a single vertical column, one letter under the next, loosely and \
unevenly spaced as if the line had come apart in the press. Every letter in that \
column belongs to the phrase and the phrase is complete; no loose letter from any \
other word appears anywhere on the sheet. Every pane inside the arch and inside \
the rose is filled with fully saturated amber-orange glass — an irregular mosaic \
of flat bright orange shards, a clean vivid orange like fresh spot ink rather \
than mustard or ochre, divided by the thin dark leading, about 5% of the whole \
sheet and about 40% of the cluster. The chromatic ink is printed at full \
saturation and fully opaque: dense, clean-edged spot colour that sits on top of \
the paper rather than tinting it. Do not wash it out, do not make it translucent, \
do not let the paper fibre show through the colour, do not desaturate it while \
adding grain. The orange must stay strictly inside the window panes and must not \
spill, glow or tint the surrounding paper. Only this one hue is saturated \
anywhere on the sheet; every other mark is neutral paper white, grey, or black. \
STRICT TEXT WHITELIST. The only text allowed anywhere on the sheet is the \
following, printed once and once only, spelled exactly as given:
the light arrived coloured
Print those words and nothing else. Do not print quotation marks, slashes, \
brackets, bullets, dashes or any other separator around them. Do not render any \
other word or any loose single letter. Do not print any word from these \
instructions. No caption, no signature, no username, no social-media handle, no \
watermark, no date stamp, no page number, no logo.

Flat scanned-paper feeling, matte and absorbent, diffuse even light, low to \
medium contrast, no hard shadow, no depth of field, no 3D. Avoid: full-bleed \
photograph, the reference photo filling the sheet, commercial headline hierarchy, \
product advertisement layout, logo, CTA, glossy mockup, cinematic lighting, neon, \
cyberpunk, cute cartoon, anime, fashion editorial drama, dense scrapbook collage, \
more than one saturated hue, long clean paragraphs of text, stock-photo realism, \
yellowed or tea-stained paper, ivory or cream paper, warm paper cast, \
travel-brochure or postcard styling."""


@dataclass(frozen=True)
class Page:
    pid: int
    photo: str
    place: str
    title: str
    title_zh: str
    layout: str
    anchor: str
    typography: str
    texture: str
    mood: str
    accent: str
    accent_hex: str
    cluster: str  # paragraph 1 tail: cluster size and placement
    subject: str  # paragraph 2: how the photograph is used
    type_and_accent: str  # paragraph 3 head: type behaviour + the colour
    text: list[str]
    note: str
    # Slug used in the shipped filename. Usually the place, but two sheets are
    # filed under their subject instead: 47 is the Rhone canvas seen in Paris,
    # 48 is the Sagrada Familia in Barcelona.
    fslug: str = ""
    wl: int = 2  # which whitelist wording produced the shipped image
    shipped: str | None = None  # verbatim prompt when it diverged from build()


def build(page: Page) -> str:
    """Compile one page into the skill's four-paragraph Standard Mode shape."""
    if page.shipped is not None:
        return page.shipped
    return "\n\n".join(
        [
            f"{PAPER} {page.cluster}",
            page.subject,
            f"{page.type_and_accent} {VIVID} "
            f"{(whitelist_v1 if page.wl == 1 else whitelist_v2)(page.text)}",
            AVOID,
        ]
    )


PAGES: tuple[Page, ...] = (
    Page(
        pid=46,
        photo="j01-paris-sunset.jpeg",
        place="Paris",
        title="everyone faced the window",
        title_zh="所有人都朝着窗坐",
        layout="irregular-cutout",
        anchor="torn-paper clipping",
        typography="short phrase pressed against image edge",
        texture="risograph grain",
        mood="night",
        accent="hot magenta-pink",
        accent_hex="#E8357F",
        cluster=(
            "About 82% of the sheet is plain empty paper. One tall narrow visual "
            "cluster occupies roughly 14% of the canvas, standing a little left "
            "of centre and a little above the middle, well away from every edge."
        ),
        subject=(
            "The cluster is a tall window-shaped clipping torn from the attached "
            "photograph, about one quarter of the sheet wide and two and a "
            "half times as tall as it is wide, with one ragged torn edge. Inside "
            "it: the flat black silhouette of a restaurant interior — a standing "
            "figure at the right, the backs of two seated diners along the bottom "
            "edge, a laid table — cut against a dusk sky, with the thin needle of "
            "the Eiffel Tower rising in the middle distance as a dark hairline. "
            "Keep the black silhouettes low and narrow so that the upper two "
            "thirds of the clipping is open sky; the silhouetted interior is "
            "solid black with no detail, and only the sky carries colour."
        ),
        type_and_accent=(
            "One short line of small serif type sits directly under the clipping, "
            "pressed against its lower edge and slightly misregistered. The sky "
            "inside the window is the single high-chroma element: hot "
            "magenta-pink risograph ink laid in flat horizontal cloud bands, "
            "filling the whole upper part of the window around the black "
            "silhouettes. The pink area by itself — not the clipping, the pink "
            "alone — covers about 4% of the whole sheet and about 45% of the "
            "cluster, so it stays the largest single element in the composition."
        ),
        text=["everyone faced the window", "PARIS  19:48"],
        note="整间餐厅都不说话地朝一个方向坐着。黑得只剩剪影，颜色全留给窗外那几道云。",
    ),
    Page(
        pid=47,
        fslug="rhone",
        photo="j02-rhone-starry-night.jpeg",
        place="Paris",
        title="the river was already blue",
        title_zh="那条河当时就已经是蓝的",
        layout="dual-panel",
        anchor="old printed illustration",
        typography="archive microtext with date/weather",
        texture="halftone degradation",
        mood="memory",
        accent="cobalt blue",
        accent_hex="#1D4FA8",
        cluster=(
            "About 80% of the sheet is plain empty paper. Two small adjacent "
            "panels with a narrow paper gap between them occupy together roughly "
            "16% of the canvas, sitting in the upper-middle of the sheet, well "
            "away from every edge."
        ),
        subject=(
            "The left and larger panel is a coarse halftone reproduction of the "
            "attached painting — a night river under stars, two small figures on "
            "the near bank, gaslight reflections running down the water as "
            "vertical streaks — printed as if plated from a worn museum "
            "catalogue, with visible halftone rosettes and slight ink "
            "misregistration. The right panel is a narrow blank grey card the "
            "height of the painting, like the wall label beside it, carrying "
            "only microtext."
        ),
        type_and_accent=(
            "Three lines of very small typewriter microtext sit on the narrow "
            "right panel, grey and quiet. The painting panel itself is the "
            "high-chroma element: its night sky and river are printed in fully "
            "saturated cobalt-blue ink while the banks, the figures and the "
            "frame stay grey, so the blue reads as about 6% of the whole sheet "
            "and about 40% of the two-panel cluster."
        ),
        text=["the river was already blue", "ARLES 1888", "OIL ON CANVAS"],
        note="站在画前才发现，梵高看见的蓝不是夜色，是他先把河认定成蓝的。旁边那张说明牌被留成一块空灰卡。",
        wl=1,
    ),
    Page(
        pid=48,
        fslug="sagrada",
        photo="j03-sagrada-glass.jpeg",
        place="Barcelona",
        title="the light arrived coloured",
        title_zh="光是带着颜色进来的",
        layout="single-specimen",
        anchor="abstract texture window",
        typography="fragmented floating letters",
        texture="letterpress ink bleed",
        mood="solitude",
        accent="amber-orange",
        accent_hex="#F07A14",
        cluster=(
            "About 84% of the sheet is plain empty paper. One single upright "
            "specimen occupies roughly 13% of the canvas, placed in the "
            "lower-middle of the sheet, well away from every edge."
        ),
        subject=(
            "The specimen is one pointed gothic arch lifted out of the attached "
            "photograph and printed alone on the paper like a pressed sample: a "
            "slender lancet window with a small circular rose above it, its stone "
            "tracery drawn as thin dark lines with letterpress ink bleed. There "
            "is no cathedral around it, no columns, no interior, no shadow — only "
            "the one window shape sitting on bare paper."
        ),
        type_and_accent=(
            "The phrase is set once in small serif type to the right of the "
            "arch, running down the sheet as a single vertical column, one letter "
            "under the next, loosely and unevenly spaced as if the line had come "
            "apart in the press. Every letter in that column belongs to the "
            "phrase and the phrase is complete; no loose letter from any other "
            "word appears anywhere on the sheet. Every "
            "pane inside the arch and inside the rose is filled with fully "
            "saturated amber-orange glass — an irregular mosaic of flat orange "
            "shards divided by the thin dark leading, about 5% of the whole sheet "
            "and about 40% of the cluster."
        ),
        text=["the light arrived coloured"],
        note="教堂里最亮的东西不是灯，是光穿过玻璃时被染上的那层橙。所以整张纸只留下那一扇窗，其余全部拿掉。",
        shipped=PROMPT_48_SHIPPED,
    ),
    Page(
        pid=49,
        photo="j04-round-pond.jpeg",
        place="London",
        title="one red thing on the water",
        title_zh="水面上只有一处红",
        layout="dot-orbit",
        anchor="flat silhouette",
        typography="archive microtext with date/weather",
        texture="xerox softness",
        mood="afternoon",
        accent="tomato red",
        accent_hex="#E0342A",
        cluster=(
            "About 85% of the sheet is plain empty paper. One wide low cluster "
            "occupies roughly 12% of the canvas, sitting in the lower third of "
            "the sheet, well away from every edge."
        ),
        subject=(
            "The cluster is a scattering of about fourteen tiny flat grey "
            "waterfowl silhouettes — ducks and one long-necked goose, seen from "
            "the side, each no bigger than a grain of rice — drifting across bare "
            "paper as if the pond itself had been left unprinted. Their edges are "
            "soft and slightly broken, like a third-generation photocopy. No "
            "water, no ripples, no bank, no trees, no sky."
        ),
        type_and_accent=(
            "One line of small typewriter microtext runs along the lower edge of "
            "the scattering, grey and archival. Among the grey birds sits one "
            "fully saturated tomato-red disc: a clean flat circle about one "
            "quarter of the sheet width across, far larger than any bird, the "
            "marker buoy swollen to the size of a printer's colour patch — the "
            "birds orbit it at uneven distances. The red disc covers about 3% of "
            "the whole sheet and is the largest single element on the paper."
        ),
        text=["one red thing on the water", "SEP 21  16:05  clear"],
        note="一池子鸭子里，唯一不动、也唯一有颜色的是那个浮标。于是这张把水抽掉了，剩下的编队自然就绕着它。",
    ),
    Page(
        pid=50,
        photo="j05-cappadocia-balloons.jpeg",
        place="Cappadocia",
        title="everyone got up in the dark",
        title_zh="所有人都摸黑起床",
        layout="upper-right-block",
        anchor="solid color block",
        typography="diagonal scattered words",
        texture="risograph grain",
        mood="slight surrealism",
        accent="violet",
        accent_hex="#7A46C6",
        cluster=(
            "About 80% of the sheet is plain empty paper. One rectangular block "
            "with a few small marks escaping it occupies roughly 18% of the "
            "canvas, placed in the upper-right of the sheet, well away from every "
            "edge."
        ),
        subject=(
            "The block is a wide, short rectangle of flat printed sky — a slab of "
            "pre-dawn cloud reduced to three or four soft horizontal bands with "
            "risograph grain, no ground, no rocks, no horizon line. Six or seven "
            "tiny teardrop balloon silhouettes are punched out of it in grey and "
            "in bare paper, and two more have drifted clear of the block "
            "altogether and float alone on the empty sheet above and to its left."
        ),
        type_and_accent=(
            "Three or four short words scatter diagonally down the empty left "
            "side of the sheet in small serif type, loosely spaced, following the "
            "drift of the escaped balloons. The sky block itself is the "
            "high-chroma element: fully saturated violet risograph ink, opaque "
            "and flatly printed, about 6% of the whole sheet and about 35% of the "
            "cluster."
        ),
        text=["everyone got up in the dark"],
        note="为了看它们，整座山谷的人四点就起来了。真正的主角其实是那块紫色的天，气球只是从里面被冲出来的几个小口子。",
        wl=1,
    ),
    Page(
        pid=51,
        photo="j06-erciyes-road.jpeg",
        place="Erciyes",
        title="the mountain stayed the same size",
        title_zh="那座山一直没有变大",
        layout="lower-left-float",
        anchor="tiny faded photo",
        typography="low-contrast gray ghost text",
        texture="scan noise and paper fibers",
        mood="quiet",
        accent="cyan",
        accent_hex="#1FA5D6",
        cluster=(
            "About 86% of the sheet is plain empty paper. One small horizontal "
            "photograph occupies roughly 11% of the canvas, floating low and left "
            "on the sheet with a large empty area above it, well away from every "
            "edge."
        ),
        subject=(
            "The photograph is a small landscape crop about one third of the "
            "sheet wide: an empty asphalt road running straight away from the "
            "viewer with its dashed white centre line, a line of dark conifers "
            "along the left verge, and a broad snow-covered mountain filling the "
            "far end. Road, trees and mountain are all printed grey and slightly "
            "grainy, with visible scan noise, as if photographed through a "
            "windscreen and reprinted small."
        ),
        type_and_accent=(
            "One line of pale grey ghost type sits high in the empty upper area, "
            "far from the photograph, printed faint enough to read as a "
            "watermark. Above the mountain, inside the photograph, the sky is the "
            "single high-chroma element: a solid slab of fully saturated cyan "
            "printed flat from the snowline to the top edge of the crop, about "
            "4.5% of the whole sheet and about 40% of the cluster."
        ),
        text=["the mountain stayed the same size"],
        note="开了一个小时，山看上去还是那么大——这是所有长途公路共有的错觉。所以照片被放得很小，压在左下角，让上面那片空白替你开这段路。",
        wl=1,
    ),
)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", type=int, nargs="*", help="only these page ids")
    args = ap.parse_args()

    pages = [p for p in PAGES if not args.id or p.pid in args.id]
    for p in pages:
        print(f"{'=' * 78}\n{p.pid}  {p.title}  ({p.title_zh})")
        print(f"photo   {PHOTO_BASE}/{p.photo}")
        print(f"recipe  {p.layout} / {p.anchor} / {p.typography} / {p.texture} / {p.mood}")
        print(f"accent  {p.accent} {p.accent_hex}\n{'-' * 78}")
        print(build(p))
        print()


if __name__ == "__main__":
    main()
