# 제어판 배선 시뮬레이터 — 작업 안내

전기기능사 실기 공개문제 1~18번 제어판 배선 연습용 PWA. 사용자는 갤럭시탭·아이패드에서 쓰는 선생님이며, 안내와 화면 문구는 한국어로 쓴다. 전체 정리는 `제어판배선_정리.md`.

## 구조
- 앱은 빌드 과정 없이 `docs/index.html` 한 파일에 있다 (CSS, 기구 정의 `DEFS`, 과제 배치 `LAYOUT`, 배선 경로, 시뮬레이션). 동작 사항 글은 `const OPS=`에 JSON으로 들어 있다.
- GitHub Pages가 `main` 브랜치의 `/docs`를 서비스한다: https://kjk321912-bot.github.io/control-panel-wiring/
- 핀 번호는 공개문제 PDF의 "5) 기구의 내부 결선도"(9쪽)가 기준이다. 짐작으로 바꾸지 말고 PDF를 확인한다.
- 도면 이미지는 `python tools/make_assets.py`로 PDF에서 다시 만든다 (`pip install pymupdf` 필요).

## 고친 뒤 배포할 때 반드시
1. `docs/sw.js`의 `VERSION`을 올린다. 올리지 않으면 설치된 태블릿에 새 버전이 내려가지 않는다.
2. `docs/index.html`의 버전 표시(`· vN`)도 같이 올린다.
3. 이미지를 추가하거나 이름을 바꿨으면 `sw.js`의 `CORE` 목록을 고친다.
4. 커밋 → push → 1~2분 뒤 Pages 반영을 확인한다.

## 확인 방법
- `docs`에서 `python -m http.server`로 띄워서 확인한다. 서비스워커는 `file://`에서 동작하지 않는다.
- 숨김 처리는 `[hidden]{display:none!important}` 규칙에 의존한다. 이 규칙이 빠지자 숨겨진 대화상자가 화면 전체의 터치를 막은 적이 있다.
