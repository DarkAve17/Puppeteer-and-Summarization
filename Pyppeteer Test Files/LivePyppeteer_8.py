import asyncio
from pyppeteer import launch
import time

async def main():
    searchfor = input("Enter Keyword to search: ")
    filename = "Search_" + searchfor + ".CSV"  # Include search keyword in the filename

    try:
        browser = await launch()
        
        context = await browser.createIncognitoBrowserContext()

        page = await context.newPage()
        await page.goto("http://www.google.com") #http://127.0.0.1:5500/antivirus_software.html #http://www.google.com
        search_bar = await page.querySelector('input[name="q"]')
        await search_bar.type(searchfor)
        await page.keyboard.press("Enter")
        await page.waitForNavigation()
        

        # Wait for sponsored element to load (adjust timeout if needed)
        await page.waitForSelector('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe', timeout=10000)
        await page.waitForSelector('div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe', timeout = 10000)

        # Get sponsored elements
        sponsored_elements = await page.querySelectorAll('div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe')
        sponsored_elements = await page.querySelectorAll('div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe')

        print(sponsored_elements)
        time.sleep(3)

        # Extract links within sponsored elements
        sponsored_links = []
        for element in sponsored_elements:
            for link in await element.querySelectorAll('a.cz3goc.BmP5tf'):
                href = await link.getProperty('href')
                href_str = await href.jsonValue()
                sponsored_links.append(href_str)
                print(f"Found sponsored link: {href_str}")

            
        #page_content = await page.content()
        #with open(filename, 'w', ) as f:
             #f.write(page_content)

        await browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())

