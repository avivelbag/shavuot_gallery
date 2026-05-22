# The Fifty Gates — Bayer-Dithered Omer Calendar

**Piece 32** | 2026

**Technique:** canvas 2D — Bayer 4×4 ordered dithering, ImageData pixel manipulation, sequential cell animation

**Theme:** Sefirat HaOmer — the fifty gates of Binah / Counting toward Shavuot

A 7×7 grid of 49 cells, one per day of the Omer count. Each cell is filled using Bayer 4×4 ordered dithering at a luminance proportional to its day number: day 1 shows a single lit pixel per 4×4 block; day 49 shows nearly complete gold coverage. Cells materialize left-to-right column by column over 250ms each, lighting up in sequence over ~12 seconds. After all 49 days complete, a larger 50th panel blooms in solid gold bearing the Hebrew letter נ (nun = 50), representing the fiftieth gate of Binah that Moses could not attain — the threshold of divine understanding that defines Shavuot.

The Bayer matrix encodes the theology: each pixel is a binary threshold-crossing, each day a gate either opened or not. Forty-nine thresholds yield to the count. The fiftieth opens itself.
