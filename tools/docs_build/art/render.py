import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..",".."))
APP="file://"+REPO+"/web/index.html"
OUT=os.path.join(REPO,"tools","out")+"/"; os.makedirs(OUT,exist_ok=True)
KIT=os.path.join(REPO,"tools","docs_build")+"/"
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}),args=["--no-sandbox"])
        for name,w,h in [("bg_16x9",1920,1080),("bg_a4",1754,1240)]:
            pg=await b.new_page(viewport={"width":w,"height":h},device_scale_factor=1.5)
            await pg.goto("file://"+KIT+"art/bg.html"); await pg.wait_for_timeout(400); await pg.screenshot(path=f"{name}.png"); await pg.close()
        await b.close()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
asyncio.run(main())
from PIL import Image, ImageEnhance, ImageFilter
for n in ['bg_16x9','bg_a4']:
    im=Image.open(n+'.png').convert('RGB'); im.save(n+'.jpg',quality=88)
    ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(2))).enhance(.45).save(n+'_dim.jpg',quality=85)
