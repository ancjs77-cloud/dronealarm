import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import json, html
S=OUT+"shots/"; A=KIT+"art/"
log=json.load(open(S+"log.json"))
F={r:{k:f for f,k in v} for r,v in log.items()}
COMMON={
 "idle":("대기 화면","기지 상황도(상황실과 같은 그림)와 비행장 상세도에 내 위치가 파란 점으로 나옵니다. 경보가 없으면 이 화면으로 대기합니다."),
 "l1_popup":("1단계 관심 알림","드론이 활주로 기준 10km 타원선을 넘으면 진동·경보음·음성과 함께 노란 알림이 뜹니다. [행동 지시 보기]를 누릅니다."),
 "l1_checked":("행동 지시 체크","지시 항목을 실제로 수행하고 하나씩 누르면 ✓ 표시가 됩니다. 모두 체크해야 [완료]가 켜집니다."),
 "l1_done_map":("완료 후 상황도","[완료]를 누르면 걸린 시간이 기록되고, 아래에 드론 이동·속도·도착 예상·나와의 거리가 표시된 상황도가 나옵니다."),
 "l2_popup":("2단계 주의 알림","5km 선을 넘으면 주황 알림이 뜹니다. 이전 단계를 끝내지 못했으면 '이전 단계 미완료'가 함께 표시됩니다."),
 "l2_map":("5km 이내 이글루 지도","2단계부터는 이글루 위치·내 위치·드론 지도가 계속 표시됩니다. 드론이 지도 밖이면 가장자리에 방향과 거리가 나옵니다."),
 "l2_checked":("2단계 행동 지시","지도 아래 행동 지시를 수행·체크한 뒤 [완료]를 누릅니다."),
 "l3_popup":("3단계 경계 알림","3km 선을 넘으면 빨간 알림이 뜹니다. 즉시 행동(대피·입고·통제) 단계입니다."),
 "l3_screen":("3단계 화면","경보 배너, 지도, 3단계 행동 지시가 표시됩니다."),
 "l3_checked":("3단계 완료","모든 항목을 체크하고 [완료]를 누르면 상황실 완료 현황에 즉시 반영됩니다."),
 "l4_popup":("4단계 심각 알림","0.5km 선을 넘으면 진한 빨간 알림이 깜박이며 뜹니다. 전원 엄폐·정지 단계입니다."),
 "l4_screen":("4단계 화면","드론이 비행장 가까이 있습니다. 지도에서 드론 위치와 나와의 거리를 확인하며 지시에 따릅니다."),
 "clear_popup":("상황 해제","상황실이 해제하면 파란 '상황 해제' 알림이 뜨고 대기 상태로 돌아갑니다."),
}
SPEC={
 "pilot":{"l3_screen":("3단계: 배정 이글루 안내","가장 가까운 빈 이글루가 자동 배정되고, 내 위치에서 이글루까지 노란 점선과 방향·거리가 표시됩니다."),
          "l3_arrived":("도착·입고 완료","이글루에 항공기를 넣으면 [도착·입고 완료]를 누릅니다. 상황실 이글루 상태가 '항공기 입고'로 바뀝니다.")},
 "maintenance":{"l3_screen":("3단계: 가장 가까운 이글루로 대피","내 위치에서 가장 가까운 열린 이글루와 방향·거리가 안내됩니다. 즉시 이동합니다."),
          "l3_entered":("입실(대피 완료)","이글루에 들어가면 [입실]을 누릅니다. 이어서 [🔒 Close 완료] 버튼이 나옵니다."),
          "l3_closed":("Close 완료","문을 닫고 [Close 완료]를 누르면 시각이 기록되고 상황실에 '닫힘'으로 표시됩니다."),
          "open_card":("상황 해제 후 Open","해제되면 닫은 이글루의 개방 카드가 나옵니다. 문을 열고 [Open 완료]를 누릅니다.")},
}
SEQ={
 "pilot":["idle","l1_popup","l1_checked","l1_done_map","l2_map","l3_popup","l3_screen","l3_arrived","l4_screen","clear_popup"],
 "maintenance":["idle","l1_popup","l1_checked","l2_map","l3_popup","l3_screen","l3_entered","l3_closed","l4_screen","open_card"],
 "controller":["idle","l1_popup","l1_checked","l1_done_map","l2_popup","l2_map","l3_screen","l3_checked","l4_popup","clear_popup"],
 "security":["idle","l1_popup","l1_checked","l1_done_map","l2_popup","l2_map","l3_screen","l3_checked","l4_popup","clear_popup"],
}
INFO={
 "pilot":("조종사","항공기 운용 중 드론 접근 시 이륙 보류·진로 변경, 3단계부터 배정 이글루로 즉시 이동·입고합니다.",["1단계: 관제 주파수 청취, 접근 방향 확인","2단계: 신규 이륙 보류, 위치 보고","3단계: 이륙 중지, 배정 이글루로 이동·입고","4단계: 항공기·엔진 정지, 입고 확인, 이동 완료 보고"]),
 "maintenance":("정비사","활주로·유도로 작업 인원을 통제하고, 3단계에서 가장 가까운 이글루로 즉시 대피해 문을 닫습니다(Close). 해제 후 문을 엽니다(Open).",["1단계: 작업 인원 위치 파악, 공구·장비 정리, 대피 경로 확인","2단계: 작업 중지 준비, 이동식 장비 고정","3단계: 즉시 대피 → 이글루 입실 → Close 완료","해제 후: Open 완료"]),
 "controller":("관제사","항공기 이착륙 통제와 공중 항공기 안내를 맡습니다. 단계에 따라 이륙 허가 보류, 활주로 운영 중지, 비행장 폐쇄를 방송합니다.",["1단계: 탐지 정보 확인, 비행 중 항공기에 방송","2단계: 신규 이륙 허가 보류, 회피 방향 안내","3단계: 활주로 운영 중지, 지상 이동 중지","4단계: 전 항공기 이동 중지, 비행장 폐쇄 방송"]),
 "security":("방호관계자","대드론 장비 운용과 감시, 접근 경로 추적, 경비 구역 출입 통제와 피해 확인을 맡습니다.",["1단계: 대드론 장비 점검, 감시 강화, 요원 대기","2단계: 대응 요원 배치, 육안 감시, 장비 운용 준비","3단계: 운용 준비 완료 보고, 경로 추적, 출입 통제","4단계: 지휘 승인 대응, 낙하 지점 통제, 피해 보고"]),
}
def cap(role,k): return SPEC.get(role,{}).get(k) or COMMON[k]
pages=[]
def page(body, cls=""): pages.append(f'<section class="pg {cls}">{body}<div class="foot">드론경보 단말 사용 매뉴얼 · 시연용 가상 데이터</div><div class="pno">{len(pages)+1}</div></section>')
# cover
pages.append(f'''<section class="pg cover"><div class="ct"><div class="kicker">AIRBASE C-UAS ALERT SYSTEM</div><h1>드론경보</h1><h2>비행장 드론 위협 경보·행동지시 체계<br>역할별 단말 사용 매뉴얼</h2>
<div class="chips"><span>조종사</span><span>정비사</span><span>관제사</span><span>방호관계자</span><span>상황실 근무자(PC)</span></div><div class="ver">2026. 11. · 시연판 · 모든 부대·인원·장비 정보는 가상</div></div></section>''')
# overview
lv=[("1","관심","10km","#f2c200","#222","대비·준비"),("2","주의","5km","#f57c00","#fff","보류·준비, 이글루 지도 표시"),("3","경계","3km","#e53935","#fff","즉시 대피·입고·통제"),("4","심각","0.5km","#8e0000","#fff","전원 엄폐·정지")]
page(f'''<h3 class="ttl">체계 개요와 공통 사용법</h3><div class="two"><div class="panel"><h4>경보 단계 (활주로 기준 타원 거리)</h4><table class="lv">{"".join(f'<tr><td><span style="background:{c};color:{t}">{n}단계 {nm}</span></td><td>{d}</td><td>{a}</td></tr>' for n,nm,d,c,t,a in lv)}</table>
<h4>공통 규칙</h4><ul><li>단계는 올라가기만 하고, 해제는 상황실만 할 수 있습니다.</li><li>알림 → [행동 지시 보기] → 항목 수행·체크 → [완료] 순서로 진행합니다.</li><li>모든 항목을 체크해야 [완료]가 켜지고, 걸린 시간이 기록됩니다.</li><li>도착 예상은 드론이 활주로 중앙에 닿는 시점 기준입니다.</li><li>훈련은 파란 띠 [훈련], 실제는 빨간 띠로 표시됩니다.</li></ul></div>
<div class="panel"><h4>화면 구성</h4><img src="{S}room_board_l3.png" class="wide"><p class="sm">PC 시연 보드: 왼쪽 상황실, 오른쪽 역할별 휴대폰 화면. 같은 PC의 모든 창이 실시간으로 연동됩니다.</p>
<h4>단말 시작</h4><ul><li>휴대폰: APK 설치 → 앱 실행 → 직능·호출부호 선택</li><li>PC: 드론경보_PC.html을 크롬으로 열기 → PIN 입력</li></ul></div></div>''')
toc_i=1
for role in ["pilot","maintenance","controller","security"]:
    nm,desc,steps=INFO[role]; seq=SEQ[role]; toc_i+=1
    for pi in range(0,len(seq),5):
        chunk=seq[pi:pi+5]
        head=f'<h3 class="ttl"><span class="no">{toc_i-1}</span>{nm} {"" if pi==0 else "(계속)"}</h3>'
        intro=f'<div class="intro"><b>{html.escape(desc)}</b><div class="steps">{"".join(f"<span>{html.escape(s)}</span>" for s in steps)}</div></div>' if pi==0 else '<div class="intro sm2">3단계 이후와 상황 해제 절차입니다.</div>'
        cards="".join(f'<div class="ph"><div class="num">{pi+i+1}</div><img src="{S}{F[role][k]}"><div class="c1">{html.escape(cap(role,k)[0])}</div><div class="c2">{html.escape(cap(role,k)[1])}</div></div>' for i,k in enumerate(chunk))
        page(head+intro+f'<div class="phones">{cards}</div>')
