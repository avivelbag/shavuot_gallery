"""Generate thumbnail.png for piece 74-stable-fluid-milk-honey.

Runs a simplified 2-D Euler fluid advection on a 200x200 grid with cream
injected from the left and honey from the right, then maps the two-channel dye
field (R=cream, G=honey) to the piece colour palette and saves a 400x400 PNG.

Usage:
    python gen_thumbnail.py
"""
import os
import numpy as np
from PIL import Image

W, H = 200, 200
OUT_W, OUT_H = 400, 400
STEPS = 500
DT = 1.0 / 60.0
DYE_STRENGTH = 0.4
DYE_RADIUS = 12.0          # texels
VEL_STRENGTH = 60.0        # texels/sec
VEL_RADIUS = 8.0           # texels
DISS_DYE = 0.999
DISS_VEL = 0.9998


def gaussian(grid_w, grid_h, cx, cy, radius):
    """Return a 2-D Gaussian kernel centred at (cx, cy) in texel coordinates."""
    ys, xs = np.meshgrid(np.arange(grid_h), np.arange(grid_w), indexing='ij')
    d2 = (xs - cx) ** 2 + (ys - cy) ** 2
    return np.exp(-d2 / (radius * radius)).astype(np.float32)


def advect(field, vx, vy):
    """Semi-Lagrangian back-trace advection (nearest-neighbour, periodic wrap)."""
    ys, xs = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
    px = np.clip(np.round(xs - DT * vx).astype(int), 0, W - 1)
    py = np.clip(np.round(ys - DT * vy).astype(int), 0, H - 1)
    return field[py, px]


def run_sim():
    """Simulate cream-honey fluid injection and advection; return (cream, honey) arrays."""
    cream = np.zeros((H, W), dtype=np.float32)
    honey = np.zeros((H, W), dtype=np.float32)
    vx    = np.zeros((H, W), dtype=np.float32)
    vy    = np.zeros((H, W), dtype=np.float32)

    for step in range(STEPS):
        t = step * DT

        # Lissajous injection path
        liss_x = int(round((0.08 + 0.04 * np.sin(t * 0.3)) * W))
        liss_y = int(round((0.50 + 0.30 * np.sin(t * 0.6)) * H))
        liss_x = np.clip(liss_x, 0, W - 1)
        liss_y = np.clip(liss_y, 0, H - 1)

        mirror_x = W - 1 - liss_x
        mirror_y = H - 1 - liss_y

        # Direction alternates every 3 seconds
        direction = 1.0 if (int(t / 3.0) % 2 == 0) else -1.0

        g_vel_l = gaussian(W, H, liss_x,   liss_y,   VEL_RADIUS)
        g_vel_r = gaussian(W, H, mirror_x,  mirror_y, VEL_RADIUS)
        g_dye_l = gaussian(W, H, liss_x,   liss_y,   DYE_RADIUS)
        g_dye_r = gaussian(W, H, mirror_x,  mirror_y, DYE_RADIUS)

        vx += VEL_STRENGTH * direction * g_vel_l
        vx -= VEL_STRENGTH * direction * g_vel_r

        cream = np.clip(cream + DYE_STRENGTH * g_dye_l, 0.0, 1.0)
        honey = np.clip(honey + DYE_STRENGTH * g_dye_r, 0.0, 1.0)

        # Advect dye and velocity
        cream = DISS_DYE * advect(cream, vx, vy)
        honey = DISS_DYE * advect(honey, vx, vy)
        vx    = DISS_VEL * advect(vx, vx, vy)
        vy    = DISS_VEL * advect(vy, vx, vy)

    return cream, honey


def dye_to_rgb(cream, honey):
    """Map two-channel dye to cream/amber/honey palette (matches display shader)."""
    bg      = np.array([0.039, 0.031, 0.016], dtype=np.float32)
    cream_c = np.array([1.000, 0.961, 0.863], dtype=np.float32)
    mid_amb = np.array([0.941, 0.698, 0.235], dtype=np.float32)
    honey_c = np.array([0.831, 0.510, 0.039], dtype=np.float32)
    deep    = np.array([0.784, 0.416, 0.000], dtype=np.float32)

    total = cream + honey
    safe  = np.where(total > 1e-3, total, 1.0)
    t     = np.where(total > 1e-3, honey / safe, 0.0)

    mask_lo = t < 0.5
    t_lo    = np.clip(t * 2.0,         0.0, 1.0)
    t_hi    = np.clip((t - 0.5) * 2.0, 0.0, 1.0)
    extra   = np.clip(honey - 0.5, 0.0, 1.0)

    honey_deep = (1.0 - extra[:, :, None]) * honey_c + extra[:, :, None] * deep

    fluid_lo = (1.0 - t_lo[:, :, None]) * cream_c + t_lo[:, :, None] * mid_amb
    fluid_hi = (1.0 - t_hi[:, :, None]) * mid_amb  + t_hi[:, :, None] * honey_deep
    fluid    = np.where(mask_lo[:, :, None], fluid_lo, fluid_hi)

    alpha = np.clip(total * 3.0, 0.0, 1.0)[:, :, None]
    rgb   = (1.0 - alpha) * bg + alpha * fluid
    return np.clip(rgb * 255, 0, 255).astype(np.uint8)


if __name__ == '__main__':
    print('Running simulation …')
    cream, honey = run_sim()
    pixels = dye_to_rgb(cream, honey)
    img = Image.fromarray(pixels, 'RGB').resize((OUT_W, OUT_H), Image.NEAREST)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail.png')
    img.save(out)
    print(f'Saved {out}')
