import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=False)
    context = await browser.createIncognitoBrowserContext()

    page = await context.newPage()
    await page.goto("file:C:\Users\mridu\Documents\GitHub Repos\Puppeteer and Summarization\Search_Result.html")

    # Wait for sponsored element to load (adjust timeout if needed)
    await page.waitForSelector('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe', timeout=10000)

    # Get sponsored element
    sponsored_element = await page.querySelector('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe')

    # Extract links within sponsored element
    sponsored_links = []
    if sponsored_element is not None:
        for link in await sponsored_element.querySelectorAll('a.sVXRqc'):
            href = await link.getProperty('href')
            href_str = await href.jsonValue()
            sponsored_links.append(href_str)
            print(f"Found sponsored link: {href_str}")
    else:
        print("No sponsored element found")

    await browser.close()

try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")

