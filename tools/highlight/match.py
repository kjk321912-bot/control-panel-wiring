"""회로도 그림의 묶음·기호를 앱의 정답 회로(ANS)와 짝짓는다."""
import re, json, sys
from extract import load, ends
from edges import free_ends, pairs
from runocr import ocr
from hints import LOADS, LEFT

import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTML = open(os.path.join(ROOT, 'docs', 'index.html'), encoding='utf8').read()
ANS_MAIN = re.search(r"const ANS_MAIN=`(.*?)`;", HTML, re.S).group(1)
ANS_FLS = re.search(r"const ANS_FLS=`(.*?)`;", HTML, re.S).group(1)
ANS = {int(k): v for k, v in re.findall(r"(\d+):`(.*?)`", re.search(r"const ANS=\{(.*?)\};", HTML, re.S).group(1), re.S)}
LOADK = {'c', 'l', 'bz', 'pwr'}
MAINP = [('MCCB.p1', 'L1', 'R', 'MCCB:1', 'MCCB:2'), ('MCCB.p2', 'L2', 'S', 'MCCB:3', 'MCCB:4'), ('MCCB.p3', 'L3', 'T', 'MCCB:5', 'MCCB:6'),
         ('EOCR.m1', 'R', 'U', 'EOCR:1', 'EOCR:7'), ('EOCR.m2', 'S', 'V', 'EOCR:2', 'EOCR:8'), ('EOCR.m3', 'T', 'W', 'EOCR:3', 'EOCR:9'),
         ('MC1.m1', 'U', 'U1', 'MC1:1', 'MC1:7'), ('MC1.m2', 'V', 'V1', 'MC1:2', 'MC1:8'), ('MC1.m3', 'W', 'W1', 'MC1:3', 'MC1:9'),
         ('MC2.m1', 'U', 'U2', 'MC2:1', 'MC2:7'), ('MC2.m2', 'V', 'V2', 'MC2:2', 'MC2:8'), ('MC2.m3', 'W', 'W2', 'MC2:3', 'MC2:9')]

def parse(n):
    nodes, els = {}, {}
    for line in '\n'.join([ANS_MAIN, ANS_FLS if n <= 9 else '', ANS[n]]).split('\n'):
        s = line.strip()
        if not s or s[0] in '~=': continue
        nm, rest = re.match(r'^(\S+):\s*(.*)$', s).groups()
        nd = nodes.setdefault(nm, {'pins': [], 'ends': []})
        for t in rest.split():
            if ':' in t: nd['pins'].append(t); continue
            lab, k = t.split('.'); k = k.split('#')[0]
            e = els.setdefault(t, {'id': t, 'label': lab, 'kind': k, 'nodes': []})
            e['nodes'].append(nm)
    for eid, a, b, pa, pb in MAINP:
        els[eid] = {'id': eid, 'label': eid.split('.')[0], 'kind': 'main', 'nodes': [a, b], 'pins': [pa, pb]}
    return nodes, els

def norm(t):
    t = t.upper().replace('I', '1').replace('O', '0')
    return t

def label_edges(E, words, labels):
    """글자 인식 결과를 가까운 기호에 붙인다"""
    for e in E: e['lab'] = None
    for w in words:
        t = norm(w['t'])
        if t not in labels: continue
        cx, cy = w['x'] + w['w'] / 2, w['y'] + w['h'] / 2
        best = None
        for e in E:
            if e['ax'] == 'v':
                d = None
                if abs(cx - e['x']) < 80 and abs(cy - e['y']) < 80: d = abs(cx - e['x']) + abs(cy - e['y'])  # 원 안
                elif 0 < w['x'] - e['x'] < 200 and abs(cy - e['y']) < 70: d = 100 + (w['x'] - e['x'])        # 오른쪽 이름
            else:
                d = 50 + abs(cx - e['x']) + abs(cy - e['y']) if abs(cx - e['x']) < 120 and 0 < e['y'] - cy < 160 else None  # 위쪽 이름
            if d is not None and (best is None or d < best[0]): best = (d, e)
        if best: best[1]['lab'] = t

