import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import asyncio, time, sys
from playwright.async_api import async_playwright
URL=APP
W,H=int(sys.argv[1]),int(sys.argv[2])
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}), args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width":W,"height":H})
        pg = await ctx.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        print("기본 화면:", await pg.evaluate("location.hash"))
        await pg.fill("#pin","1234"); await pg.click("#pinGo"); await pg.wait_for_timeout(900)
        print("휴대폰 수:", await pg.locator(".phone").count(), await pg.evaluate("[...document.querySelectorAll('.plabel')].map(e=>e.textContent)"))
        print("폰 크기:", await pg.evaluate("[...document.querySelectorAll('.phone')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.x),Math.round(r.width),Math.round(r.height)]})"))
        await pg.screenshot(path=OUT+f"b3_idle_{W}.png")
        await pg.click("[data-room=start]"); t0=time.time(); seen=set()
        while time.time()-t0<90:
            await pg.wait_for_timeout(500)
            lv=await pg.evaluate("()=>active()?active().level:0")
            if lv not in seen: seen.add(lv); print(" 단계",lv,"t=",round(time.time()-t0,1), await pg.evaluate("()=>active()&&active().track&&[active().track.distance_m,active().track.center_m]"))
            if lv>=3: break
        await pg.wait_for_timeout(1800)
        for r in ["pilot","maintenance","security"]:
            if await pg.locator(f"[data-bpop={r}]").count(): await pg.locator(f"[data-bpop={r}]").click(timeout=3000); await pg.wait_for_timeout(200)
        await pg.screenshot(path=OUT+f"b3_l3_{W}.png")
        await pg.locator(".scr[data-role=pilot] [data-igarrive]").click(timeout=3000); await pg.wait_for_timeout(300)
        await pg.locator(".scr[data-role=maintenance] [data-igenter]").click(timeout=3000); await pg.wait_for_timeout(300)
        await pg.locator(".scr[data-role=maintenance] [data-igclose]").click(timeout=3000); await pg.wait_for_timeout(500)
        await pg.click("[data-room=clear]"); await pg.locator(".modal [data-c='1']").click(); await pg.wait_for_timeout(1500)
        for r in ["pilot","maintenance","security"]:
            if await pg.locator(f"[data-bpop={r}]").count(): await pg.locator(f"[data-bpop={r}]").click(timeout=3000); await pg.wait_for_timeout(150)
        await pg.wait_for_timeout(6000)
        print("Open 전 자동 복귀 안 됨:", await pg.evaluate("()=>!S.resetAt"), "| 안내:", (await pg.inner_text(".resetnote")).replace("\n"," "))
        await pg.locator(".scr[data-role=maintenance] [data-igopen]").click(timeout=3000); await pg.wait_for_timeout(2000)
        print("카운트다운:", (await pg.inner_text(".resetnote")).replace("\n"," "))
        await pg.screenshot(path=OUT+f"b3_open_{W}.png")
        await pg.wait_for_timeout(4500)
        st=await pg.evaluate("()=>({reset:!!S.resetAt, active:!!active(), sim:S.sim, closed:S.igloos.filter(g=>g.closed||g.aircraftBy||g.assignedTo||g.evac.length).length, start:!!document.querySelector('[data-room=start]'), note:!!document.querySelector('.resetnote')})")
        print("복귀 후:", st)
        print("폰 화면:", [ (await pg.inner_text(f".scr[data-role={r}]"))[:40].replace("\n"," | ") for r in ["pilot","maintenance","security"]])
        await pg.screenshot(path=OUT+f"b3_reset_{W}.png")
        # 두 번째 시연도 가능?
        await pg.click("[data-room=start]"); await pg.wait_for_timeout(1500); print("재시작 가능:", await pg.evaluate("()=>!!active()"))
        await pg.click("[data-room=reset]"); await pg.wait_for_timeout(800); print("처음 상태로 버튼:", await pg.evaluate("()=>!active()&&!S.sim"))
        print("errors:", errs)
        await b.close()
asyncio.run(main())
