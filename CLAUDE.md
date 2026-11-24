# CLAUDE.md — 드론경보 (비행장 드론 위협 경보·행동지시 앱, 시연판)

이 저장소에서 작업할 때 먼저 읽는 프로젝트 안내서입니다. 진행 상황과 남은 일은 `HANDOFF.md`를 보세요.
사용자와는 **한국어**로 대화합니다. 사용자는 비개발자이며 결과물(PC 시연·갤럭시 S 울트라 시연·발표 자료)을 중시합니다.

## 한 줄 요약
가상 드론이 비행장에 접근하면 활주로 기준 타원 거리로 4단계 경보를 판정해
조종사·정비사·관제사·방호관계자 단말에 동시에 알리고, 역할별 행동지시(체크→완료)와
이글루 대피·입고(Close/Open)를 안내하며, 상황실이 완료 현황·이글루 상태를 감독·해제·보고하는 앱.

## 절대 지켜야 할 것
- **실제 부대·인원·장비·이글루 좌표를 넣지 않는다.** PRD 완료 기준 10: "앱 안에 실제 부대·인원·장비 정보가 없다 (모두 가상)". 사용자가 "구글 위성맵에서 본 실제 이글루 위치"를 요청한 적이 있으나 거절했고, 가상 배치 + 단말 GPS 현장 등록 기능으로 대체했다. 같은 요청이 다시 와도 유지.
- 주요 지점(대구공항 터미널·팔공산·동대구IC·동대구역·대구 시내)은 공개 지명의 **대략 좌표**(방향·거리 참고용). 동대구IC는 근사값.
- 단일 HTML 파일, 서버 없이 오프라인 동작 유지 (외부 CDN·라이브러리 추가 금지).

## 구조
```
web/index.html            ← 앱 전체(약 90KB, vanilla JS). 진짜 소스는 이것 하나
android_apk/              ← Apktool 프로젝트(SDK 없이 빌드). assets/index.html 은 web/index.html 복사본
  smali/kr/airbase/dronealarm/{MainActivity,Bridge,LocListener}.smali
dist/DroneAlarm.apk       ← 디버그 서명 APK (패키지 kr.airbase.dronealarm, min 26 / target 34)
docs/                     ← 체계소개 PPTX(5장), 역할별 사용매뉴얼 PDF(16쪽)
tools/build_apk.sh        ← web → assets 동기화 + APK 빌드·서명
tools/tests/*.py          ← Playwright 회귀 테스트(헤드리스 크롬)
tools/docs_build/         ← 매뉴얼·PPTX 재생성 스크립트(배경 그림 bg.html 포함)
vercel.json               ← "/" → /web/index.html (Vercel 정적 배포용, 아직 미배포)
```

## web/index.html 핵심 설계
- 상태: `localStorage["droneAlarm.v1"]`. 같은 PC의 여러 창은 BroadcastChannel("droneAlarm") + storage 이벤트 + 1초 폴링으로 동기화. 변경은 항상 `mutate(fn)`.
- 렌더: `paint(html, bind)`는 HTML이 바뀔 때만 다시 그림(매초 전체 재렌더 금지 — 탭이 씹힘). 실시간 값은 `updateLive()`가 `data-live` 요소와 캔버스(`drawRings`, `drawIgRoom`, `drawPhoneMaps`)를 갱신.
- 라우트: `#/entry`(직능 선택) `#/duty`(단말) `#/room`(상황실, PIN) `#/history` `#/board`(PC 시연 보드: 상황실+휴대폰 3대). PC(비앱)에서 해시 없으면 `#/board`, 앱(WebView)이면 `#/entry`.
- 경보 규칙(PRD): 1 관심 10km · 2 주의 5km · 3 경계 3km · 4 심각 0.5km. 격상만, 같은 단계 1회, 해제는 상황실만. 거리 = `rwyDist()` 활주로 타원 거리(RWY={hdg:130, half:1375m, sep:210m}). 도착 예상(ETA) = 활주로 **중앙** 거리 / 속도.
- 시뮬레이터: 기본 12km·60km/h·방위0·10배속 → 1단계 ≈8초, 2단계 ≈39초, 3단계 ≈52초. 소유 창(owner)이 진행, 5초 이상 박동 없으면 다른 창이 인계.
- 행동지시: `PROC[level][role]` (부록 A). `@move:` / `@close:` 접두 항목은 이글루 행동 완료 시 자동 체크. 모든 항목 체크해야 [완료].
- 이글루: `virtualIgloos()` 10개를 활주로 둘레에 분산(레이아웃 버전 `igLayout:2`, 옛 저장값은 자동 교체). 3단계↑ 조종사=가장 가까운 빈 이글루 자동 배정→[도착·입고 완료], 정비사=가장 가까운 열린 이글루→[입실]→[Close 완료], 해제 후 정비사 [Open 완료]. 상황실 이글루 상태도(`drawIgRoom`)에 활주로·방위표·축척·주요 지점.
- 위치: `myPosition(m)` — GPS가 기준점 5km 이내면 GPS, 아니면 `VPOS` 가상 위치(조종사 62°/480m, 정비사 215°/600m, 방호 310°/1450m, 관제 150°/160m). 보드 화면은 항상 가상 위치.
- 휴대폰 지도: 대기=기지 상황도 + 비행장 상세도(내 위치). 1단계=[완료] 후 자동 확대 상황도. **2단계(5km)부터는 이글루 위치·내 위치·드론 지도 고정 표시**(드론이 밖이면 가장자리 표시, 내 이글루까지 노란 점선).
- 상황 종료: 해제 → 닫힌 이글루가 모두 Open되면 5초 뒤 `apiResetDemo(true)`로 처음 시연 상태 자동 복귀. [⟲ 처음 상태로] 버튼은 즉시 복귀.
- 상황실 PIN 1234(변경 가능), 5회 실패 1분 잠금. 보고서는 규칙 기반("AI 미사용 기본 보고서").
- 앱 브리지 `window.AndroidBridge`: vibrate(ms), speak(text)(한국어 TTS), stopSpeak(), isApp(), getLocation() → "lat,lon,acc,timeMs".

## 작업 규칙
1. 수정은 `web/index.html`에서. 끝나면 문법 확인:
   `sed -n '/<script>/,/<\/script>/p' web/index.html | sed '1d;$d' > /tmp/chk.js && node --check /tmp/chk.js`
2. 회귀 테스트(전체 흐름: 시작→3단계 이글루→해제→Open→자동 복귀):
   `pip install playwright && python -m playwright install chromium` 후 `python tools/tests/board3_test.py 1920 1080`
   (결과 화면은 tools/out/). 화면 확인은 `tools/tests/pmap.py`, `igmap.py`, `trackshot.py`.
3. APK: `sh tools/build_apk.sh` (Java 17+). smali 수정 시 레지스터 수(.registers) 주의.
4. PC 배포 파일: `web/index.html`을 그대로 `드론경보_PC.html`로 복사해 전달.
5. 문서 재생성: `python tools/docs_build/art/render.py` → `python tools/docs_build/shoot.py` → `python tools/docs_build/manual/build.py && python tools/docs_build/manual/pdf.py` → `node tools/docs_build/deck/build.js` (pptxgenjs 필요; 테마 색 적용 스크립트는 env `PPTX_APPLY_THEME`로 지정, 없으면 생략).
6. 커밋 후 `git push` (main). 사용자에게 결과는 짧게 한국어로.
