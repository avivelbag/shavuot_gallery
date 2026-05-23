# The Cloud That Would Not Lift

**Shavuot theme:** Har Sinai — the cloud of glory that descended on Sinai (Exodus 19:16–19, 24:15–18)

A full-viewport WebGL fragment shader computing thin-film interference in real time. A noise-driven thickness field slowly undulates across the canvas; at each pixel, a physically accurate interference formula evaluates eight wavelength samples spanning the visible spectrum and converts the result to sRGB via the CIE 1931 observer functions. The output is iridescence in perpetual motion: not a rainbow gradient but a drifting, organic spectrum produced by wave physics.

## Technique

| Step | Detail |
|------|--------|
| Film thickness field | Two octaves of `sin(x·f + t)·cos(y·f·1.3 + t·0.7)`; f₁ = 0.004, f₂ = 0.009; amplitude ratio 1 : 0.5; vertical gradient adds 0–80 nm top-to-bottom |
| Thickness range | ~200–880 nm (shifts entire visible spectrum) |
| Interference formula | I(λ) = cos²(π · 2 · n · d / λ), n = 1.45 (water/soap refractive index) |
| Spectral sampling | 8 wavelengths: 380, 426, 472, 518, 564, 610, 656, 702 nm |
| Color space | 8-sample intensities weighted by CIE 1931 2° observer (x̄, ȳ, z̄); XYZ converted to linear sRGB with D65 white point matrix; sqrt gamma compression |
| Vignette | Dark oval border via `smoothstep(0.33, 0.65, length(uv − 0.5))` |
| Loop | `requestAnimationFrame`; time uniform advances at 0.3× wall-clock seconds |

## Palette

| Appearance | Cause |
|------------|-------|
| Violet / deep blue | Thin film (~200–350 nm); constructive interference peaks in short wavelengths |
| Cyan / teal | Mid-thin film (~350–450 nm) |
| Green | Mid film (~450–550 nm) |
| Gold / yellow | Film ~500–600 nm; peak in 560–580 nm band |
| Orange / red | Thicker film (~600–750 nm); long-wavelength constructive peak |
| Broad white shimmer | Where multiple wavelengths constructively interfere simultaneously |