def run(n, verbose=False):
    B = load(n)
    segs = json.load(open(f'segs{n:02d}.json'))
    fe = free_ends(segs)
    E, used = pairs(B, fe)
    term = [e for e in E if e['gap'] < 100]          # 단자를 지나가는 선 (TB2·TB3 PE)
    E = [e for e in E if e['gap'] >= 100]
    nodes, els = parse(n)
    labels = {e['label'] for e in els.values()}
    label_edges(E, ocr(n), labels)
    unp = [f for k, f in enumerate(fe) if k not in used]
    # 단자대 단자 위치
    anchor = {}   # 'TB1:L1' -> (comp, x, y)
    tb1 = sorted([f for f in unp if f['y'] < 300 and f['x'] < 1000], key=lambda f: f['x'])
    for k, f in zip(['L1', 'L2', 'L3', 'PE'], tb1): anchor['TB1:' + k] = (f['c'], f['x'], f['y'])
    row = sorted([f for f in unp if 1950 < f['y'] < 2150 and f['x'] < 2000], key=lambda f: f['x'])
    for k, f in zip(['TB2:U', 'TB2:V', 'TB2:W', 'TB3:U', 'TB3:V', 'TB3:W'], row): anchor[k] = (f['c'], f['x'], f['y'])
    pes = sorted(term, key=lambda e: e['x'])
    for k, e in zip(['TB2:PE', 'TB3:PE'], pes): anchor[k] = (e['ca'], e['x'], e['y'])
    if n <= 9:
        bot = sorted([f for f in unp if f['y'] > 2420 and f['x'] > 2000], key=lambda f: f['x'])
        for k, f, p in zip(['E1', 'E2', 'E3'], bot, ['FLS:7', 'FLS:8', 'FLS:1']):
            anchor['TB4:' + k] = (f['c'], f['x'], f['y'])
            other = sorted([g for g in fe if g['c'] == f['c'] and g is not f and g['a'] == 'h' and g['d'] == (-1, 0)], key=lambda g: g['x'])
            if other: anchor[p] = (f['c'], other[0]['x'], other[0]['y'])
    # 고정 단자 → 점 → 묶음
    pinnode = {p: nm for nm, nd in nodes.items() for p in nd['pins']}
    fixed = {}
    for p, (c, x, y) in anchor.items():
        nm = pinnode.get(p)
        if nm is None: continue
        if nm in fixed and fixed[nm] != c: print(n, '고정 단자 충돌', p, nm, fixed[nm], c)
        fixed[nm] = c
    # 되돌아가며 짝짓기
    order = list(els.values())
    sols = []
    m = dict(fixed); inv = {c: k for k, c in m.items()}; eA = {}; usedE = set()
    budget = [200000]
    def cands(e):
        a, b = e['nodes']
        out = []
        for k, d in enumerate(E):
            if k in usedE: continue
            for ca, cb, flip in ((d['ca'], d['cb'], False), (d['cb'], d['ca'], True)):
                okA = (m.get(a) == ca) if a in m else (ca not in inv)
                okB = (m.get(b) == cb) if b in m else (cb not in inv)
                if a not in m and b not in m: okA = okB = False
                if a == b: continue
                if not (okA and okB): continue
                if a not in m and b not in m: continue
                if ca == cb and (a not in m or b not in m): continue
                if a not in m and b not in m: continue
                if (a not in m) and (b not in m): continue
                if a not in m and ca == cb: continue
                out.append((k, ca, cb, flip))
        return out
    want = LOADS[n].split()
    def score():
        s = 0
        ld = sorted(((E[k]['x'], els[eid]['label']) for eid, (k, f) in eA.items() if els[eid]['kind'] in LOADK))
        if [l for _, l in ld] == want: s += 100
        for a, b in LEFT.get(n, []):
            if a in eA and b in eA and E[eA[a][0]]['x'] < E[eA[b][0]]['x']: s += 10
        for eid, (k, flip) in eA.items():
            lab = E[k]['lab']
            if lab: s += 1 if lab == els[eid]['label'] else -3
            kind = els[eid]['kind']
        return s
    def solve():
        budget[0] -= 1
        if budget[0] < 0: return
        rest = [e for e in order if e['id'] not in eA]
        if not rest:
            sols.append((score(), dict(m), dict(eA))); return
        best = None
        for e in rest:
            a, b = e['nodes']
            if a not in m and b not in m: continue
            c = cands(e)
            if best is None or len(c) < len(best[1]): best = (e, c)
            if not c: break
        if best is None: return
        e, c = best
        if not c: return
        for k, ca, cb, flip in c:
            a, b = e['nodes']; add = []
            if a not in m: m[a] = ca; inv[ca] = a; add.append(a)
            if b not in m: m[b] = cb; inv[cb] = b; add.append(b)
            eA[e['id']] = (k, flip); usedE.add(k)
            solve()
            del eA[e['id']]; usedE.discard(k)
            for x in add: del inv[m[x]]; del m[x]
            if len(sols) > 2000: return
    solve()
    if not sols:
        print(n, '짝짓기 실패'); return None
    sols.sort(key=lambda s: -s[0])
    top = [s for s in sols if s[0] == sols[0][0]]
    # 같은 점수의 답끼리 다른 기호 배정
    amb = set()
    for s in top[1:]:
        for eid, v in s[2].items():
            if top[0][2][eid][0] != v[0]: amb.add(eid)
    if verbose or amb:
        print(n, f'답 {len(sols)}개, 최고점 {sols[0][0]} {len(top)}개, 애매한 기호 {sorted(amb)}, 남은 그림 기호 {len(E) - len(top[0][2])}')
    return dict(n=n, segs=segs, fe=fe, E=E, anchor=anchor, m=top[0][1], eA=top[0][2], els=els, nodes=nodes, amb=sorted(amb), nsol=len(sols))

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        r = run(n, True)
