# 61 — First Fruits: Delaunay Harvest

**Theme:** Bikkurim / First Fruits  
**Technique:** Delaunay triangulation / weighted Poisson-disk sampling  
**Year:** 2026

## Description

A static SVG patchwork of ~700 Delaunay triangles covering a 700×700 canvas.
Seed points are generated with a weighted Poisson-disk sample: denser in the
lower two-thirds of the canvas (the fields of Israel) and sparser near the
top (sky and horizon).  Each triangle is colored according to which of the
seven species — wheat, barley, grapes, figs, pomegranates, olives, dates —
its centroid falls among, using a deterministic spatial hash.  Triangles in
the sky zone (upper 20%) are tinted blue; the path zone (bottom 8%) is
terracotta.

A row of seven Hebrew species glyphs runs along the bottom as a legend.  A
subtle `feTurbulence` overlay gives the surface a slight parchment texture.

The piece is fully static; the SVG is constructed once on page load by a
plain-JavaScript Bowyer-Watson implementation with no external libraries.

## Theological focus

Bikkurim (first fruits) required the farmer to mark the very first ripened
fruit with a straw before it was fully ripe — consecrating the threshold
moment of abundance before it became ordinary.  The Delaunay tessellation
shows the land not as a uniform backdrop but as a patchwork of seven distinct
promises, each one fulfilled.

## Sources

- Deuteronomy 8:8 (seven species)
- Deuteronomy 26:1–11 (the first-fruits declaration)
- Mishnah Bikkurim 3:1–4 (the Temple procession)

## Files

| File | Purpose |
|------|---------|
| `index.html` | Self-contained artwork + embedded essay |
| `essay.md` | Standalone essay (~430 words) |
| `thumbnail.svg` | 400×400 preview (92 triangles) |
| `tools/gen_thumbnail.py` | Python script that generated `thumbnail.svg` |
