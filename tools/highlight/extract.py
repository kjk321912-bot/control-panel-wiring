"""회로도 그림에서 전선(가로·세로 직선)과 이음점을 찾아 묶음(같은 전위)으로 나눈다."""
import sys, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

L_MIN = 100     # 이보다 짧은 직선은 글자·기호로 보고 버린다 (원본 해상도 px)
TOL = 10        # 끝점이 닿았다고 보는 거리
DOT_R = 10      # 이음점(검은 점) 반지름

def load(n):
    im = np.array(Image.open(f'raw{n:02d}.png'))
    return im > 128

def segments(B):
    segs = []
    for axis in ('h', 'v'):
        st = np.ones((1, L_MIN), bool) if axis == 'h' else np.ones((L_MIN, 1), bool)
        O = ndi.binary_opening(B, structure=st)
        lab, k = ndi.label(O)
        for sl in ndi.find_objects(lab):
            ys, xs = sl
            h, w = ys.stop - ys.start, xs.stop - xs.start
            if axis == 'h' and h <= 16 and w >= L_MIN:
                y = (ys.start + ys.stop - 1) / 2
                segs.append(dict(a='h', x0=xs.start, x1=xs.stop - 1, y0=y, y1=y))
            elif axis == 'v' and w <= 16 and h >= L_MIN:
                x = (xs.start + xs.stop - 1) / 2
                segs.append(dict(a='v', x0=x, x1=x, y0=ys.start, y1=ys.stop - 1))
    return segs

def is_dot(B, x, y):
    x, y = int(round(x)), int(round(y))
    r = DOT_R
    sub = B[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1]
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    m = (xx * xx + yy * yy) <= r * r
    if sub.shape != m.shape:
        return False
    return sub[m].mean() > 0.85

def ends(s):
    return [(s['x0'], s['y0']), (s['x1'], s['y1'])]

def build(B):
    segs = segments(B)
    n = len(segs)
    P = list(range(n))
    def f(i):
        while P[i] != i:
            P[i] = P[P[i]]; i = P[i]
        return i
    def u(i, j): P[f(i)] = f(j)
    used = [[False, False] for _ in segs]
    for i, s in enumerate(segs):
        for j, t in enumerate(segs):
            if i >= j: continue
            # 끝점끼리 (모서리, 일직선 이어짐)
            for a, pa in enumerate(ends(s)):
                for b, pb in enumerate(ends(t)):
                    if abs(pa[0] - pb[0]) <= TOL and abs(pa[1] - pb[1]) <= TOL:
                        u(i, j); used[i][a] = used[j][b] = True
            # 끝점이 다른 선의 중간에 닿음 (T자) → 이음점이 있을 때만
            for (x, y), (p, q, k) in [(e, (s, t, (i, a))) for a, e in enumerate(ends(s))] + [(e, (t, s, (j, b))) for b, e in enumerate(ends(t))]:
                other = q
                TT = 24
                if other['a'] == 'h':
                    on = other['x0'] - TOL < x < other['x1'] + TOL and abs(y - other['y0']) <= TT
                    px, py = x, other['y0']
                else:
                    on = other['y0'] - TOL < y < other['y1'] + TOL and abs(x - other['x0']) <= TT
                    px, py = other['x0'], y
                if on and is_dot(B, px, py):
                    u(i, j); used[k[0]][k[1]] = True
            # 가운데끼리 십자 교차 → 이음점이 있을 때만
            if s['a'] != t['a']:
                h, v = (s, t) if s['a'] == 'h' else (t, s)
                if h['x0'] + TOL < v['x0'] < h['x1'] - TOL and v['y0'] + TOL < h['y0'] < v['y1'] - TOL and is_dot(B, v['x0'], h['y0']):
                    u(i, j)
    comp = [f(i) for i in range(n)]
    ids = {c: k for k, c in enumerate(sorted(set(comp)))}
    for i, s in enumerate(segs):
        s['c'] = ids[comp[i]]
        s['free'] = [not used[i][0], not used[i][1]]
    return segs

def draw(B, segs, out, scale=0.25):
    im = Image.fromarray(np.where(B, 0, 255).astype('uint8')).convert('RGB')
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(3)
    cols = {c: tuple(int(v) for v in rng.integers(40, 230, 3)) for c in set(s['c'] for s in segs)}
    for s in segs:
        d.line([(s['x0'], s['y0']), (s['x1'], s['y1'])], fill=cols[s['c']], width=9)
    for s in segs:
        for k, (x, y) in enumerate(ends(s)):
            if s['free'][k]:
                d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(255, 0, 0), width=4)
    im = im.resize((int(im.width * scale), int(im.height * scale)))
    im.save(out)

if __name__ == '__main__':
    n = int(sys.argv[1])
    B = load(n)
    segs = build(B)
    print(len(segs), 'segs', len(set(s['c'] for s in segs)), 'comps')
    json.dump(segs, open(f'segs{n:02d}.json', 'w'))
    draw(B, segs, f'segs{n:02d}.png')
