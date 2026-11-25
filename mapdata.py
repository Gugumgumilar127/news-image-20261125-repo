# mapdata.py - coarse dot-grid world map for the news page.
# Each character is one grid cell. ' ' is ocean; a letter is land
# coloured by the region that owns that cell:
#   N = AMERICAS  E = EUROPE   M = MIDDLE EAST
#   F = AFRICA    A = ASIA    O = OCEANIA
# The grid is 76 x 19 cells on an equirectangular projection
# (longitude -180..180 left to right, latitude 90
# ..-90 top to
# bottom). It is deliberately coarse: continents sit in the right
# places and stay recognisable at poster size.
# Pins are not stored here: compose.py projects each lead story's
# (lon, lat) from stories.py through pin_xy(). This edition carries
# 16 pins for the lead stories of Sunday 22 November 2026.

GRID_W = 76
GRID_H = 19

MAP_ROWS = [
    "      NNNNNNNNNNNNNNN         NNNNNN          AAAAAAAAAAAAAAAAAAAAAAAAAAAA  ",
    "  NNNNNN  NNNNNNNNNNNNNNN NNNNNNN         AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    " NNNNNNNNNNNNNNNNNNNNNNNNNNN NNNN  EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "   NNNN  NNNNNNNNNNNNNNNNN          EEEEEEEEEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "     NNNNNNNNNNNNNNNNNNNNN        EEEEEEEEEEEEAAAAAAAAAAAAAAAAAAAAAAAAAAAA  ",
    "     NNNNNNNNNNNNNNNNNNN            EEEEEEMMMAAAAAAAAAAAAAAAAAAAAAAAA AA AA ",
    "       NNNNNNNNNNNNNNNNN          FFFFFFFFFFFFMMMMMAAAAAAAAAAAAAAA          ",
    "           NNNNNNNNNNNNN          FFFFFFFFFFFFFFMMMMMAAAAAAAAA              ",
    "          NNNNNNN      NNNNNN          FFFFFFFFFFFFFFFF        AAAAAAAAAA   ",
    "                 NNNNNNNNN       FFFFFFFFFFFFFFFFF     AAAAAAAAAAAAAAAA     ",
    "                NNNNNNNNNNNN        FFFFFFFFFFFFF       AAAOOOOOOOOOOOOOOOO ",
    "                    NNNNNNN             FFFFFFF           OOOOOOOOOOOOOO    ",
    "                      NNNNN               FFFFF           OOOOOOOOOOOOOO    ",
    "                            NNNN                 FFFF                    OO ",
    " " * 76,
    " " * 76,
    " " * 76,
    " " * 76,
    " " * 76,
]

REGION_OF_CHAR = {"N": "AMERICAS", "E": "EUROPE", "M": "MIDDLE EAST",
                 "F": "AFRICA", "A": "ASIA", "O": "OCEANIA"}

for _row in MAP_ROWS:
    assert len(_row) == GRID_W, "map row must be %d cells" % GRID_W
assert len(MAP_ROWS) == GRID_H

def pin_xy(lon, lat, x0, y0, w, h):
    """Equirectangular projection of (lon, lat) into a pixel box."""
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (90.0 - lat) / 180.0 * h
    return (x, y)


def cell_xy(col, row, x0, y0, w, h):
    """Pixel centre of grid cell (col, row) inside a pixel box."""
    cw = w / GRID_W
    ch = h / GRID_H
    return (x0 + (col + 0.5) * cw, y0 + (row + 0.5) * ch)
