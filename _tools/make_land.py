#!/usr/bin/env python3
"""Turns PetroGram's own world map (world.bin) into dots for the website:
assets/land.js (points on a globe) and _tools/flat_map.json (a flat dot map)."""
import json, math, struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIN = Path('/Users/fardinvatani/Developer/petrogram/assets/map/world.bin')

b = BIN.read_bytes()
assert b[:4] == b'PGWM' and b[4] == 1
o = 5
(count,) = struct.unpack_from('<H', b, o); o += 2
rings = []
for _ in range(count):
    o += 2 + 4
    (rc,) = struct.unpack_from('<H', b, o); o += 2
    for _ in range(rc):
        (n,) = struct.unpack_from('<H', b, o); o += 2
        pts = struct.unpack_from('<%dh' % (n * 2), b, o); o += n * 4
        xs = [p / 100 for p in pts[0::2]]; ys = [p / 100 for p in pts[1::2]]
        rings.append((min(xs), max(xs), min(ys), max(ys), xs, ys))


def land(lon, lat):
    if lat <= -71:          # Antarctica is not in the app's map: a simple cap
        return True
    for x0, x1, y0, y1, xs, ys in rings:
        if lon < x0 or lon > x1 or lat < y0 or lat > y1:
            continue
        inside = False
        j = len(xs) - 1
        for i in range(len(xs)):
            if (ys[i] > lat) != (ys[j] > lat) and \
               lon < (xs[j] - xs[i]) * (lat - ys[i]) / (ys[j] - ys[i]) + xs[i]:
                inside = not inside
            j = i
        if inside:
            return True
    return False


# Globe: rows of latitude, evenly spaced along each row.
STEP = 2.15
globe = []
lat = -88.0
while lat <= 88:
    n = max(1, round(360 * math.cos(math.radians(lat)) / STEP))
    for k in range(n):
        lon = -180 + (k + 0.5) * 360 / n
        if land(lon, lat):
            globe += [round(lon * 10), round(lat * 10)]
    lat += STEP
(HERE.parent / 'assets/land.js').write_text('window.VL_LAND=' + json.dumps(globe, separators=(',', ':')) + ';\n')

# Flat map: a square grid, lat 84..-58.
F = 3.0
flat = []
lat = 82.5
while lat >= -57:
    lon = -178.5
    while lon < 180:
        if land(lon, lat):
            flat.append([lon, lat])
        lon += F
    lat -= F
(HERE / 'flat_map.json').write_text(json.dumps(flat, separators=(',', ':')))
print('globe points', len(globe) // 2, 'flat dots', len(flat))
