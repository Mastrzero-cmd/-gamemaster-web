"""Posterize the Image Gen art sources into the exact GameMaster palette.

Sources live in `art-src/` (raw generations, git-ignored and never served;
only the optimized output is versioned). Output goes to
`public/art/cromo/` as lossless WebP so every pixel is exactly blue, black or
red: no intermediate tones, no purple blends, no anti-aliased fringes.

The hero hardware and the AI chip are also split into two planes for parallax:
- `*-front.webp`: the red objects with their own black details (transparent elsewhere);
- `*-rear.webp`: everything else, with the red area continued as the surface it sits on.
Both planes come from the same single drawing, so nothing is duplicated.

Requires: python3, Pillow, numpy.
Usage: python3 scripts/build-art-layers.py
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "art-src"
OUT = ROOT / "public" / "art" / "cromo"

BLUE = (36, 56, 255)
BLACK = (5, 5, 6)
RED = (255, 42, 31)

# Nearest-neighbour 2x keeps every pixel in palette while letting browsers
# downscale smoothly on standard screens and stay crisp on retina screens.
UPSCALE = 2


def classify(image: Image.Image, allow_red: bool, denoise: bool = True, blue_floor: int = 120) -> np.ndarray:
    """Return a label map: 0 = black, 1 = blue, 2 = red.

    Fields are drawn with 1px hairlines, so they skip the median filter and use a
    higher blue floor: anything darker than clean background blue becomes ink.
    """
    source = image.filter(ImageFilter.MedianFilter(3)) if denoise else image
    rgb = np.asarray(source.convert("RGB")).astype(np.int16)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    labels = np.zeros(r.shape, dtype=np.uint8)
    labels[(b > blue_floor) & (b > r + 40)] = 1
    if allow_red:
        labels[(r > 130) & (r > b + 40) & (r > g + 60)] = 2
    return labels


def paint(labels: np.ndarray) -> np.ndarray:
    out = np.zeros(labels.shape + (3,), dtype=np.uint8)
    out[labels == 0] = BLACK
    out[labels == 1] = BLUE
    out[labels == 2] = RED
    return out


def morph(mask: np.ndarray, size: int, grow: bool) -> np.ndarray:
    img = Image.fromarray((mask * 255).astype(np.uint8))
    img = img.filter(ImageFilter.MaxFilter(size) if grow else ImageFilter.MinFilter(size))
    return np.asarray(img) > 127


def fill_holes(mask: np.ndarray) -> np.ndarray:
    """Close interior gaps by flood-filling the background from the borders."""
    outside = np.zeros_like(mask)
    outside[0, :] = ~mask[0, :]
    outside[-1, :] = ~mask[-1, :]
    outside[:, 0] = ~mask[:, 0]
    outside[:, -1] = ~mask[:, -1]
    while True:
        grown = outside.copy()
        grown[1:, :] |= outside[:-1, :]
        grown[:-1, :] |= outside[1:, :]
        grown[:, 1:] |= outside[:, :-1]
        grown[:, :-1] |= outside[:, 1:]
        grown &= ~mask
        if np.array_equal(grown, outside):
            return ~outside
        outside = grown


def save(array: np.ndarray, name: str, scale: int = 1) -> None:
    mode = "RGBA" if array.shape[-1] == 4 else "RGB"
    img = Image.fromarray(array, mode)
    if scale > 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    path = OUT / f"{name}.webp"
    img.save(path, "WEBP", lossless=True, quality=100, method=6)
    print(f"{path.relative_to(ROOT)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")


def build_field(source: str, name: str) -> None:
    labels = classify(Image.open(SRC / source), allow_red=False, denoise=False, blue_floor=175)
    save(paint(labels), name, scale=UPSCALE)


def build_panel(source: str, name: str) -> None:
    labels = classify(Image.open(SRC / source), allow_red=True)
    save(paint(labels), name, scale=UPSCALE)


def build_split_panel(source: str, name: str, rear_fill: int = 1, shadow_reach: int = 21, thick: int = 15, open_field: bool = False) -> None:
    labels = classify(Image.open(SRC / source), allow_red=True)
    red = labels == 2
    figure = fill_holes(morph(morph(red, 9, grow=True), 9, grow=False)) | red
    # The black outline belongs to the front object; otherwise the rear keeps a
    # black silhouette of the same contour that peeks out when the planes move.
    black = labels == 0
    thick_black = morph(morph(black, thick, grow=False), thick, grow=True)
    figure = morph(figure, 7, grow=True) | (morph(figure, shadow_reach, grow=True) & black & ~thick_black)


    front = np.zeros(labels.shape + (4,), dtype=np.uint8)
    front[..., :3] = paint(labels)
    front[..., 3] = np.where(figure, 255, 0)
    save(front, f"{name}-front", scale=UPSCALE)

    # `rear_fill` is the label the red objects sit on: open blue field (1) or a black body (0).
    rear_labels = np.where(figure, rear_fill, labels).astype(np.uint8)
    if open_field:
        # Blue reachable from the border is the open field: make it transparent so the
        # page field shows through. Blue enclosed by black (screens) stays opaque.
        outside = ~fill_holes(rear_labels != 1)
        rear = np.zeros(labels.shape + (4,), dtype=np.uint8)
        rear[..., :3] = paint(rear_labels)
        rear[..., 3] = np.where(outside, 0, 255)
        save(rear, f"{name}-rear", scale=UPSCALE)
    else:
        save(paint(rear_labels), f"{name}-rear", scale=UPSCALE)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    build_field("gm-raw-field-gaming-desktop.jpg", "field-gaming-desktop")
    build_field("gm-raw-field-gaming-mobile.jpg", "field-gaming-mobile")
    build_field("gm-raw-field-floor-desktop.jpg", "field-floor-desktop")
    build_split_panel("gm-raw-hero-consoles.jpg", "panel-consoles", shadow_reach=45, thick=27, open_field=True)
    build_split_panel("gm-raw-ia-chip.jpg", "panel-chip", rear_fill=0)


if __name__ == "__main__":
    main()
