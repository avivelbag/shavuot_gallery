"""Generate thumbnail.png for piece 07-milk-honey-reaction-diffusion.

Runs the Gray-Scott reaction-diffusion simulation for 2000 steps to reach
steady-state worm/coral patterns, then maps the V field to a cream-to-amber
color ramp and saves a 256x256 PNG.

Usage:
    python gen_thumbnail.py
"""
import os
import numpy as np
from PIL import Image

SIM_W, SIM_H = 256, 256
Du, Dv = 0.16, 0.08
F, K = 0.055, 0.062
STEPS = 2000


def run_gray_scott() -> np.ndarray:
    """Run simulation and return V field (0..1) at steady state."""
    U = np.ones((SIM_H, SIM_W), dtype=np.float32)
    V = np.zeros((SIM_H, SIM_W), dtype=np.float32)

    seeds = [(SIM_H // 2, SIM_W // 2), (77, 77), (102, 179), (179, 102)]
    for cy, cx in seeds:
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                if dx * dx + dy * dy <= 36:
                    U[(cy + dy) % SIM_H, (cx + dx) % SIM_W] = 0.0
                    V[(cy + dy) % SIM_H, (cx + dx) % SIM_W] = 1.0

    for _ in range(STEPS):
        lapU = (np.roll(U, 1, 0) + np.roll(U, -1, 0) +
                np.roll(U, 1, 1) + np.roll(U, -1, 1) - 4 * U)
        lapV = (np.roll(V, 1, 0) + np.roll(V, -1, 0) +
                np.roll(V, 1, 1) + np.roll(V, -1, 1) - 4 * V)
        uvv = U * V * V
        U += Du * lapU - uvv + F * (1.0 - U)
        V += Dv * lapV + uvv - (F + K) * V
        np.clip(U, 0, 1, out=U)
        np.clip(V, 0, 1, out=V)

    return V


def v_to_rgb(V: np.ndarray) -> np.ndarray:
    """Map V field (0..1) to cream (#fdf6e3) → honey (#d4a017) → amber (#8b5a00)."""
    img = np.zeros((SIM_H, SIM_W, 3), dtype=np.float32)
    low = V < 0.5
    t_low = np.where(low, V * 2.0, 0.0)
    t_high = np.where(~low, (V - 0.5) * 2.0, 0.0)

    img[:, :, 0] = np.where(low, 253 + (212 - 253) * t_low,
                             212 + (139 - 212) * t_high)
    img[:, :, 1] = np.where(low, 246 + (160 - 246) * t_low,
                             160 + (90 - 160) * t_high)
    img[:, :, 2] = np.where(low, 227 + (23 - 227) * t_low,
                             23 * (1.0 - t_high))
    return np.clip(img, 0, 255).astype(np.uint8)


if __name__ == '__main__':
    V = run_gray_scott()
    pixels = v_to_rgb(V)
    img = Image.fromarray(pixels, 'RGB')
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail.png')
    img.save(out_path)
    print(f'Saved {out_path}')
