# 인수인계서 — 드론경보 시연판 (2026-11-24 기준)

## 지금까지 완료된 것
- PRD "비행장 드론 위협 경보·행동지시 앱(가칭 드론경보)" 기준 웹앱 + 안드로이드 APK(WebView, 진동·TTS·GPS 브리지)
- PC 시연 보드: 왼쪽 상황실(상황도·시뮬레이터·완료 현황·타임라인·이글루 상태도), 오른쪽 조종사·정비사·방호관계자 휴대폰 3대(갤럭시 S 울트라 모양)
- 상황도: 비행장 중심, 활주로(13/31) 방향 타원 경보선, 지형 모식도, 가상 표적 항적·예상 경로·속도/활주로 중앙 거리/도착 예상 정보 상자
- 이글루 10개 분산 가상 배치, 조종사 자동 배정·입고, 정비사 대피·Close·해제 후 Open, 상황실 이글루별 상태
- 이글루 상태도: 흰 활주로, 방위표, 축척, 주요 지점(공개 지명 대략 위치) 방향·거리
- 휴대폰: 대기 화면 기지 상황도 + 비행장 상세도(역할별 다른 가상 위치), 1단계 완료 후 상황도, 2단계부터 이글루 지도 고정
- 상황 종료 후 자동 처음 상태 복귀 + [처음 상태로] 버튼
- 문서: docs/드론경보_체계소개.pptx(5장), docs/드론경보_역할별_사용매뉴얼.pdf(조종사·정비사·관제사·방호관계자·상황실 PC, 미래형 배경)
- GitHub: ancjs77-cloud/dronealarm (main)

## 2026-11-24 세션에서 추가된 것 (자세한 내용: `세션정리_2026-11-24.md`)
- 상황도 클릭 확대, PC 보드 왼쪽 칸 560px, 상황실 상황도에 주변 주요 지점(공개 지명 대략 위치) 표시, 휴대폰 지도는 지명 없음
- APK 재빌드(서명 키 변경 → 휴대폰은 예전 앱 삭제 후 설치)
- **Vercel 배포 완료: https://dronealarm.vercel.app** (프로젝트 hong-ab60/dronealarm, GitHub 연결 → main 푸시 시 자동 배포. 연결 후 첫 자동 배포는 아직 미확인)
- **Supabase 기기 연동 코드 작성(미커밋)**: `drone_state` 테이블 한 행(방 코드)에 상태 저장, rev 비교 저장 + 1초 확인. `supabase/setup.sql`, `SUPA_DEFAULT`에 URL·공개 키 넣으면 활성. APK 매니페스트에 INTERNET 권한 추가(미빌드)

## 남은 일 / 사용자가 원했던 다음 단계 (우선순위 순)
1. **Supabase 연동 마무리** — 사용자에게 Project URL·공개 키(anon/publishable) 받기 → `SUPA_DEFAULT` 입력 → 창 2개로 연동 시험 → 커밋·푸시(Vercel 자동 배포 확인) → APK 재빌드.
2. Gemini 등 AI 보고서 — 키 필요. 현재 규칙 기반 보고서로 대체 중.
3. 확인 필요/개선 후보
   - 조종사 비행 단계(시동·지상활주·이륙·착륙) 4가지 구분: 과거(이전 Kotlin 버전)에 요청·구현했으나 PRD 재구성 후 현재 PROC에는 없음. 사용자에게 다시 넣을지 확인.
   - 연동을 1초 확인(폴링) 대신 Supabase Realtime(WebSocket)으로 바꾸면 더 빠름(필요 시).
   - 동대구IC 등 주요 지점 좌표는 근사값 — 사용자가 정확한 값을 주면 `LANDMARKS` 수정.
   - 갤럭시에서 APK 설치가 막힘(자동 차단/Play 프로텍트). 사용자는 PC 시연을 주로 사용. Vercel 주소로 대체 가능.

## Windows 작업 메모
- PowerShell 실행 정책 때문에 `npx` 대신 `npx.cmd` (예: `npx.cmd vercel deploy --prod --yes`).
- GitHub 푸시 로그인은 `git -c credential.gitHubAuthModes=browser push origin main` (브라우저 승인).
- 로컬 시연 서버: `node .claude/serve.js` → http://localhost:5173

## 사용자 성향·소통
- 한국어, 짧은 지시를 연속으로 보냄(오타 많음: "시현"=시연, "vessel"=Vercel, "superbase"=Supabase).
- 결과 화면(스크린샷)으로 확인하는 것을 선호. 변경 후 PC 시연 파일·APK·GitHub를 같이 갱신해 주면 좋음.
- 실제 군사 좌표 요청 시 정중히 거절하고 가상/현장 GPS 등록으로 안내(이미 합의된 방향).

## 바로 시작하는 법 (Claude Code)
```
git clone https://github.com/ancjs77-cloud/dronealarm && cd dronealarm
# CLAUDE.md 와 이 파일을 읽고, 남은 일 1번(Vercel 배포)부터 사용자에게 확인 후 진행
```
