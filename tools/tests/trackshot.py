import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}),args=["--no-sandbox"])
        pg=await (await b.new_context(viewport={"width":1920,"height":1080})).new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto(APP+"#/room"); await pg.wait_for_timeout(400)
        await pg.fill("#pin","1234"); await pg.click("#pinGo"); await pg.wait_for_timeout(800)
        await pg.evaluate("roomCfg.bearing=300; roomCfg.startKm=12"); await pg.click("[data-room=start]"); await pg.wait_for_timeout(30000)
        await pg.locator("#rings").screenshot(path="track_room.png")
        print(await pg.evaluate("()=>[active().level, active().track, active().alerts.map(a=>a.eta_sec)]"))
        await pg.evaluate("location.hash='#/board'"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path="track_board.png")
        print(errs); await b.close()
asyncio.run(main())
