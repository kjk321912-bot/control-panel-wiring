"""짝짓기 결과로 앱이 쓸 형광 표시 자료(docs/hl.json)를 만들고, 확인용 그림도 그린다"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from match import run, MAINP
from extract import load
from PIL import Image as _I
# 원본 그림(raw) 좌표 → 앱의 cNN.png 좌표 (tools/make_assets.py: 7쪽, 170dpi, clip (20,95)~)
IMG_BOX = (30.087, 109.262, 811.392, 428.170)
def tf(x, y):
    X = IMG_BOX[0] + x * (IMG_BOX[2] - IMG_BOX[0]) / 6518
    Y = IMG_BOX[1] + y * (IMG_BOX[3] - IMG_BOX[1]) / 2659
    return round((X - 20) * 170 / 72, 1), round((Y - 95) * 170 / 72, 1)
SNAP = 26
def node_graph(segs):
    """한 묶음의 선들을 점·선분 그래프로 만든다 (원본 좌표)"""
    stops = [[(s['x0'], s['y0']), (s['x1'], s['y1'])] for s in segs]
    for i, s in enumerate(segs):
        for j, t in enumerate(segs):
            if i >= j or s['a'] == t['a']: continue
            h, v, hi, vi = (s, t, i, j) if s['a'] == 'h' else (t, s, j, i)
            if h['x0'] - SNAP <= v['x0'] <= h['x1'] + SNAP and v['y0'] - SNAP <= h['y0'] <= v['y1'] + SNAP:
                p = (v['x0'], h['y0']); stops[hi].append(p); stops[vi].append(p)
    pts = []
    def pid(p):
        for k, q in enumerate(pts):
            if abs(p[0] - q[0]) <= SNAP and abs(p[1] - q[1]) <= SNAP: return k
        pts.append(p); return len(pts) - 1
    E = set()
    for i, s in enumerate(segs):
        key = (lambda p: p[0]) if s['a'] == 'h' else (lambda p: p[1])
        ids = []
        for p in sorted(stops[i], key=key):
            k = pid(p)
            if not ids or ids[-1] != k: ids.append(k)
        for a, b in zip(ids, ids[1:]): E.add((min(a, b), max(a, b)))
    return pts, sorted(E)
def nearest(pts, p):
    return min(range(len(pts)), key=lambda k: abs(pts[k][0] - p[0]) + abs(pts[k][1] - p[1]))
def export(n, out, check):
    r = run(n)
    segs, fe, E, m, eA, els = r['segs'], r['fe'], r['E'], r['m'], r['eA'], r['els']
    comp2node = {c: nm for nm, c in m.items()}
    nodes = {}
    for nm, c in m.items():
        ss = [s for s in segs if s['c'] == c]
        pts, ed = node_graph(ss)
        nodes[nm] = dict(pts=pts, ed=ed, t={})
    def put(key, nm, x, y):
        if nm not in nodes: return
        nd = nodes[nm]; nd['t'][key] = nearest(nd['pts'], (x, y))
    for eid, (k, flip) in eA.items():
        d = E[k]; a, b = els[eid]['nodes']; P, Q = fe[d['p']], fe[d['q']]
        A, Bq = (Q, P) if flip else (P, Q)
        if els[eid]['kind'] == 'main':
            pa, pb = els[eid]['pins']; put(pa, a, A['x'], A['y']); put(pb, b, Bq['x'], Bq['y'])
        else:
            put(eid + '@' + a, a, A['x'], A['y']); put(eid + '@' + b, b, Bq['x'], Bq['y'])
    for p, (c, x, y) in r['anchor'].items():
        nm = comp2node.get(c)
        if nm is None:
            nm = next((k for k, nd in r['nodes'].items() if p in nd['pins']), None)
            if nm and nm not in nodes:
                ss = [s for s in segs if s['c'] == c]; pts, ed = node_graph(ss); nodes[nm] = dict(pts=pts, ed=ed, t={}); m[nm] = c
        if nm: put(p, nm, x, y)
    # 확인: 정답의 모든 끝이 그림 점을 가졌는지
    miss = []
    for nm, nd in r['nodes'].items():
        for p in nd['pins']:
            if not (nm in nodes and p in nodes[nm]['t']): miss.append(p)
    for eid, e in els.items():
        if e['kind'] == 'main': continue
        for nm in e['nodes']:
            if not (nm in nodes and eid + '@' + nm in nodes[nm]['t']): miss.append(eid + '@' + nm)
    if miss: print(n, '그림 점 없음:', miss)
    if check:
        B = load(n)
        im = Image.fromarray(np.where(B, 0, 200).astype('uint8')).convert('RGB'); dr = ImageDraw.Draw(im)
        try: font = ImageFont.truetype('arial.ttf', 46); fs = ImageFont.truetype('arial.ttf', 34)
        except Exception: font = fs = None
        rng = np.random.default_rng(5)
        for nm, nd in nodes.items():
            col = tuple(int(v) for v in rng.integers(30, 220, 3))
            for a, b in nd['ed']: dr.line([nd['pts'][a], nd['pts'][b]], fill=col, width=12)
            p = nd['pts'][0]; dr.text((p[0] + 8, p[1] - 50), nm, fill=col, font=font)
            for key, k in nd['t'].items():
                x, y = nd['pts'][k]; dr.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(255, 0, 0))
        for eid, (k, flip) in eA.items():
            d = E[k]
            if els[eid]['kind'] == 'main': continue
            dr.text((d['x'] - 140, d['y'] - 20), eid, fill=(220, 0, 160), font=fs)
        im.resize((im.width // 4, im.height // 4)).save(f'chk{n:02d}.png')
    J = {}
    for nm, nd in nodes.items():
        J[nm] = dict(p=[tf(*p) for p in nd['pts']], e=nd['ed'], t=nd['t'])
    out[str(n)] = J
if __name__ == '__main__':
    out = {}
    ns = list(map(int, sys.argv[2:])) or range(1, 19)
    for n in ns: export(n, out, sys.argv[1] == 'check')
    if sys.argv[1] == 'write':
        from match import ROOT
        import os
        json.dump(out, open(os.path.join(ROOT, 'docs', 'hl.json'), 'w'), separators=(',', ':'))
        print('docs/hl.json 저장')
