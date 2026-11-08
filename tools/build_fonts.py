"""Build a reader font: subset the main font, fill missing codepoints from donors.

python3 -I build.py OUT MAIN [DONOR:WGHT:RANGES ...]
WGHT is ignored for static donors. Donor glyphs are scaled to the main font's x-height.
"""
import os
import sys
import tempfile
from fontTools import subset
from fontTools.merge import Merger
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools.varLib import instancer

MAIN = ("U+0020-007E,U+00A0-024F,U+02B0-02FF,U+0300-036F,U+0370-03FF,U+0400-045F,U+0490-0491,U+1E00-1EFF,"
        "U+1F00-1FFF,U+2010-2027,U+2030-203A,U+2070-209F,U+20AC,U+2116,U+2122,U+2190-2193,U+2212,U+FB01-FB02")
DROP = ['meta', 'STAT', 'vhea', 'vmtx', 'MATH']


def cut(font, unicodes, feats):
    o = subset.Options()
    o.layout_features = feats
    o.hinting = False
    o.drop_tables += DROP
    s = subset.Subsetter(o)
    s.populate(unicodes=unicodes)
    s.subset(font)
    return font


out, main = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp()
m = cut(TTFont(main), subset.parse_unicodes(MAIN), ['kern', 'liga', 'locl', 'mark', 'mkmk', 'ccmp'])
parts = [os.path.join(tmp, '0.ttf')]
m.save(parts[0])
have = set(m.getBestCmap())
for i, spec in enumerate(sys.argv[3:], 1):
    path, wght, ranges = spec.rsplit(':', 2)
    d = TTFont(path)
    if 'fvar' in d:
        loc = {a.axisTag: a.defaultValue for a in d['fvar'].axes}
        loc.update({'wght': float(wght), **({'wdth': 100.0} if 'wdth' in loc else {})})
        d = instancer.instantiateVariableFont(d, loc)
    want = [c for c in subset.parse_unicodes(ranges) if c not in have and c in d.getBestCmap()]
    if not want:
        continue
    d = cut(d, want, [])
    for t in ('GDEF', 'GSUB', 'GPOS'):
        if t in d:
            del d[t]
    k = m['OS/2'].sxHeight / d['OS/2'].sxHeight
    scale_upem(d, round(d['head'].unitsPerEm * k))
    d['head'].unitsPerEm = m['head'].unitsPerEm
    parts.append(os.path.join(tmp, f'{i}.ttf'))
    d.save(parts[-1])
    have |= set(want)
f = Merger().merge(parts)
f.save(out)
cm = f.getBestCmap()
need = subset.parse_unicodes("U+0041-005A,U+0410-044F,U+0391-03C9,U+1F00-1F07,U+2192,U+00E9,U+0153,U+0101")
print(os.path.basename(out), 'glyphs', len(f.getGlyphOrder()), 'missing key chars:',
      ''.join(chr(c) for c in need if c not in cm and c not in (0x3A2,)) or 'none',
      f'{os.path.getsize(out) // 1024} KB')