# room (PC)
room=[("room_board_idle.png","시연 보드 · 대기","PIN 입력 후 상황실 화면. 왼쪽에 기지 상황도와 가상 표적 시뮬레이터, 오른쪽에 역할별 휴대폰 화면이 있습니다."),
      ("room_board_l1.png","가상 표적 시작 · 1단계 발령","출발 거리·속도·방위·배속을 정하고 ▶ 시작. 타원선을 넘을 때마다 자동으로 단계가 발령되고 전 단말에 알림이 갑니다."),
      ("room_board_l3done.png","3단계 · 직능별 완료 현황·이글루 상태","직능별 완료/접속 수, 개인별 완료 시간, 경보 타임라인, 이글루별 상태(배정·입고·대피·닫힘)를 실시간으로 확인합니다."),
      ("room_board_l4.png","4단계 심각 · 상황도","드론의 지나온 항적·예상 경로와 속도·활주로 중앙까지 거리·도착 예상이 표시됩니다. [일시정지]로 설명 시간을 확보할 수 있습니다."),
      ("room_board_reset_cd.png","상황 해제 · 자동 복귀","[상황 해제] 후 정비사가 모든 이글루를 Open하면 5초 뒤 처음 시연 상태로 돌아갑니다. [⟲ 처음 상태로]로 즉시 복귀도 가능합니다."),
      ("room_report_c.png","기록 · 상세 타임라인과 보고서","지난 상황을 고르면 발령·완료·이글루 조치가 시간 순으로 나옵니다. [보고서 초안 만들기]로 결과 보고서를 만듭니다.")]
