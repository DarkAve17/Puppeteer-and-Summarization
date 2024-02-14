import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    searchfor = "best hair dresser pune"

    page = await context.newPage()
    #await page.goto("https://www.google.com")
    await page.goto("file:Search_Result.html")
    #search_bar = await page.querySelector('input[name="q"]')
    #await search_bar.type(searchfor)
    #await page.keyboard.press("Enter")
    #await page.waitForNavigation()

    #next_button = await page.querySelector('.nBDE1b.G5eFlf')  # Adjust if element class changes

    sponsored_links = []

    #while next_button:
    for i in range(1, 4):
        link = await page.querySelector(f'.g:nth-child({i}) a')
        if link:
            href = await link.getProperty('href')
            href_str = await href.jsonValue()
            if "www.google.com/search" not in href_str:
                sponsored_links.append(href_str)
                print(f"Found sponsored link: {href_str}")

    #await page.waitFor({3000})  # Adjust wait time if needed
    #await next_button.click()
    #await page.waitForNavigation()
#
    #next_button = await page.querySelector('a[aria-label="Next page"]')  # Adjust if element structure changes

    await browser.close()

try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")
