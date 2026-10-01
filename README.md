# 제어판 배선 시뮬레이터

전기기능사 실기 공개문제(1~18번)의 제어판 배선을 태블릿에서 연습하는 앱(PWA)입니다.
배치도대로 놓인 기구 단자 사이에 손가락이나 펜으로 전선을 그려 연결하고, 전원을 넣어 회로 동작을 시험합니다.

**앱 주소:** https://kjk321912-bot.github.io/control-panel-wiring/

- 갤럭시탭: Chrome이나 삼성 인터넷에서 메뉴 → 앱 설치
- 아이패드: Safari에서 공유 → 홈 화면에 추가

## 폴더

| 폴더·파일 | 내용 |
|---|---|
| `docs/` | 앱 (GitHub Pages가 이 폴더를 서비스) |
| `전기기능사/` | 공개문제 PDF 원본 |
| `tools/make_assets.py` | PDF에서 도면 이미지와 동작 사항 글을 다시 만드는 스크립트 |
| `제어판배선_정리.md` | 기능, 핀 배치, 동작 규칙, 작업 방법, 진행 기록 전체 정리 |

## 다른 PC에서 시작하기

```
git clone https://github.com/kjk321912-bot/control-panel-wiring.git 제어판배선
cd 제어판배선/docs
python -m http.server 8000
```

브라우저에서 `http://localhost:8000`을 엽니다. 자세한 내용은 [제어판배선_정리.md](제어판배선_정리.md)를 보세요.

앱을 고쳐서 올릴 때는 `docs/sw.js`의 `VERSION`을 꼭 올려야 설치된 태블릿에 새 버전이 내려갑니다.
