const pptxgen = require("pptxgenjs");
let applyTheme=async()=>{}; try{ ({applyTheme}=require(process.env.PPTX_APPLY_THEME||"./apply_theme.js")); }catch(e){ console.log("apply_theme.js 없음: 테마 색 적용 생략"); }
const path=require("path"); const R=path.resolve(__dirname,"../../.."); const S=R+"/tools/out/shots/", A=R+"/tools/docs_build/art/";
const THEME={ name:"Drone Alert Night", headFontFace:"Malgun Gothic", bodyFontFace:"Malgun Gothic",
  colors:{ dk1:"0B1626", lt1:"FFFFFF", dk2:"04142C", lt2:"CFE9FF", accent1:"2AD4FF", accent2:"FF9F1A", accent3:"E53935", accent4:"F2C200", accent5:"7DF9FF", accent6:"8E0000", hlink:"5FF6FF", folHlink:"9FB3C8" } };
(async()=>{
const pres=new pptxgen(); pres.layout="LAYOUT_16x9"; pres.title="드론경보 체계 소개"; pres.theme={headFontFace:THEME.headFontFace, bodyFontFace:THEME.bodyFontFace};
const C=pres.SchemeColor;
pres.defineSlideMaster({ title:"COVER", background:{path:A+"bg_16x9.jpg"},
  objects:[{placeholder:{options:{name:"title",type:"title",x:0.55,y:1.25,w:6.2,h:1.0,fontSize:44,bold:true,color:C.background1,align:"left"},text:""}},
           {placeholder:{options:{name:"body",type:"body",x:0.55,y:2.25,w:6.2,h:1.0,fontSize:18,color:C.background2,align:"left"},text:""}}]});
pres.defineSlideMaster({ title:"CONTENT", background:{path:A+"bg_16x9_dim.jpg"},
  objects:[{line:{x:0.45,y:0.92,w:9.1,h:0,line:{color:C.accent1,width:1.5}}},
           {text:{text:"드론경보 · 시연용 가상 데이터",options:{x:0.45,y:5.28,w:5,h:0.25,fontSize:8,color:C.text2==null?C.background2:C.background2}}},
           {placeholder:{options:{name:"title",type:"title",x:0.45,y:0.3,w:9.1,h:0.6,fontSize:24,bold:true,color:C.background1,align:"left"},text:""}}],
  slideNumber:{x:9.2,y:5.25,w:0.4,h:0.25,fontSize:9,color:C.accent1}});
const card=(s,x,y,w,h,name)=>s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,rectRadius:0.08,fill:{color:C.text2,transparency:15},line:{color:C.accent1,width:1},objectName:name});
// 1 cover
let s=pres.addSlide({masterName:"COVER"});
s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.35,y:0.75,w:6.6,h:3.55,rectRadius:0.12,fill:{color:"020A18",transparency:25},line:{color:C.accent1,width:1.25},objectName:"cover panel"});
s.addText("AIRBASE C-UAS ALERT SYSTEM",{x:0.55,y:0.92,w:6,h:0.35,fontSize:12,color:C.accent5,charSpacing:3,isTextBox:true});
s.addText("드론경보",{placeholder:"title"});
s.addText("비행장 드론 위협 경보·행동지시 체계",{placeholder:"body"});
s.addText([{text:"탐지 → 단계 경보 → 역할별 행동지시 → 완료 확인 → 해제·보고",options:{breakLine:true}},{text:"2026. 11. · 시연판",options:{color:C.background2,fontSize:11}}],{x:0.55,y:3.3,w:6.3,h:0.85,fontSize:13,color:C.accent2,bold:true,isTextBox:true});
s.addNotes("표지. 비행장에 접근하는 드론을 탐지하면 단계별 경보를 조종사·정비사·관제사·방호관계자에게 동시에 보내고, 역할별 행동을 지시·확인하는 체계를 소개합니다.");
// 2 concept
s=pres.addSlide({masterName:"CONTENT"}); s.addText("왜 필요한가 · 체계 개념",{placeholder:"title"});
card(s,0.45,1.1,3.1,3.95,"problem card");
s.addText([{text:"현재의 문제",options:{bold:true,color:C.accent3,fontSize:15,breakLine:true}},
  {text:"드론 접근 정보가 무전·전화로 차례차례 전달돼 늦음",options:{bullet:true,breakLine:true}},
  {text:"역할마다 무엇을 해야 하는지 현장에서 헷갈림",options:{bullet:true,breakLine:true}},
  {text:"누가 언제 조치했는지 확인·기록이 어려움",options:{bullet:true,breakLine:true}},
  {text:"대피할 이글루를 각자 판단",options:{bullet:true}}],{x:0.6,y:1.2,w:2.85,h:3.7,fontSize:12,color:C.background1,valign:"top",paraSpaceAfter:6,isTextBox:true});
