import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import asyncio
from playwright.async_api import async_playwright
async def done_level(pg):
    for r in ["pilot","maintenance","security"]:
        if await pg.locator(f"[data-bpop={r}]").count(): await pg.locator(f"[data-bpop={r}]").click(); await pg.wait_for_timeout(150)
    for r in ["pilot","maintenance","security"]:
        while await pg.locator(f".scr[data-role={r}] .chk:not(.on)").count():
            await pg.locator(f".scr[data-role={r}] .chk:not(.on)").first.click(); await pg.wait_for_timeout(120)
        b2=pg.locator(f".scr[data-role={r}] [data-ack]:not([disabled])")
        if await b2.count(): await b2.click(); await pg.wait_for_timeout(300)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}),args=["--no-sandbox"])
        pg=await (await b.new_context(viewport={"width":1920,"height":1080})).new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(APP); await pg.wait_for_timeout(400)
        await pg.fill("#pin","1234"); await pg.click("#pinGo"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path="pm_idle.png")
        await pg.click("[data-room=start]")
        await pg.wait_for_function("()=>active()&&active().level>=2",timeout=90000); await pg.click("[data-room=pause]"); await pg.wait_for_timeout(500)
        await done_level(pg); await pg.wait_for_timeout(1200)
        await pg.screenshot(path="pm_l2done.png")
        await pg.click("[data-room=pause]")
        await pg.wait_for_function("()=>active()&&active().level>=3",timeout=90000); await pg.wait_for_timeout(3000); await pg.click("[data-room=pause]"); await pg.wait_for_timeout(500)
        await done_level(pg); await pg.wait_for_timeout(1200)
        await pg.screenshot(path="pm_l3done.png")
        print(errs); await b.close()
asyncio.run(main())
