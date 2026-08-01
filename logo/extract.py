#!/usr/bin/env python3
"""Find the single-colour green logo paths in page.svg and report their bboxes."""
import re, xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
tree = ET.parse('/home/user/workspace/butterfly/logo/page.svg')
root = tree.getroot()

GREEN = 'rgb(68.62793%, 79.216003%, 1.960754%)'
num = re.compile(r'-?\d*\.?\d+(?:[eE][-+]?\d+)?')


def bbox(d):
    xs, ys = [], []
    # crude: treat every coordinate pair in order as x,y
    vals = [float(v) for v in num.findall(d)]
    for i in range(0, len(vals) - 1, 2):
        xs.append(vals[i]); ys.append(vals[i + 1])
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def walk(el, depth=0, inherited=None):
    fill = el.get('fill', inherited)
    tag = el.tag.split('}')[-1]
    if fill == GREEN:
        d = el.get('d')
        if d:
            print(f'{"  "*depth}{tag} d-len={len(d)} bbox={bbox(d)}')
        else:
            # container: report children path bboxes combined
            ds = [c.get('d') for c in el.iter() if c.get('d')]
            if ds:
                bs = [bbox(x) for x in ds if bbox(x)]
                if bs:
                    print(f'{"  "*depth}{tag} GROUP children={len(ds)} '
                          f'bbox=({min(b[0] for b in bs):.1f},{min(b[1] for b in bs):.1f},'
                          f'{max(b[2] for b in bs):.1f},{max(b[3] for b in bs):.1f})')
            else:
                print(f'{"  "*depth}{tag} (green, no path data) attrs={dict(el.attrib)}')
    for c in el:
        walk(c, depth + 1, fill)


walk(root)
