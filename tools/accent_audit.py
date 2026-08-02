#!/usr/bin/env python3
"""Measure the saturated chromatic anchor on every sheet, against the skill's rule.

The Standard Color Engine asks for "roughly 0.8%-2.5% of the whole canvas or
15%-35% of the small visual cluster", and for the anchor to "remain visible when
the image is viewed as a thumbnail". Eyeballing that is exactly the kind of
judgement that drifts across 45 sheets, so it is measured instead.

Method: convert to CIELAB, take chroma C = hypot(a, b) and hue h = atan2(b, a),
and count the pixels that are both chromatic enough and close in hue to the
accent recorded in index.json. The hue gate is what separates a real anchor from
warm paper — paper carries a low but nonzero chroma everywhere, so a chroma-only
threshold quietly counts the whole sheet.

Cluster share is reported too, using the anchor's own connected components: the
"small visual cluster" is the photo/cutout the anchor sits in, so it is estimated
as the convex bounding region of the ink and mid-dark image content around the
anchor. It is an estimate and labelled as one; the canvas figure is the one the
gate uses.

Usage:
    python3 tools/accent_audit.py                # audit all 45
    python3 tools/accent_audit.py --id 6 10      # just these
    python3 tools/accent_audit.py --thumb        # also check thumbnail survival
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.color import rgb2lab

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "posters" / "index.json"

FLOOR, CEIL = 0.008, 0.025        # the skill's canvas band
HUE_TOL = 30.0                    # degrees
CHROMA_FLOOR = 18.0               # below this, it is paper warmth, not ink
CHROMA_FRAC = 0.45                # or 45% of the accent's own chroma
THUMB_W = 64                      # "viewed as a thumbnail"


def lab_of_hex(h):
    h = h.lstrip("#")
    rgb = np.array([[[int(h[i:i + 2], 16) for i in (0, 2, 4)]]], dtype=np.uint8)
    return rgb2lab(rgb / 255.0)[0, 0]


def anchor_mask(lab, target):
    """Pixels that read as the accent ink: chromatic enough, and the right hue."""
    a, b = lab[..., 1], lab[..., 2]
    chroma = np.hypot(a, b)
    hue = np.degrees(np.arctan2(b, a))

    c0 = math.hypot(target[1], target[2])
    h0 = math.degrees(math.atan2(target[2], target[1]))
    gate = max(CHROMA_FLOOR, CHROMA_FRAC * c0)

    d = np.abs((hue - h0 + 180.0) % 360.0 - 180.0)
    return (chroma >= gate) & (d <= HUE_TOL), chroma


def cluster_share(mask, lab):
    """Rough share of the anchor inside the visual cluster it belongs to.

    The cluster is taken as the printed content near the anchor: anything
    meaningfully darker than the paper, dilated enough to close halftone gaps,
    then restricted to the component that actually contains the anchor.
    """
    if not mask.any():
        return None
    content = lab[..., 0] < 82.0                       # darker than bare paper
    joined = ndimage.binary_dilation(content | mask, iterations=6)
    lbl, n = ndimage.label(joined)
    if n == 0:
        return None
    # the component holding the most anchor pixels
    ids, counts = np.unique(lbl[mask], return_counts=True)
    keep = ids[np.argmax(counts)]
    if keep == 0:
        return None
    comp = lbl == keep
    area = int(comp.sum())
    # numerator must be the anchor *inside* this component, not the whole sheet's
    # anchor: an anchor split across components otherwise reports over 100%.
    return int((mask & comp).sum()) / area if area else None


def audit(path, accent_hex, want_thumb=False):
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im, dtype=np.float64) / 255.0
    lab = rgb2lab(arr)
    target = lab_of_hex(accent_hex)

    mask, _ = anchor_mask(lab, target)
    canvas = mask.sum() / mask.size
    clus = cluster_share(mask, lab)

    out = {"size": im.size, "canvas": canvas, "cluster": clus}

    if want_thumb:
        w = THUMB_W
        t = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
        tlab = rgb2lab(np.asarray(t, dtype=np.float64) / 255.0)
        tmask, _ = anchor_mask(tlab, target)
        out["thumb_px"] = int(tmask.sum())
    return out


def verdict(canvas, cluster):
    if FLOOR <= canvas <= CEIL:
        return "PASS canvas"
    if cluster is not None and 0.15 <= cluster <= 0.35:
        return "PASS cluster"
    return "LOW " if canvas < FLOOR else "HIGH"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", nargs="*", type=int)
    ap.add_argument("--thumb", action="store_true")
    args = ap.parse_args()

    data = json.loads(INDEX.read_text(encoding="utf-8"))
    posters = data["posters"]
    if args.id:
        posters = [p for p in posters if p["id"] in args.id]

    print(f"{'id':>3}  {'canvas%':>8} {'cluster%':>9}  {'thumb':>5}  verdict   accent")
    bad = []
    for p in posters:
        r = audit(ROOT / "posters" / p["file"], p["accent_hex"], args.thumb)
        v = verdict(r["canvas"], r["cluster"])
        cl = f"{r['cluster'] * 100:8.1f}" if r["cluster"] is not None else "       -"
        th = f"{r.get('thumb_px', ''):>5}"
        print(f"{p['id']:>3}  {r['canvas'] * 100:8.3f} {cl}   {th}  {v:9} {p['recipe']['accent']}")
        if v.startswith(("LOW", "HIGH")):
            bad.append((p["id"], r["canvas"], r["cluster"]))

    print(f"\noutside the band: {len(bad)}")
    for i, c, cl in bad:
        print(f"  no.{i:02d}  canvas {c * 100:.3f}%  cluster {'-' if cl is None else f'{cl * 100:.1f}%'}")


if __name__ == "__main__":
    main()
