"""공개문제 PDF에서 앱에 쓰는 도면 이미지와 동작 사항 글을 다시 만든다.

사용법 (저장소 맨 위 폴더에서):
    pip install pymupdf
    python tools/make_assets.py

만드는 것:
    docs/img/cNN.png   시퀀스 회로도 (PDF 7쪽)
    docs/img/bNN.png   배관 및 기구 배치도 (PDF 5쪽)
    docs/img/pin01.png, pin10.png   기구의 내부 결선도 (PDF 9쪽, 1~9번용 / 10~18번용)
    tools/ops.json     제어회로의 동작 사항 (PDF 8쪽).
                       docs/index.html 안의 `const OPS=` 값에 이 내용이 들어 있다.

이미지를 새로 만들거나 이름을 바꿨으면 docs/sw.js의 CORE 목록과 VERSION도 고칠 것.
"""
import glob
import json
import os
import re

import pymupdf as fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '전기기능사')
IMG = os.path.join(ROOT, 'docs', 'img')


def main():
    fs = sorted(glob.glob(os.path.join(SRC, '전기기능사-*.pdf')))
    assert len(fs) == 18, f'공개문제 PDF가 18개여야 합니다 (찾은 개수: {len(fs)})'
    os.makedirs(IMG, exist_ok=True)

    for i, f in enumerate(fs):
        n = i + 1
        d = fitz.open(f)
        p = d[6]
        r = p.rect
        p.get_pixmap(dpi=170, clip=fitz.Rect(20, 95, r.width - 20, r.height * 0.72),
                     colorspace=fitz.csGRAY).save(os.path.join(IMG, f'c{n:02d}.png'))
        p = d[4]
        r = p.rect
        p.get_pixmap(dpi=110, clip=fitz.Rect(40, 140, r.width - 40, r.height - 70),
                     colorspace=fitz.csGRAY).save(os.path.join(IMG, f'b{n:02d}.png'))

    for n, i in ((1, 0), (10, 9)):
        p = fitz.open(fs[i])[8]
        r = p.rect
        p.get_pixmap(dpi=150, clip=fitz.Rect(40, 130, r.width - 40, r.height - 90),
                     colorspace=fitz.csGRAY).save(os.path.join(IMG, f'pin{n:02d}.png'))

    ops = {}
    for i, f in enumerate(fs):
        p = fitz.open(f)[7]
        lines = []
        for b in p.get_text('blocks'):
            if 100 < b[1] < 780:
                lines.extend(b[4].strip().split('\n'))
        out = []
        for line in lines:
            if line.startswith('11 -'):
                continue
            if re.match(r'^(\d\)|[가-하]\)|\(\d+\)|※)', line) or not out:
                out.append(line)
            else:
                out[-1] += ' ' + line
        ops[str(i + 1)] = [x for x in out if not x.startswith('4)')]
    with open(os.path.join(ROOT, 'tools', 'ops.json'), 'w', encoding='utf-8') as fp:
        json.dump(ops, fp, ensure_ascii=False, indent=1)

    print('완료:', len(os.listdir(IMG)), '개 이미지, tools/ops.json')


if __name__ == '__main__':
    main()
