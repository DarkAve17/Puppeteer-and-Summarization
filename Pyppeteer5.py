import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=False)
    context = await browser.createIncognitoBrowserContext()

    page = await context.newPage()
    await page.goto("http://localhost:8000/Search_Result.html")

    # Wait for sponsored element to load (adjust timeout if needed)
    await page.waitForSelector('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe', timeout=10000)

    # Get sponsored element
    sponsored_elements = await page.querySelectorAll('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe')

    # Extract links within sponsored element
    sponsored_links = []
    sponsored_elements = await page.querySelectorAll('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe')

    filename = input(str("Name of new file: "))
    
    
    for element in sponsored_elements:
        for link in await element.querySelectorAll('a.sVXRqc'):
            href = await link.getProperty('href')
            href_str = await href.jsonValue()
            sponsored_links.append(href_str)
            print(f"Found sponsored link: {href_str}")

    await browser.close()

try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")

