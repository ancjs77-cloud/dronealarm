import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}),args=["--no-sandbox","--allow-file-access-from-files"])
        pg=await b.new_page(); await pg.goto("file://"+KIT+"manual/manual.html"); await pg.wait_for_timeout(1500)
        await pg.pdf(path=OUT+"드론경보_역할별_사용매뉴얼.pdf", width="297mm", height="210mm", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
