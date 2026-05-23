# The Night Turns on Its Axis — Aizawa Attractor

Five trajectories orbit a three-dimensional strange attractor, projected onto 2D
with a slowly rotating viewpoint, rendered as fading star trails colored from
midnight blue at the bottom of the torus to pale gold at the top — night turning
toward dawn.

**Theme:** Tikkun Leil Shavuot — the all-night Torah vigil on the eve of Shavuot,
practiced to repair the legend that Israel overslept before the revelation at Sinai.
The toroidal orbit of the Aizawa attractor mirrors the structured spiral of the
Tikkun: Tanach, Mishnah, Talmud, Kabbalah — each pass through the same material
at a different depth, never exactly retracing.

## Technique

The **Aizawa attractor** is integrated with **Runge-Kutta 4** at dt=0.01. Each
animation frame advances 5 trajectories by 50 integration steps and plots each
intermediate point as a 1px dot with `globalCompositeOperation = 'lighter'` at
8% opacity, so dense regions bloom bright.

**Parameters:** a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1

**System equations:**
- dx/dt = (z − b)·x − d·y
- dy/dt = d·x + (z − b)·y
- dz/dt = c + a·z − z³/3 − (x²+y²)(1+e·z) + f·z·x³

**Projection:** xz-plane with slow azimuthal rotation. θ += 0.0003 rad/frame
gives one full revolution every ~2 minutes at 60fps. Scale = H/5.

**Fading trails:** Each frame begins with `rgba(5, 5, 16, 0.025)` overlay, decaying
old points over ~40 frames for smooth star-trail persistence.

**Color:** z coordinate mapped linearly from z_min = −1.5 (midnight blue #0a0a2e)
through deep violet (#2d0a5c), cobalt (#1a1a8c), silver-blue (#8899cc), to
z_max = 2.0 (pale gold #f0e8b0).

**Hebrew overlays:** "תִּקּוּן לֵיל שָׁבוּעוֹת" fixed at canvas bottom; "שַׁחֲרִית"
fades in smoothly when any trajectory rises above z = 1.5 (the dawn region).

**Background:** #050510 (deep indigo-black). No external dependencies.
Animation via `requestAnimationFrame`.

**Theme:** Tikkun Leil Shavuot — Night Vigil and Dawn  
**Technique:** Aizawa strange attractor (RK4, 3D projection, fading trails)
