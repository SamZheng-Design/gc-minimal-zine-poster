#!/usr/bin/env python3
"""Colorful Journey — Plates (52-57). The photograph printed as a plate.

WHY THIS SET EXISTS
-------------------
The first Colorful Journey run (46-51) did what the skill's Standard Mode tells
you to do, and the result was that the photographs almost disappeared. That is
structural, not a prompting mistake. The skill's `Image Anchor` vocabulary has
exactly eight entries --

    tiny faded photo / torn-paper clipping / flat silhouette / solid color block
    old printed illustration / object specimen / translucent geometric overlay
    abstract texture window

-- and every one of them shrinks, flattens or fragments the source image. There
is no anchor in the vocabulary that means "show the photograph properly". So
sheet 48 became a generic gothic window instead of Gaudi's glass, and sheet 49
threw away the Serpentine skyline and kept six grey ducks.

WHAT THIS SET KEEPS FROM THE SKILL
----------------------------------
    - near-white printmaking paper, flat orthographic scanner view, no mockup,
      no paper shadow, no curl
    - generous empty paper; the plate never bleeds to an edge
    - one governing hue per sheet, saturated and opaque, everything else held to
      paper tone / grey / black
    - minimal typography: one phrase, at most one small slug
    - print artefacts: riso grain, halftone, ink bleed, misregistration
    - the Variation Engine's habit of giving every sheet a different recipe

WHAT THIS SET DELIBERATELY ABANDONS
-----------------------------------
    - the Standard Color Engine's "0.8%-2.5% of canvas" anchor size. A plate
      covers 40-55% of the sheet. This is not a near-miss on the rule, it is a
      different strategy, and it is recorded as such rather than reported as a
      pass.

The two footholds that make it defensible inside the skill's own text:

    "Color can carry the subject itself. Prefer a colored tree, fruit, shell,
     flower, geometric cutout, window, poster fragment, or IMAGE PANEL over a
     gray object with one colored registration tick."          -- Color Engine

    "Always avoid: FULL-BLEED subject or scene"               -- Negatives

An image panel is sanctioned wording, and the negative constraint bans bleeding
to the edge, not scale. Every plate here sits inside wide paper margins.

The six phrases are the same as 46-51 on purpose, so the two treatments of the
same six photographs can be read side by side.
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
    "NEUTRAL WHITE cotton printmaking paper — the same cool bright white as a "
    "fresh sheet of copier paper, RGB roughly 252,252,250, with fine visible "
    "paper fibre and a faint even tooth. The paper must read as WHITE, not "
    "ivory, not cream, not eggshell, not oatmeal, not antique, not aged, not "
    "warm-toned. No yellow cast, no beige cast, no tea stain, no brown edges, "
    "no vignette, no light-to-dark gradient; the paper tone is identical from "
    "corner to corner and its red, green and blue values are within two or "
    "three points of each other. Flat orthographic scanner-bed view, no border, "
    "no mockup, no paper shadow, no curl."
)

# Appended to paragraph 3 of every sheet. The point of this series is that the
# photograph survives, so the colour clause protects image content as well as
# saturation.
PRINT = (
    "This is a printed photographic plate, not a drawing and not a flat "
    "graphic: the photograph's real shapes, depth, texture and detail all "
    "survive the printing. The chromatic ink is laid at full saturation and "
    "fully opaque — dense, clean-edged colour that sits on the paper rather "
    "than tinting it. Do not wash it out, do not make it translucent, do not "
    "desaturate it while adding grain. Outside the plate the sheet is bare "
    "white paper; the only other marks are small grey or black type."
)

AVOID = (
    "Flat scanned-paper feeling, matte and absorbent, diffuse even light on the "
    "paper itself, no hard shadow cast by the sheet, no 3D, no mockup. Avoid: "
    "the image bleeding to any edge of the sheet, a full-bleed scene, the plate "
    "touching the paper's border, commercial headline hierarchy, product "
    "advertisement layout, logo, CTA, glossy mockup, cute cartoon, anime, "
    "fashion editorial drama, dense scrapbook collage, long clean paragraphs of "
    "text, travel-brochure or postcard styling, yellowed or tea-stained paper, "
    "ivory or cream paper, warm paper cast. Do NOT reduce the photograph to a "
    "flat silhouette, a line drawing, a cartoon, a vector illustration or a "
    "single solid block of colour — the photographic image must be fully "
    "present and legible."
)


def whitelist(strings: list[str]) -> str:
    """
    Delimiter-free whitelist. Inherited from journey_pages.whitelist_v2, which
    exists because the first version quoted and slash-separated the strings and
    the model printed the punctuation onto the sheet whenever it set two of them
    on one line.
    """
    return (
        "STRICT TEXT WHITELIST. The only text allowed anywhere on the sheet is "
        "the following, printed once and once only, each line set on its own "
        "separate line of the poster, spelled exactly as given:\n"
        + "\n".join(strings)
        + "\nPrint those words and nothing else. Do not print quotation marks, "
        "slashes, brackets, bullets, dashes or any other separator around them, "
        "and do not run two of the lines together into one line. Do not render "
        "any other word or any loose single letter. Do not print any word from "
        "these instructions. No caption, no signature, no username, no "
        "social-media handle, no watermark, no date stamp, no page number, no "
        "logo."
    )


@dataclass(frozen=True)
class Plate:
    pid: int
    photo: str
    place: str
    fslug: str
    title: str
    title_zh: str
    geometry: str  # Variation axis 1: plate shape and where it sits
    treatment: str  # Variation axis 2: how colour enters the plate
    typography: str  # Variation axis 3
    texture: str  # Variation axis 4
    mood: str  # Variation axis 5
    accent: str
    accent_hex: str
    plate_para: str  # paragraph 1 tail: margins, plate geometry, placement
    image_para: str  # paragraph 2: what the photograph must show
    print_para: str  # paragraph 3 head: colour treatment + type placement
    text: list[str]
    note: str


def build(plate: Plate) -> str:
    """Compile one plate into the four-paragraph shape."""
    return "\n\n".join(
        [
            f"{PAPER} {plate.plate_para}",
            plate.image_para,
            f"{plate.print_para} {PRINT} {whitelist(plate.text)}",
            AVOID,
        ]
    )


PLATES: tuple[Plate, ...] = (
    Plate(
        pid=52,
        photo="j01-paris-sunset.jpeg",
        place="Paris",
        fslug="paris",
        title="everyone faced the window",
        title_zh="所有人都朝着窗坐",
        geometry="tall 3:4 plate, upper left",
        treatment="three-ink riso, warm gradient sky",
        typography="one line in the lower margin",
        texture="risograph grain and slight misregistration",
        mood="dusk",
        accent="hot magenta-pink into orange",
        accent_hex="#E8357F",
        plate_para=(
            "One rectangular photographic plate is printed on the sheet, a tall "
            "3:4 portrait rectangle about 62% of the sheet width, placed in the "
            "upper left with a wide clean paper margin on all four sides — a "
            "broad empty band down the right edge and a deep empty area across "
            "the bottom third. About 55% of the sheet is bare white paper."
        ),
        image_para=(
            "The plate reproduces the attached photograph in full, as a "
            "photograph: the interior of a high restaurant at sunset, shot from "
            "inside looking out. A tall grid of window mullions divides the "
            "view into panes. Against the twilight sky beyond, the Eiffel Tower "
            "stands slightly right of the plate's centre, its lattice structure "
            "clearly readable. Between the camera and the glass, the near-black "
            "silhouettes of diners: a figure standing at the right, the backs "
            "and shoulders of seated people along the bottom, a dining table "
            "with a pale cloth, a potted plant at the right edge. Depth is "
            "preserved — the silhouettes are close and large, the tower is far "
            "and small. Keep the window's grid geometry and the individual "
            "shapes of the people; do not merge them into one black mass."
        ),
        print_para=(
            "The plate is printed as a three-ink risograph: dense black for the "
            "interior silhouettes, and for the sky a hot magenta-pink laid over "
            "a band of saturated orange low at the horizon, the two blending "
            "into one continuous warm sunset gradient. That warm gradient is "
            "the only chromatic family on the sheet. Fine riso grain and a "
            "hairline misregistration where the pink and orange plates meet. "
            "The phrase is set once in small serif type in the empty paper "
            "below the plate, left-aligned to the plate's left edge; the short "
            "slug sits on its own line beneath it."
        ),
        text=["everyone faced the window", "PARIS  19:48"],
        note=(
            "第一版把这张拍成了一块粉色天空加一片黑影。真正的照片里有窗格、有远近、"
            "有一桌人各自的姿势——现在整张印出来，粉色仍然只有一个色系，但它托着的是画面，不是替代画面。"
        ),
    ),
    Plate(
        pid=53,
        photo="j02-rhone-starry-night.jpeg",
        place="Paris",
        fslug="rhone",
        title="the river was already blue",
        title_zh="那条河当时就已经是蓝的",
        geometry="landscape 5:4 plate, centred high",
        treatment="full-chroma plate, painting in its frame",
        typography="museum label line, lower left",
        texture="halftone dot and paper fibre",
        mood="museum quiet",
        accent="deep cobalt blue",
        accent_hex="#1D4FA8",
        plate_para=(
            "One landscape photographic plate is printed on the sheet, a 5:4 "
            "rectangle about 72% of the sheet width, centred left to right and "
            "sitting a little above the middle, with a wide clean paper margin "
            "all round and a large empty area filling the lower third. About "
            "58% of the sheet is bare white paper."
        ),
        image_para=(
            "The plate reproduces the attached photograph in full: Van Gogh's "
            "painting Starry Night Over the Rhone as it actually hangs, "
            "photographed straight on. The carved ornamental frame is included "
            "and is part of the image — a heavy moulded frame with a worn "
            "gilded surface, its carved relief catching the gallery light. "
            "Inside it the painting itself: the night river, the row of gas "
            "lamps along the far bank with their long yellow reflections "
            "dragged down into the water, the constellation overhead, two small "
            "figures at the near shore. The impasto is visible — thick "
            "directional brushstrokes standing up off the canvas, the ridged "
            "paint texture readable across the sky and water. Around the frame, "
            "a narrow band of the plain neutral gallery wall."
        ),
        print_para=(
            "The plate is printed at full chroma with a deep cobalt blue "
            "governing everything — the river, the sky, the shadowed wall. The "
            "lamp reflections and the frame's gilding stay warm gold, which is "
            "the subject's own second colour and must not be removed or "
            "neutralised; no third hue appears anywhere. A soft halftone dot is "
            "visible in the blue, and the paper fibre shows through the gallery "
            "wall. Three short lines of small grey serif type sit in the empty "
            "paper below the plate, left-aligned under the frame's left edge, "
            "set like a wall label."
        ),
        text=["the river was already blue", "ARLES 1888", "OIL ON CANVAS"],
        note=(
            "这张照片拍的不是画，是「在美术馆里站到这幅画面前」——所以金框和墙都留着。"
            "第一版当成「旧印刷插图」处理，把厚涂笔触磨平了，那恰恰是这张照片唯一无法替代的东西。"
        ),
    ),
    Plate(
        pid=54,
        photo="j03-sagrada-glass.jpeg",
        place="Barcelona",
        fslug="sagrada",
        title="the light arrived coloured",
        title_zh="光是带着颜色进来的",
        geometry="narrow 1:2.6 vertical strip, centred",
        treatment="full-chroma plate, light on stone",
        typography="one line at the foot of the sheet",
        texture="letterpress ink bleed in the shadows",
        mood="solitude",
        accent="amber orange",
        accent_hex="#F07A14",
        plate_para=(
            "One narrow vertical photographic plate is printed on the sheet, a "
            "tall strip roughly one part wide to two and a half parts high, "
            "about 40% of the sheet width, centred left to right and centred "
            "top to bottom, with very wide clean paper margins down both sides. "
            "About 60% of the sheet is bare white paper."
        ),
        image_para=(
            "The plate reproduces the attached photograph in full: the interior "
            "of the Sagrada Familia seen from a low angle. In the foreground, "
            "the smooth curved stone banister of a staircase sweeps up from the "
            "bottom of the plate and away to the right — its polished surface "
            "is the single most important thing in the picture, because the "
            "coloured light from the windows is lying across it as a soft warm "
            "glow. Behind and above it, tall narrow stained-glass windows rise "
            "the full height of the plate, their panes glowing. A structural "
            "column edges the right side in deep shadow. Keep the low viewpoint, "
            "the curve of the banister, and the light falling onto the stone — "
            "this is a photograph of light on a surface, not a picture of a "
            "window."
        ),
        print_para=(
            "The plate is printed at full chroma with amber orange governing: "
            "the glass burns orange and gold, and the same orange lies as a "
            "reflected wash along the curved banister. Everything the light "
            "does not reach — the columns, the vault, the shadowed stone — goes "
            "to deep neutral near-black with a soft letterpress ink bleed at "
            "its edges. No second hue. One line of small serif type sits in the "
            "empty paper near the foot of the sheet, centred under the strip."
        ),
        text=["the light arrived coloured"],
        note=(
            "这张返工三次仍然是错的：我给出的是一扇「通用哥特窗」，而照片真正的主角是"
            "彩光打在石扶手上的那道反光。现在照片整个印出来，橙色是从玻璃洒到石头上的，不是填在窗格里的。"
        ),
    ),
    Plate(
        pid=55,
        photo="j04-round-pond.jpeg",
        place="London",
        fslug="serpentine",
        title="one red thing on the water",
        title_zh="水面上只有一处红",
        geometry="wide 16:6 letterbox band, mid sheet",
        treatment="neutral grey halftone, one region left in colour",
        typography="one line above the band, right-aligned",
        texture="newspaper halftone, coarse dot",
        mood="overcast afternoon",
        accent="tomato red",
        accent_hex="#E0342A",
        plate_para=(
            "One wide horizontal photographic plate is printed on the sheet, a "
            "letterbox band roughly 16 parts wide to 6 parts high, about 78% of "
            "the sheet width, centred left to right and crossing the sheet a "
            "little below the middle, with wide clean paper above and below. "
            "About 62% of the sheet is bare white paper."
        ),
        image_para=(
            "The plate reproduces the attached photograph in full: a wide view "
            "across a city park lake under flat overcast light. Along the "
            "bottom of the band, open water with fine wind ripples and a dozen "
            "ducks and geese swimming, each bird a distinct small shape. Across "
            "the middle, the paved far shore with a few walking figures. Behind "
            "them a dense line of full summer trees, and rising above the trees "
            "on the right, a tall gothic church spire against a pale hazy sky, "
            "with slimmer towers further left. Floating in the water near the "
            "centre, a single small red marker buoy. Keep the whole depth of "
            "the view — ripples, birds, people, treeline, spire, sky."
        ),
        print_para=(
            "The plate is printed as a coarse neutral grey newspaper halftone — "
            "water, birds, trees, spire and sky all in warm-neutral grey ink "
            "with a visible dot screen, no colour anywhere in them. The single "
            "exception is the marker buoy, which is printed in fully saturated "
            "tomato red at the same size it occupies in the photograph: small, "
            "but the only chromatic mark on the entire sheet, so the eye finds "
            "it immediately against all that grey. One line of small typewriter "
            "type sits in the empty paper above the band, right-aligned to the "
            "band's right edge; the slug sits on its own line beneath it."
        ),
        text=["one red thing on the water", "SEP 21  16:05  clear"],
        note=(
            "第一版删掉了整条天际线，只留几只灰鸭子和一个被我放大到荒谬的红圆盘。"
            "红点本来就该是小的——它之所以扎眼，是因为周围有一整片灰色的世界，而不是因为它大。"
        ),
    ),
    Plate(
        pid=56,
        photo="j05-cappadocia-balloons.jpeg",
        place="Cappadocia",
        fslug="cappadocia",
        title="everyone got up in the dark",
        title_zh="所有人都摸黑起床",
        geometry="landscape 3:2 plate, upper two thirds",
        treatment="full-chroma plate, dawn gradient",
        typography="one line low left in the empty third",
        texture="risograph grain in the sky",
        mood="slight surrealism",
        accent="violet into magenta",
        accent_hex="#7A46C6",
        plate_para=(
            "One landscape photographic plate is printed on the sheet, a 3:2 "
            "rectangle about 80% of the sheet width, centred left to right and "
            "sitting in the upper portion of the sheet with a clean paper "
            "margin above and to both sides, and a deep empty paper area "
            "filling the lower third. About 52% of the sheet is bare white "
            "paper."
        ),
        image_para=(
            "The plate reproduces the attached photograph in full: a high wide "
            "view over the Cappadocia valleys at dawn. The lower part of the "
            "plate is dark rugged terrain — eroded ridges and shadowed valleys, "
            "with several hot air balloons floating low among them, close "
            "enough to read their envelopes. Above and beyond, the sky is "
            "filled with dozens more balloons at every distance, scattered from "
            "large ones near the camera to specks near the horizon; the sheer "
            "number of them is the subject. On the far horizon a low "
            "snow-flecked mountain range. Keep the count high and the sizes "
            "varied so the depth of the sky is readable."
        ),
        print_para=(
            "The plate is printed at full chroma with violet governing: the sky "
            "runs from deep lavender-violet at the top down into saturated "
            "magenta near the horizon, one continuous cool gradient. The "
            "terrain is charcoal near-black. The lit balloon burners glow warm "
            "orange as small points — the subject's own second colour, kept "
            "small and not extended anywhere else. Visible risograph grain "
            "through the sky. One line of small sans type sits low in the empty "
            "paper beneath the plate, aligned to the plate's left edge; the "
            "second line sits under it."
        ),
        text=["everyone got up in the dark", "05:12  BEFORE SUNRISE"],
        note=(
            "第一版是一个紫色实心方块。这张照片的全部意义在于「多」——几十只球、"
            "从近到远各种大小，那个密度才是「所有人都摸黑起床」的理由。"
        ),
    ),
    Plate(
        pid=57,
        photo="j06-erciyes-road.jpeg",
        place="Erciyes",
        fslug="erciyes",
        title="the mountain stayed the same size",
        title_zh="那座山一直没有变大",
        geometry="4:5 plate, lower centre",
        treatment="two-ink riso duotone, cyan and black",
        typography="one line high in the empty upper area",
        texture="clean riso, slight plate offset",
        mood="quiet",
        accent="cyan blue",
        accent_hex="#1FA5D6",
        plate_para=(
            "One photographic plate is printed on the sheet, a 4:5 portrait "
            "rectangle about 70% of the sheet width, centred left to right and "
            "sitting low, with a clean paper margin below and to both sides, "
            "and a tall empty paper area above it. About 56% of the sheet is "
            "bare white paper."
        ),
        image_para=(
            "The plate reproduces the attached photograph in full: a two-lane "
            "asphalt road running straight away from the camera toward a huge "
            "snow-covered volcanic mountain. The road fills the bottom of the "
            "plate with its dashed white centre line receding in strong linear "
            "perspective. A row of pine trees and tall streetlights lines the "
            "left verge. In the middle distance, low village houses with "
            "pitched roofs and a slim flagpole. Filling the whole upper half of "
            "the plate, Mount Erciyes itself — broad, snow-covered, its "
            "crevices and ridges clearly modelled — under an open sky with a "
            "band of low cloud along its base. Keep the perspective of the road "
            "and the mass of the peak; the point of the picture is that the "
            "mountain is enormous and the road never gets closer to it."
        ),
        print_para=(
            "The plate is printed as a strict two-ink risograph duotone: one "
            "saturated cyan-blue ink and one black ink on the bare white paper, "
            "nothing else. Cyan carries the sky and the blue shadows in the "
            "snow; black carries the road, the pines and the buildings; the "
            "snow and the cloud are the unprinted white paper showing through. "
            "A slight offset between the two plates leaves a thin cyan fringe "
            "along one side of the dark shapes. No other hue appears. One line "
            "of small grey sans type sits high in the empty paper above the "
            "plate, aligned to the plate's left edge."
        ),
        text=["the mountain stayed the same size"],
        note=(
            "唯一一张用严格双色套印的：青 + 黑，雪是纸本身的白。"
            "照片里那块红色警示牌被这个印法丢掉了——这是印刷决定，不是失误。"
        ),
    ),
)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", type=int, nargs="*", help="only these plate ids")
    args = ap.parse_args()

    for plate in PLATES:
        if args.id and plate.pid not in args.id:
            continue
        print(f"===== {plate.pid}  {plate.place}  {plate.accent_hex}  {plate.title}")
        print(f"photo: {PHOTO_BASE}/{plate.photo}")
        print(build(plate))
        print()


if __name__ == "__main__":
    main()
