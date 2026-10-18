"""Bangun ulang aset web dari Logo.png dan folder Porto/.

Jalankan dari folder Web MAKA:
    python tools/build_assets.py

Output:
    assets/brand/  -> mark-cream.png, mark-ink.png (transparan), favicon.png, og.jpg
    assets/photo/  -> pNN-s.webp (720px), pNN-m.webp (1280px), pNN-l.webp (2000px)
    assets/photo/manifest.json -> urutan + rasio (disalin ke PHOTOS di index.html)
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Porto"
OUT_BRAND = ROOT / "assets" / "brand"
OUT_PHOTO = ROOT / "assets" / "photo"

CREAM = (239, 235, 228)
INK = (24, 23, 21)

# Semua foto di Porto ditampilkan (permintaan 10 Okt 2026).
SKIP = set()

# Urutan kurasi. 21 pertama = bola foto di hero; sisanya ikut di arsip.
ORDER = [
    "DSC04938.jpg", "Copy of DSC08973.jpg", "DSC09497.jpg", "DSC05059.jpg",
    "Copy of DSC08901.jpg", "DSC04804.jpg", "karya-04-full.webp", "DSC05001.jpg",
    "DSC09330.jpg", "Copy of DSC09004.jpg", "DSC09285.jpg", "DSC04959.jpg",
    "karya-01-full.webp", "Copy of DSC09034.jpg", "DSC09492.jpg", "DSC09238.jpg",
    "DSC05012.jpg", "DSC09484.jpg", "Copy of DSC09104.jpg", "DSC09400.jpg",
    "DSC09151.jpg",
    # arsip + section
    "DSC04827.jpg", "Copy of DSC08943.jpg", "DSC09180.jpg", "DSC09604.jpg",
    "karya-02-full.webp", "DSC09323.jpg", "Copy of DSC09013.jpg", "Copy of DSC09021.jpg",
    "Copy of DSC09053.jpg", "Copy of DSC09060.jpg", "DSC09398.jpg", "karya-06-full.webp",
    # tambahan Okt 2026
    "DSC09536.jpg", "WhatsApp Image 2026-09-26 at 20.27.56.jpeg", "WhatsApp Image 2026-09-26 at 20.27.55.jpeg",
    "DSC09348.jpg", "karya-05-full.webp",
    # tambahan 18 Okt 2026
    "DSC09169.jpg", "DSC09188.jpg", "DSC09228.jpg", "DSC09246.jpg",
    "DSC09307.jpg", "DSC09337.JPG", "DSC09359.jpg", "DSC09465.jpg",
]


def build_brand():
    OUT_BRAND.mkdir(parents=True, exist_ok=True)
    logo = Image.open(ROOT / "Logo.png").convert("RGB")
    arr = np.asarray(logo).astype(int)
    bg = np.median(arr.reshape(-1, 3), axis=0)
    ink = np.abs(arr - bg).sum(2)
    ys, xs = np.where(ink > 90)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    alpha = np.clip((ink - 30) * 255 / 200, 0, 255).astype(np.uint8)
    for name, color in (("mark-cream", CREAM), ("mark-ink", INK)):
        layer = Image.new("RGBA", logo.size, color + (0,))
        layer.putalpha(Image.fromarray(alpha))
        layer = layer.crop((x0 - 3, y0 - 3, x1 + 4, y1 + 4))
        layer.thumbnail((480, 480), Image.LANCZOS)
        layer.save(OUT_BRAND / f"{name}.png", optimize=True)
    # favicon: mark krem di kotak gelap
    mark = Image.open(OUT_BRAND / "mark-cream.png")
    fav = Image.new("RGBA", (256, 256), INK + (255,))
    m = mark.copy(); m.thumbnail((150, 150), Image.LANCZOS)
    fav.alpha_composite(m, ((256 - m.width) // 2, (256 - m.height) // 2))
    fav.save(OUT_BRAND / "favicon.png", optimize=True)
    print("brand ok", (x1 - x0, y1 - y0))


def build_photos():
    OUT_PHOTO.mkdir(parents=True, exist_ok=True)
    names = {p.name for p in SRC.iterdir()} - SKIP
    missing = [n for n in ORDER if n not in names]
    assert not missing, missing
    extra = names - set(ORDER)
    assert not extra, f"Foto baru belum masuk ORDER: {sorted(extra)}"
    manifest = []
    for i, name in enumerate(ORDER, 1):
        im = ImageOps.exif_transpose(Image.open(SRC / name)).convert("RGB")
        key = f"p{i:02d}"
        if all((OUT_PHOTO / f"{key}-{x}.webp").exists() for x in "sml") and i != 6:
            manifest.append([key, round(im.width / im.height, 3)])
            continue
        for suffix, box, q in (("s", 720, 78), ("m", 1280, 80), ("l", 2000, 82)):
            c = im.copy(); c.thumbnail((box, box), Image.LANCZOS)
            c.save(OUT_PHOTO / f"{key}-{suffix}.webp", quality=q, method=6)
        manifest.append([key, round(im.width / im.height, 3)])
        if i == 6:
            og = im.copy(); og = ImageOps.fit(og, (1200, 630), Image.LANCZOS)
            og.save(OUT_BRAND / "og.jpg", quality=82)
        print(key, name, im.size)
    (OUT_PHOTO / "manifest.json").write_text(json.dumps(manifest))
    print(json.dumps(manifest))


if __name__ == "__main__":
    build_brand()
    build_photos()
