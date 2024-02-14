import asyncio
from pyppeteer import launch

async def main():
    searchfor = input(str("Enter Keyword to search: "))
    
    browser = await launch(headless=True)
    context = await browser.createIncognitoBrowserContext()
    filename = "Search_"+searchfor
    page = await context.newPage()
    await page.goto("https://www.google.com")
    search_bar = await page.querySelector('input[name="q"]')
    await search_bar.type(searchfor)
    await page.keyboard.press("Enter")
    await page.waitForNavigation()

    # Wait for sponsored element to load (adjust timeout if needed)
    await page.waitForSelector('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe', timeout=10000)

    # Get sponsored element
    sponsored_elements = await page.querySelectorAll('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe')

    # Extract links within sponsored element
    sponsored_links = []
    sponsored_elements = await page.querySelectorAll('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe')

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

