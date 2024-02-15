import asyncio
from pyppeteer import launch

# Add a counter to track position



async def main():
    browser = await launch(headless = False)
    context = await browser.createIncognitoBrowserContext()
    #searchfor = input("Best Hair Salon Pune")
    searchfor = input(str("Enter Keyword to search: "))
    page = await context.newPage()
    await page.goto("https://www.google.com")

    search_bar = await page.querySelector('input[name="q"]')
    await search_bar.type(searchfor)
    await page.keyboard.press("Enter")
    await page.waitForNavigation()
    scroll_position = 0
    captured_links = []
   
    sponsored_links = []
    
    
    while True:
        # Scroll down
        await page.evaluate(f'window.scrollBy(0, {scroll_position})')
        await page.waitForTimeout(1000)

        # Get viewport height
        viewport_height = await page.evaluate('return window.innerHeight')

        # Capture links within viewport
        for i in range(1, 4):
            link = await page.querySelector(f'.g:nth-child({i}) a')
            if link:
                href = await link.getProperty('href')
                href_str = await href.jsonValue()
                if "www.google.com/search" not in href_str:
                    captured_links.append(href_str)
                    print(f"Found sponsored link: {href_str}")
    
        new_links = len(captured_links) - len(sponsored_links)
        if new_links == 0:
            break

        # Update scroll position for next iteration
        scroll_position += viewport_height
        browser.close()
    #for i in range(1, 20000):
    #    # Modify selector to target specific elements within sponsored area
    #    link = await page.querySelector(f'.g:nth-child({i}) a')
    #    if link:
    #        href = await link.getProperty('href')
    #        href_str = await href.jsonValue()
    #        if "www.google.com/search" not in href_str:
    #            sponsored_links.append(href_str)
    #            sponsored_position += 1
    #            print(f"Found sponsored link {sponsored_position}: {href_str}")

    
    

try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")
