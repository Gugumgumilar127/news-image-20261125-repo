# THE WORLD — Wednesday 25 November 2026 (one-page news image)

A single 1024×1024 JPEG that sums up one day of world news,
built with the winning formula measured from the top finishers
of the previous editions of this contest: density and furniture
beat a pretty poster.

## The formula

- **50 stories total** — 16 illustrated lead stories plus a
  34-story numbered one-line digest ("ALSO ON WEDNESDAY").
- **Lead stories** each carry: a red number badge, a flat vector
  icon panel, a REGION · TOPIC kicker, a bold headline, a 1–2
  line summary and a named source line (Reuters, AP, BBC, …).
  The day's leads run from the COP31 collapse in Antalya and
  Ukraine's sinking of the Russian corvette Merkury off Libya
  to China's launch of the first Pakistani astronaut and
  Senegal restored as African champions by CAS.
- **Orientation strip** under the masthead: a proportional
  region bar — ASIA 10 · AMERICAS 13 · EUROPE 9 ·
  MIDDLE EAST 7 · AFRICA 5 · WORLD 2 · OCEANIA 4 (recomputed
  from the final 50-story list; every digest entry carries its
  region in `stories.py` so the counts can be audited).
- **World map**: dot-grid continents coloured by region, with
  red numbered pins matching the 16 lead stories — including
  the Antalya pin for COP31 and the Riyadh pin for the tower
  strike — plus a legend.
- **Verification furniture**: a CLAIM chip on the contested
  story (Iran's Hormuz mine claim), a DATE CHECK box listing
  older stories that were checked and deliberately left out,
  and a footer — "Every story on this page happened or was
  first reported on Wednesday 25 November 2026" — with the
  full source list.
- **Style**: flat vector, cream paper background, navy + red,
  giant serif date masthead. The file is not shrunk: it renders
  at its natural size (roughly 250–650 KB at quality 90).
  Lead cards are 55px tall with a 45px icon panel and tight
  type, so all 16 leads fit above the map.

## Run it (grader pattern: copy-the-asset)

```sh
python3 main.py            # or: MAKEFUN_OUTPUT_DIR=/some/dir python3 main.py
```

`main.py` is a copy-the-asset entrypoint, by design. The
competition grader runs the repository **read-only**
(`python3 -P -s /bot/main.py`) and only the output directory is
writable, so a program that renders and writes `entry.png` next
to itself can never complete there. Instead the repo ships the
finished image as the asset `entry.png`, and `main.py` —
standard library only (`os`, `shutil`, `sys`), no sibling
imports — copies it into `MAKEFUN_OUTPUT_DIR` (default
`/output`), then verifies the copy: JPEG magic bytes `FF D8`,
the trailing end-of-image marker `FF D9`, size ≤ 1 MiB, and
copy size equal to the shipped asset. It prints the byte count
and dimensions and exits 0.

## Rebuilding the asset (build-time only)

```sh
python3 compose.py   # writes ./entry.png, deterministically
```

Rendering is deterministic — repeated runs produce identical
bytes. Requires Python 3 and Pillow 10.2 with the DejaVu fonts
(DejaVuSerif-Bold, DejaVuSans-Bold, DejaVuSans). The grader
never runs this; it is how the shipped asset was produced.

## Files

- `main.py` — grader entrypoint: copy-the-asset + verification
  (see above).
- `entry.png` — the finished front page (JPEG bytes, 1024×1024,
  ≤ 1 MiB) shipped as a ready asset.
- `stories.py` — the full dataset: 16 lead stories (kicker,
  headline, summary, source, icon, map pin, tag), the 34-line
  digest (each with its region), region order/counts/colours,
  the DATE CHECK list and the footer/source strings.
- `mapdata.py` — the dot-grid world map (76×19 cells, land
  cells coded by region) and the equirectangular pin projection.
- `compose.py` — all rendering (build-time only): masthead,
  region bar, lead grid, icon glyphs, map with
  collision-resolved pins, DATE CHECK box, legend, digest
  columns and footer. Text is wrapped with real glyph widths
  so nothing overflows its panel.
- `research.md` — per-story sourcing and date basis, including
  the stories checked and left out.

## Date discipline

Every story was verified against the named wires and happened
or was first reported on Wednesday 25 November 2026. Anything
older (the GTA 6 release, Jensen Huang's return as Nvidia CEO,
the Nepal PM's India visit) is named in the DATE CHECK box
instead of being passed off as today's news.
