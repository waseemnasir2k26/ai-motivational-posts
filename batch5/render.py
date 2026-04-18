"""Render 6 quote cards to PNGs via headless Chromium. 1080x1350 IG/LinkedIn-friendly."""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
HTML = (ROOT / "WASEEM-QUOTES-BATCH5.html").as_uri()
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

CARDS = [
    ("card-1", "waseem-batch5-01-tweet.png"),
    ("card-2", "waseem-batch5-02-terminal.png"),
    ("card-3", "waseem-batch5-03-poster.png"),
    ("card-4", "waseem-batch5-04-serif.png"),
    ("card-5", "waseem-batch5-05-xdark.png"),
    ("card-6", "waseem-batch5-06-stats.png"),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1400, "height": 1600}, device_scale_factor=2)
        page = await ctx.new_page()
        await page.goto(HTML, wait_until="networkidle")
        await page.wait_for_function("window.WASEEM_PHOTO && document.fonts.ready")
        # Ensure all <img> loaded
        await page.wait_for_function(
            "[...document.querySelectorAll('img')].every(i => i.complete && i.naturalWidth > 0)"
        )
        # Unscale every card-inner so they render at full 1080x1350
        await page.evaluate(
            "document.querySelectorAll('.card-inner').forEach(n => { n.style.transform='scale(1)'; n.style.width='1080px'; n.style.height='1350px'; })"
        )
        # Give fonts + layout a tick
        await page.wait_for_timeout(500)

        for card_id, filename in CARDS:
            el = await page.query_selector(f"#{card_id}")
            if not el:
                print(f"MISS: {card_id}")
                continue
            # Screenshot the 1080x1350 inner node (scale=2 from device_scale_factor → effective 2160x2700)
            out = OUT / filename
            await el.screenshot(path=str(out), omit_background=False)
            print(f"OK  {filename}  ({out.stat().st_size // 1024} KB)")

        await browser.close()

asyncio.run(main())
