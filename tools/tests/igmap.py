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
        await pg.goto(APP); await pg.wait_for_timeout(400)
        await pg.fill("#pin","1234"); await pg.click("#pinGo"); await pg.wait_for_timeout(1200)
        await pg.locator("#igroom").screenshot(path="igmap_board.png")
        await pg.evaluate("location.hash='#/room'"); await pg.wait_for_timeout(1200)
        await pg.locator("#igroom").screenshot(path="igmap_room.png")
        print(errs); await b.close()
asyncio.run(main())
