"""회로도 형광 표시 자료(docs/hl.json)를 다시 만든다.

공개문제 PDF 7쪽의 회로도 그림에서 전선(가로·세로 직선)과 이음점을 찾아 묶음으로 나누고,
기호(접점·코일)를 사이에 둔 선 끝을 짝지은 뒤, docs/index.html의 회로도 정답(const ANS=)과 짝짓는다.
구조만으로 구별되지 않는 것은 tools/highlight/hints.py의 단서(맨 아래 줄 부하 순서, 나란한 접점의 좌우)와
글자 인식 결과(tools/highlight/ocr/, Windows 내장 OCR로 만들어 둠)로 가린다.

사용법 (저장소 맨 위 폴더에서):
    pip install pymupdf numpy pillow scipy
    python tools/make_highlight.py          # docs/hl.json 만들기
    python tools/make_highlight.py check    # 확인용 그림 tools/highlight/work/chkNN.png 도 만들기

회로도 정답(ANS)을 고쳤다면 이것도 다시 돌린다. '짝짓기 실패'가 나오면 정답과 회로도가 다르다는 뜻이다.
"""
import glob, os, sys
import pymupdf as fitz
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'highlight')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(HERE, 'work')
os.makedirs(WORK, exist_ok=True)
fs = sorted(glob.glob(os.path.join(ROOT, '전기기능사', '전기기능사-*.pdf')))
assert len(fs) == 18
for i, f in enumerate(fs):
    out = os.path.join(WORK, f'raw{i + 1:02d}.png')
    if os.path.exists(out): continue
    d = fitz.open(f); p = d[6]
    big = max(p.get_images(), key=lambda im: im[2] * im[3])
    pix = fitz.Pixmap(d, big[0])
    if pix.n > 1: pix = fitz.Pixmap(fitz.csGRAY, pix)
    pix.save(out)
sys.path.insert(0, HERE)
os.chdir(WORK)
import extract, export
from extract import load, build, draw
import json
for n in range(1, 19):
    B = load(n); segs = build(B)
    json.dump(segs, open(f'segs{n:02d}.json', 'w'))
out = {}
for n in range(1, 19): export.export(n, out, len(sys.argv) > 1 and sys.argv[1] == 'check')
json.dump(out, open(os.path.join(ROOT, 'docs', 'hl.json'), 'w'), separators=(',', ':'))
print('docs/hl.json 저장')