const steps=[["탐지","가상 표적·탐지체계\n거리·속도·방위"],["단계 판정","활주로 기준 타원\n10·5·3·0.5km"],["동시 경보","진동·경보음·음성\n전 단말 동시"],["행동지시·완료","역할별 체크리스트\n이글루 안내"],["감독·해제·보고","완료 현황·이글루 상태\n타임라인·보고서"]];
steps.forEach(([t,d],i)=>{ const y=1.1+i*0.8;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:3.85,y,w:5.7,h:0.66,rectRadius:0.08,fill:{color:C.text2,transparency:10},line:{color:i==2?C.accent2:C.accent1,width:1},objectName:"flow step "+(i+1)});
  s.addShape(pres.shapes.OVAL,{x:3.97,y:y+0.11,w:0.44,h:0.44,fill:{color:i==2?C.accent2:C.accent1},line:{type:"none"},objectName:"flow num "+(i+1)});
  s.addText(String(i+1),{x:3.97,y:y+0.11,w:0.44,h:0.44,align:"center",valign:"middle",fontSize:14,bold:true,color:C.text2,margin:0,isTextBox:true});
  s.addText(t,{x:4.55,y,w:1.9,h:0.66,fontSize:15,bold:true,color:C.background1,valign:"middle",isTextBox:true});
  s.addText(d,{x:6.45,y,w:3.0,h:0.66,fontSize:10.5,color:C.background2,valign:"middle",isTextBox:true});
});
s.addNotes("문제와 체계 개념. 5단계 흐름: 탐지, 활주로 기준 단계 판정, 전 단말 동시 경보, 역할별 행동지시·완료, 상황실 감독·해제·보고.");
// 3 levels x roles table
s=pres.addSlide({masterName:"CONTENT"}); s.addText("4단계 경보와 역할별 핵심 행동",{placeholder:"title"});
const hd=(t)=>({text:t,options:{bold:true,color:C.text2,fill:{color:C.accent1},align:"center"}});
const lv=(t,f,c)=>({text:t,options:{bold:true,fill:{color:f},color:c,align:"center",valign:"middle"}});
const cell=(t)=>({text:t,options:{color:C.background1,fill:{color:C.text2}}});
const rows=[[hd("단계"),hd("조종사"),hd("정비사"),hd("관제사"),hd("방호관계자")],
 [lv("1 관심\n10km",C.accent4,C.text1),cell("관제 주파수 청취\n접근 방향 확인"),cell("작업 인원 위치 파악\n대피 경로 확인"),cell("탐지 정보 확인\n비행 중 항공기 방송"),cell("대드론 장비 점검\n감시 강화")],
 [lv("2 주의\n5km",C.accent2,C.background1),cell("신규 이륙 보류\n현재 위치 보고"),cell("작업 중지 준비\n장비 고정"),cell("이륙 허가 보류\n회피 방향 안내"),cell("대응 요원 배치\n장비 운용 준비")],
 [lv("3 경계\n3km",C.accent3,C.background1),cell("이륙 중지\n배정 이글루 입고"),cell("가장 가까운 이글루 대피\nClose 완료"),cell("활주로 운영 중지\n지상 이동 중지"),cell("경로 추적 유지\n출입 통제")],
 [lv("4 심각\n0.5km",C.accent6,C.background1),cell("항공기·엔진 정지\n입고 확인 보고"),cell("전원 엄폐\n인원 확인 보고"),cell("전 항공기 이동 중지\n비행장 폐쇄 방송"),cell("지휘 승인 대응\n피해 확인 보고")]];
