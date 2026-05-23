"""Generate thumbnail.png for piece 74-heat-equation-engraved-freedom.

Runs 200 FTCS steps on a 200x150 grid seeded with a pixel mask for the
Hebrew letters חֵרוּת.  The mask is built using Pillow with the best
available Hebrew-capable font; if none is found, a hand-coded elliptical
fallback mask is used.  The resulting heat field is mapped through the
four-stop ember palette and saved as a 400x300 PNG (2x upscale).

Usage:
    python gen_thumbnail.py
"""
import os
import struct
import zlib

import numpy as np

# ---------------------------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------------------------

GW, GH = 200, 150
ALPHA = 0.24
STEPS = 200

# Palette stops: t in [0,1] → RGB
STOPS = [0.00, 0.15, 0.45, 0.75, 1.00]
COLORS = [
    (26, 20, 16),
    (61, 26, 8),
    (200, 74, 8),
    (232, 160, 32),
    (255, 240, 192),
]


# ---------------------------------------------------------------------------
# Letter mask construction
# ---------------------------------------------------------------------------

def _build_mask_pillow() -> np.ndarray | None:
    """Try to render חֵרוּת with Pillow and return a bool mask (GH x GW)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None

    # Font search order: Noto Hebrew (best), then generic system fallbacks
    font_candidates = [
        "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansHebrew-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ]
    font = None
    font_size = 72
    for path in font_candidates:
        if os.path.isfile(path):
            try:
                font = ImageFont.truetype(path, font_size)
                break
            except Exception:
                continue

    img = Image.new("L", (GW, GH), 0)
    draw = ImageDraw.Draw(img)

    text = "חֵרוּת"
    if font is not None:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (GW - tw) // 2 - bbox[0]
        y = (GH - th) // 2 - bbox[1]
        draw.text((x, y), text, fill=255, font=font)
    else:
        # No font available — use built-in default (may not render Hebrew)
        draw.text((GW // 2, GH // 2), text, fill=255, anchor="mm")

    arr = np.array(img, dtype=np.float32) / 255.0
    return arr > 0.5


def _build_mask_fallback() -> np.ndarray:
    """Hand-coded elliptical mask approximating letter positions."""
    mask = np.zeros((GH, GW), dtype=bool)
    cy, cx = GH // 2, GW // 2
    # Three oval blobs roughly where the three letter clusters sit
    for dx_frac, ry, rx in [(-0.30, 0.20, 0.08), (0.0, 0.20, 0.08), (0.28, 0.20, 0.08)]:
        dx = int(cx * dx_frac * 2)
        for y in range(GH):
            for x in range(GW):
                ny = (y - cy) / (GH * ry)
                nx = (x - (cx + dx)) / (GW * rx)
                if ny * ny + nx * nx <= 1.0:
                    mask[y, x] = True
    return mask


def build_mask() -> np.ndarray:
    m = _build_mask_pillow()
    if m is None or m.sum() == 0:
        m = _build_mask_fallback()
    return m


# ---------------------------------------------------------------------------
# FTCS heat solver
# ---------------------------------------------------------------------------

def run_ftcs(mask: np.ndarray) -> np.ndarray:
    """Run STEPS FTCS iterations and return the temperature field."""
    T = np.where(mask, 1.0, 0.0).astype(np.float32)
    for _ in range(STEPS):
        # Diffusion via roll-based Laplacian (periodic boundary, then zero border)
        lap = (np.roll(T, 1, 0) + np.roll(T, -1, 0) +
               np.roll(T, 1, 1) + np.roll(T, -1, 1) - 4.0 * T)
        T = T + ALPHA * lap
        # Zero-temperature boundary (Dirichlet)
        T[0, :] = 0.0
        T[-1, :] = 0.0
        T[:, 0] = 0.0
        T[:, -1] = 0.0
        # Enforce letter sources at 1.0
        T[mask] = 1.0
        np.clip(T, 0.0, 1.0, out=T)
    return T


# ---------------------------------------------------------------------------
# Color mapping
# ---------------------------------------------------------------------------

def temp_to_rgb(T: np.ndarray) -> np.ndarray:
    """Map temperature field (H x W) through the ember palette to uint8 RGB."""
    img = np.zeros((*T.shape, 3), dtype=np.float32)
    for s in range(len(STOPS) - 1):
        lo, hi = STOPS[s], STOPS[s + 1]
        ca, cb = np.array(COLORS[s], dtype=np.float32), np.array(COLORS[s + 1], dtype=np.float32)
        in_band = (T >= lo) & (T < hi)
        f = np.where(in_band, (T - lo) / (hi - lo), 0.0)[..., None]
        img += np.where(in_band[..., None], ca + (cb - ca) * f, 0.0)
    # Top stop
    top = T >= STOPS[-1]
    img[top] = np.array(COLORS[-1], dtype=np.float32)
    return np.clip(img, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------------------
# Minimal PNG encoder (avoids the need for an external library for output)
# ---------------------------------------------------------------------------

def _write_png(path: str, rgb: np.ndarray) -> None:
    """Write an H x W x 3 uint8 array as a PNG file."""
    try:
        from PIL import Image
        Image.fromarray(rgb, "RGB").save(path)
        return
    except ImportError:
        pass

    # Pure-Python fallback: build a minimal valid PNG
    H, W = rgb.shape[:2]

    def chunk(tag: bytes, data: bytes) -> bytes:
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))

    # Build raw image data with filter byte 0 per row
    raw = b""
    for row in rgb:
        raw += b"\x00" + row.tobytes()
    idat = chunk(b"IDAT", zlib.compress(raw, 9))
    iend = chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(sig + ihdr + idat + iend)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    mask = build_mask()
    T = run_ftcs(mask)

    # Upscale 2x to produce a 400x300 thumbnail
    T_up = np.repeat(np.repeat(T, 2, axis=0), 2, axis=1)
    rgb = temp_to_rgb(T_up)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail.png")
    _write_png(out_path, rgb)
    print(f"Saved {out_path}  ({rgb.shape[1]}x{rgb.shape[0]} px)")


if __name__ == "__main__":
    main()
