"""Generate thumbnail.png for piece 75-mandelbrot-infinite-torah.

Renders a 400x400 view of the Mandelbrot set in pure Python (no numpy, no
Pillow) at 64 iterations max, using the same Shavuot palette as the WebGL
piece: indigo #1A0A40 → royal blue #1A3080 → sapphire #1060C0 → gold
#C8A020 → amber #D4720A → cream #F0E8D0.  The interior is rendered as
near-black #050508.  Output is a valid PNG written via stdlib zlib + struct.

Usage:
    python gen_thumbnail.py
"""
import math
import os
import struct
import zlib

WIDTH = 400
HEIGHT = 400
MAX_ITER = 64

# Standard Mandelbrot viewport
X_MIN, X_MAX = -2.5, 1.0
Y_MIN, Y_MAX = -1.25, 1.25

# Six palette stops matching the WebGL shader (RGB floats 0-1)
_STOPS = [
    (0x1A / 255.0, 0x0A / 255.0, 0x40 / 255.0),  # indigo #1A0A40
    (0x1A / 255.0, 0x30 / 255.0, 0x80 / 255.0),  # royal blue #1A3080
    (0x10 / 255.0, 0x60 / 255.0, 0xC0 / 255.0),  # sapphire #1060C0
    (0xC8 / 255.0, 0xA0 / 255.0, 0x20 / 255.0),  # gold #C8A020
    (0xD4 / 255.0, 0x72 / 255.0, 0x0A / 255.0),  # amber #D4720A
    (0xF0 / 255.0, 0xE8 / 255.0, 0xD0 / 255.0),  # cream #F0E8D0
]


def _mandelbrot(cr, ci):
    """Return smooth escape value for c = cr + ci*i, or None if inside the set."""
    zr, zi = 0.0, 0.0
    for i in range(MAX_ITER):
        zr2 = zr * zr
        zi2 = zi * zi
        if zr2 + zi2 > 4.0:
            # Smooth coloring: removes integer-step banding at escape boundary.
            # Formula: iter - log2(log2(|z|^2)) + 4  (Iñigo Quilez / standard technique)
            log_zmod = math.log(zr2 + zi2) / 2.0  # log(|z|) = log(|z|^2)/2
            smooth = i - math.log(log_zmod / math.log(2.0)) / math.log(2.0) + 4.0
            return smooth
        zi = 2.0 * zr * zi + ci
        zr = zr2 - zi2 + cr
    return None


def _palette(t):
    """Map t in [0,1) to an RGB byte triple via piecewise-linear interpolation."""
    t = t % 1.0
    n = len(_STOPS)
    s = t * n
    i = int(s) % n
    f = s - int(s)
    r0, g0, b0 = _STOPS[i]
    r1, g1, b1 = _STOPS[(i + 1) % n]
    return (
        max(0, min(255, int((r0 + (r1 - r0) * f) * 255 + 0.5))),
        max(0, min(255, int((g0 + (g1 - g0) * f) * 255 + 0.5))),
        max(0, min(255, int((b0 + (b1 - b0) * f) * 255 + 0.5))),
    )


def _render():
    """Return flat list of (r, g, b) pixel tuples in row-major order."""
    pixels = []
    for row in range(HEIGHT):
        for col in range(WIDTH):
            cr = X_MIN + (col + 0.5) / WIDTH * (X_MAX - X_MIN)
            ci = Y_MAX - (row + 0.5) / HEIGHT * (Y_MAX - Y_MIN)
            smooth = _mandelbrot(cr, ci)
            if smooth is None:
                pixels.append((5, 5, 8))  # interior: #050508
            else:
                pixels.append(_palette((smooth % 32) / 32.0))
    return pixels


def _write_png(path, pixels, width, height):
    """Write an RGB PNG file using only Python stdlib (zlib + struct)."""

    def _chunk(tag, data):
        """Return a PNG chunk: length + tag + data + CRC32."""
        payload = tag + data
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + payload + struct.pack('>I', crc)

    # IHDR: width(4) height(4) bit_depth(1) color_type(1=RGB=2) compress(1) filter(1) interlace(1)
    ihdr = _chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))

    # Raw scanlines: each row preceded by a filter byte 0 (no filter)
    raw = bytearray()
    for row in range(height):
        raw.append(0)  # filter type: None
        for col in range(width):
            r, g, b = pixels[row * width + col]
            raw.extend([r, g, b])

    idat = _chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    iend = _chunk(b'IEND', b'')

    with open(path, 'wb') as fh:
        fh.write(b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend)


if __name__ == '__main__':
    pixels = _render()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail.png')
    _write_png(out, pixels, WIDTH, HEIGHT)
    print(f'Saved {out}')