s.addTable(rows,{x:0.45,y:1.1,w:9.1,colW:[1.3,1.95,1.95,1.95,1.95],rowH:[0.36,0.78,0.78,0.78,0.78],fontSize:11,border:{type:"solid",pt:0.75,color:"2AD4FF"},valign:"middle"});
s.addText("단계는 올라가기만 하며 해제는 상황실만 가능 · 해제 후 정비사가 이글루 Open",{x:0.45,y:4.75,w:9.1,h:0.35,fontSize:11,color:C.accent5,isTextBox:true});
s.addNotes("경보 단계는 활주로를 장축으로 한 타원 거리 기준. 각 단계에서 역할별 핵심 행동 2가지씩.");
// 4 features with screenshots
s=pres.addSlide({masterName:"CONTENT"}); s.addText("주요 기능 · 상황실과 단말",{placeholder:"title"});
s.addImage({path:S+"room_map_l3.png",x:0.45,y:1.1,w:3.15,h:3.17,objectName:"room map",altText:"상황실 상황도: 활주로 기준 타원 경보선과 드론 항적"});
s.addText("상황실 상황도: 항적·속도·도착 예상",{x:0.45,y:4.3,w:3.15,h:0.3,fontSize:10,color:C.background2,align:"center",isTextBox:true});
const ph=[["pilot_10_l3_screen.png","조종사: 배정 이글루"],["maintenance_12_l3_closed.png","정비사: 대피·Close"]];
ph.forEach(([f,t],i)=>{ s.addImage({path:S+f,x:3.8+i*1.5,y:1.05,w:1.38,h:3.28,objectName:"phone "+t,altText:t}); s.addText(t,{x:3.7+i*1.5,y:4.33,w:1.6,h:0.3,fontSize:9.5,color:C.background2,align:"center",isTextBox:true}); });
const feats=[["동시 경보","진동·경보음·음성, 훈련/실제 구분"],["행동지시 체크","전 항목 체크 시 완료, 소요 시간 기록"],["이글루 자동 안내","가장 가까운 빈 이글루 배정·대피, Close/Open"],["실시간 감독","직능별 완료 현황·이글루 상태·타임라인"],["기록·보고","상황별 타임라인과 보고서 초안"]];
feats.forEach(([t,d],i)=>{ const y=1.05+i*0.72; card(s,6.9,y,2.65,0.62,"feature "+(i+1));
  s.addText([{text:t,options:{bold:true,color:C.accent1,fontSize:12,breakLine:true}},{text:d,options:{fontSize:9,color:C.background1}}],{x:7.0,y,w:2.5,h:0.62,valign:"middle",isTextBox:true}); });
s.addNotes("상황실 상황도와 단말 화면 예시. 5가지 핵심 기능.");
// 5 demo & effects
s=pres.addSlide({masterName:"CONTENT"}); s.addText("시연 구성과 기대효과",{placeholder:"title"});
s.addImage({path:S+"room_board_l3.png",x:0.45,y:1.1,w:5.0,h:2.8,objectName:"board shot",altText:"PC 시연 보드: 상황실과 휴대폰 4대"});
s.addText([{text:"시연 방법",options:{bold:true,color:C.accent2,fontSize:13,breakLine:true}},
  {text:"PC: 드론경보_PC.html → PIN → 상황실 + 휴대폰 화면 동시 시연",options:{bullet:true,breakLine:true}},
  {text:"휴대폰: APK 설치(갤럭시) · 가상 표적 10배속 약 1분에 3단계",options:{bullet:true,breakLine:true}},
  {text:"소스: GitHub ancjs77-cloud/dronealarm",options:{bullet:true}}],{x:0.45,y:3.95,w:5.0,h:1.25,fontSize:10.5,color:C.background1,valign:"top",isTextBox:true});
const eff=[["경보 전파","무전 순차 전달 → 전 단말 동시"],["행동 표준화","역할·단계별 체크리스트"],["안전 확보","이글루 자동 안내·Close/Open 관리"],["평가·개선","완료 시간 기록, 보고서 자동화"]];
eff.forEach(([t,d],i)=>{ const y=1.1+i*0.78; card(s,5.75,y,3.8,0.68,"effect "+(i+1));
  s.addText(t,{x:5.88,y,w:1.35,h:0.68,fontSize:13,bold:true,color:C.accent5,valign:"middle",isTextBox:true});
  s.addText(d,{x:7.2,y,w:2.3,h:0.68,fontSize:10.5,color:C.background1,valign:"middle",isTextBox:true}); });
s.addText("향후: 실제 탐지 레이더 연동 · 서버(Supabase) 실시간 동기화 · AI 보고서",{x:5.75,y:4.32,w:3.8,h:0.75,fontSize:10.5,color:C.accent2,bold:true,valign:"middle",isTextBox:true});
s.addNotes("PC 하나로 상황실과 휴대폰 화면을 함께 시연. 기대효과 4가지와 향후 연동 계획.");
await pres.writeFile({fileName:R+"/tools/out/드론경보_체계소개.pptx"}); await applyTheme(R+"/tools/out/드론경보_체계소개.pptx",THEME); console.log("ok");
})();
