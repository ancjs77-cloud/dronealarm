import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import asyncio, json
from playwright.async_api import async_playwright
ROLES=["pilot","controller","maintenance","security"]
OUT=OUT+"shots/"; os.makedirs(OUT,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}),args=["--no-sandbox"])
        ctx=await b.new_context(viewport={"width":2000,"height":1120},device_scale_factor=2)
        pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(APP); await pg.wait_for_timeout(400)
        await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(400)
        await pg.evaluate('BOARD_MEMBERS.splice(1,0,["controller","관제1"]); BOARD_ROLES.splice(1,0,"controller"); boardIds=null;')
        await pg.screenshot(path=OUT+"room_pin.png")
        await pg.fill("#pin","1234"); await pg.click("#pinGo"); await pg.wait_for_timeout(1500)
        n={r:0 for r in ROLES}; log={r:[] for r in ROLES}
        async def shot(r,key):
            n[r]+=1; f=f"{r}_{n[r]:02d}_{key}.png"; await pg.locator(f".pcol:has(.scr[data-role={r}]) .phone").screenshot(path=OUT+f); log[r].append([f,key])
        async def shot_all(key, roles=ROLES):
            for r in roles: await shot(r,key)
        async def closepop(roles=ROLES):
            for r in roles:
                if await pg.locator(f"[data-bpop={r}]").count(): await pg.locator(f"[data-bpop={r}]").click(); await pg.wait_for_timeout(150)
        async def check(r):
            while await pg.locator(f".scr[data-role={r}] .chk:not(.on)").count():
                await pg.locator(f".scr[data-role={r}] .chk:not(.on)").first.click(); await pg.wait_for_timeout(120)
        async def ack(r):
            b2=pg.locator(f".scr[data-role={r}] [data-ack]:not([disabled])")
            if await b2.count(): await b2.click(); await pg.wait_for_timeout(400)
        async def scroll(r,y):
            await pg.evaluate(f"document.querySelector('.scr[data-role={r}]').scrollTop={y}"); await pg.wait_for_timeout(250)
        async def wait_level(l):
            await pg.click("[data-room=pause]"); await pg.wait_for_function(f"()=>active()&&active().level>={l}",timeout=120000); await pg.click("[data-room=pause]"); await pg.wait_for_timeout(1200)
        await shot_all("idle")
        await pg.screenshot(path=OUT+"room_board_idle.png")
        await pg.click("[data-room=start]"); await pg.wait_for_timeout(300); await pg.click("[data-room=pause]")
        await wait_level(1)
        await shot_all("l1_popup"); await pg.screenshot(path=OUT+"room_board_l1.png")
        await closepop(); await shot_all("l1_list")
        for r in ROLES: await check(r)
        await shot_all("l1_checked")
        for r in ROLES: await ack(r)
        await pg.wait_for_timeout(800)
        for r in ROLES: await scroll(r,10000)
        await shot_all("l1_done_map")
        await wait_level(2)
        await shot_all("l2_popup"); await closepop(); await pg.wait_for_timeout(500)
        await shot_all("l2_map")
        for r in ROLES:
            await check(r); await scroll(r,10000)
        await shot_all("l2_checked")
        for r in ROLES: await ack(r)
        await wait_level(3)
        await shot_all("l3_popup"); await pg.screenshot(path=OUT+"room_board_l3.png"); await closepop(); await pg.wait_for_timeout(800)
        await shot_all("l3_screen")
        await pg.locator(".scr[data-role=pilot] [data-igarrive]").click(); await pg.wait_for_timeout(500); await shot("pilot","l3_arrived")
        await pg.locator(".scr[data-role=maintenance] [data-igenter]").click(); await pg.wait_for_timeout(500); await shot("maintenance","l3_entered")
        await pg.locator(".scr[data-role=maintenance] [data-igclose]").click(); await pg.wait_for_timeout(600); await shot("maintenance","l3_closed")
        for r in ROLES:
            await check(r); await scroll(r,10000)
        await shot_all("l3_checked")
        for r in ROLES: await ack(r)
        await pg.wait_for_timeout(600); await pg.screenshot(path=OUT+"room_board_l3done.png")
        await wait_level(4)
        await shot_all("l4_popup"); await closepop(); await pg.wait_for_timeout(500); await shot_all("l4_screen")
        await pg.screenshot(path=OUT+"room_board_l4.png")
        await pg.click("[data-room=pause]")
        await pg.click("[data-room=clear]"); await pg.locator(".modal [data-c='1']").click(); await pg.wait_for_timeout(1500)
        await shot_all("clear_popup"); await pg.screenshot(path=OUT+"room_board_clear.png"); await closepop(); await pg.wait_for_timeout(500)
        await shot("maintenance","open_card")
        await pg.locator(".scr[data-role=maintenance] [data-igopen]").first.click(); await pg.wait_for_timeout(1800)
        await pg.screenshot(path=OUT+"room_board_reset_cd.png")
        await pg.wait_for_timeout(6000); await pg.screenshot(path=OUT+"room_board_after.png")
        # room-only page & history
        await pg.evaluate("location.hash='#/history'"); await pg.wait_for_timeout(1200); await pg.screenshot(path=OUT+"room_history.png")
        if await pg.locator("[data-h]").count(): await pg.locator("[data-h]").first.click(); await pg.wait_for_timeout(1200); await pg.screenshot(path=OUT+"room_report.png", full_page=True)
        json.dump(log,open(OUT+"log.json","w"),ensure_ascii=False,indent=1)
        print(errs, {k:len(v) for k,v in log.items()}); await b.close()
asyncio.run(main())
# 문서용 잘라낸 이미지
from PIL import Image
Image.open(OUT+"room_report.png").crop((600,80,3400,2050)).save(OUT+"room_report_c.png")
Image.open(OUT+"room_board_l3done.png").crop((0,0,1040,2240)).crop((45,112,920,992)).save(OUT+"room_map_l3.png")
