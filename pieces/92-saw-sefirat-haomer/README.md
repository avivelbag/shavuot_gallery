# Forty-Nine Steps That Do Not Return

**Shavuot theme: Sefirat HaOmer / the 49-day count**

A self-avoiding walk (SAW) on a square lattice, animated one step per second over 49 steps. The walk models the Omer count: each of the 49 days is a distinct step that cannot be un-taken, each moving into territory not yet visited. Kabbalistic tradition maps the 49 days to the 49 combinations of the seven lower sefirot; the SAW's rule — no cell twice — is the geometric expression of that spiritual demand.

## Technique

Canvas 2D API. A backtracking depth-first search (DFS) pre-generates a guaranteed 49-step self-avoiding path before the animation begins, so the walk never gets trapped mid-count. The path is revealed step by step at 1-second intervals. Each segment is rendered with per-segment opacity (fading from 0.15 at the tail to 1.0 at the head) in wheat gold (#D4A017). The head is marked by a glowing white circle with a gold halo (shadow blur 20px). A Hebrew day counter in the top-right corner advances with each step. At step 49, the path flashes white, then the fiftieth day is proclaimed in the center before the walk resets.

## Sources

- Leviticus 23:15–16 — the commandment of Sefirat HaOmer
- Shulchan Aruch, Orach Chaim 489:8 — missing a day forfeits the blessing
- Zohar, Emor (III:97b); R. Chaim Vital, Sefer ha-Omer — 49 sefirot combinations
- Nienhuis (1982) — exact scaling exponent 3/4 for two-dimensional SAWs