for i,(f,t,d) in enumerate(room):
    page(f'<h3 class="ttl"><span class="no">5</span>상황실 근무자 (PC 버전){"" if i==0 else " (계속)"}</h3>'+(f'<div class="intro"><b>상황실은 드론 탐지 시 단계 발령을 확인하고, 직능별 조치 완료와 이글루 상태를 감독하며, 상황 해제와 결과 보고를 맡습니다. PIN 1234(변경 가능), 5회 틀리면 1분 잠금.</b></div>' if i==0 else "")+
         f'<div class="pc1"><div class="num">{i+1}</div><img src="{S}{f}"><div class="side"><div class="c1">{t}</div><div class="c2">{d}</div></div></div>')
css=f'''@page{{size:A4 landscape;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;color:#e8f4ff}}
.pg{{width:297mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;background:url({A}bg_a4_dim.jpg) center/cover;padding:12mm 14mm 14mm}}
.cover{{background:url({A}bg_a4.jpg) center/cover;padding:0}}.cover .ct{{position:absolute;left:16mm;top:30mm;background:rgba(2,10,24,.72);border:1px solid #2ad4ff;border-radius:6mm;padding:12mm 14mm;width:150mm}}
.kicker{{color:#5ff6ff;letter-spacing:3px;font-size:11pt}}h1{{font-size:52pt;margin:2mm 0;color:#fff;text-shadow:0 0 12px #18e0ff}}h2{{font-size:17pt;font-weight:500;margin:0 0 8mm;color:#cfe9ff;line-height:1.5}}
.chips span{{display:inline-block;border:1px solid #5ff6ff;color:#bffcff;border-radius:20px;padding:1.5mm 4mm;margin:0 2mm 2mm 0;font-size:11pt}}.ver{{margin-top:6mm;color:#8fb3d0;font-size:10pt}}
.ttl{{margin:0 0 4mm;font-size:20pt;color:#fff;border-bottom:2px solid #2ad4ff;padding-bottom:2mm}}.ttl .no{{display:inline-block;background:#2ad4ff;color:#021428;border-radius:2mm;padding:0 3mm;margin-right:3mm}}
.intro{{background:rgba(4,20,44,.8);border-left:4px solid #2ad4ff;padding:2.5mm 4mm;font-size:10.5pt;margin-bottom:4mm}}.intro .steps{{margin-top:2mm;display:flex;gap:2mm;flex-wrap:wrap}}.intro .steps span{{background:rgba(42,212,255,.15);border:1px solid rgba(42,212,255,.5);border-radius:2mm;padding:.8mm 2.5mm;font-size:9.5pt}}.sm2{{font-size:10pt}}
.phones{{display:flex;gap:4mm;justify-content:space-between}}.ph{{width:47mm;position:relative}}.ph img{{width:100%;display:block;filter:drop-shadow(0 0 4px rgba(42,212,255,.4))}}
.num{{position:absolute;left:-2mm;top:-2mm;width:8mm;height:8mm;border-radius:50%;background:#ff9f1a;color:#111;font-weight:900;text-align:center;line-height:8mm;font-size:11pt;z-index:2}}
.c1{{font-weight:900;font-size:11pt;margin-top:2mm;color:#7df9ff}}.c2{{font-size:9pt;line-height:1.45;color:#dbe9f6}}
.two{{display:flex;gap:6mm}}.panel{{flex:1;background:rgba(4,20,44,.82);border:1px solid rgba(42,212,255,.5);border-radius:4mm;padding:4mm 5mm;font-size:10.5pt}}.panel h4{{margin:1mm 0 2mm;color:#7df9ff;font-size:12pt}}.panel ul{{margin:0;padding-left:5mm;line-height:1.6}}
.lv{{width:100%;border-collapse:collapse;margin-bottom:3mm}}.lv td{{padding:1.8mm 2mm;border-bottom:1px solid rgba(255,255,255,.15)}}.lv span{{border-radius:2mm;padding:.8mm 3mm;font-weight:900}}
.wide{{width:100%;border-radius:2mm;border:1px solid #2ad4ff}}.sm{{font-size:9pt;color:#bcd}}
.pcs{{display:flex;gap:6mm}}.pc{{flex:1;position:relative;background:rgba(4,20,44,.82);border:1px solid rgba(42,212,255,.5);border-radius:3mm;padding:3mm}}.pc img{{width:100%;border-radius:1.5mm;display:block}}.pc .c2{{font-size:10pt}}
.pc1{{position:relative;display:flex;gap:5mm;background:rgba(4,20,44,.85);border:1px solid rgba(42,212,255,.5);border-radius:3mm;padding:4mm;align-items:flex-start}}.pc1 img{{width:205mm;max-height:140mm;object-fit:contain;object-position:top left;border-radius:1.5mm}}.pc1 .side{{flex:1}}.pc1 .c1{{font-size:14pt;margin-top:0}}.pc1 .c2{{font-size:11pt;line-height:1.6;margin-top:2mm}}
.foot{{position:absolute;left:14mm;bottom:6mm;font-size:8pt;color:#7fa6c4}}.pno{{position:absolute;right:14mm;bottom:6mm;font-size:9pt;color:#7fe8ff}}'''
open(KIT+"manual/manual.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages)}</body></html>')
print(len(pages),"pages")
