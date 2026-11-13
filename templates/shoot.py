# usage: python3 shoot.py slides_current.html OUTDIR  -> OUTDIR/slide_1.png ... slide_7.png
import asyncio, sys, os
from playwright.async_api import async_playwright
html, out = os.path.abspath(sys.argv[1]), sys.argv[2]
os.makedirs(out, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://' + html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
        for i, el in enumerate(await pg.query_selector_all('section.slide')):
            await el.screenshot(path=os.path.join(out, f'slide_{i+1}.png'))
        await b.close()
asyncio.run(main())
