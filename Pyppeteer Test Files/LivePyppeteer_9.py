import asyncio
from pyppeteer import launch

async def main():
    searchfor = input("Enter Keyword to search: ")
    filename = "Search_" + searchfor + ".CSV"

    try:
        browser = await launch()
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()

        await page.goto("http://127.0.0.1:5500/antivirus_software.html")
        #search_bar = await page.querySelector('input[name="q"]')
        #await search_bar.type(searchfor)
        #await page.keyboard.press("Enter")
        #await page.waitForNavigation()

        # Combined selector for efficiency:
        selector = "div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe"

        # Wait for either selector to appear (adjust timeout if needed):
        await page.waitForSelector(selector, timeout=10000)

        # Get the found element:
        sponsored_element = await page.querySelector(selector)

        if sponsored_element:
            # Element found, proceed with extraction:
            sponsored_links = await sponsored_element.querySelectorAll('a.cz3goc.BmP5tf')
            for link in sponsored_links:
                href = await link.getProperty('href')
                href_str = await href.jsonValue()
                print(f"Found sponsored link: {href_str}")
                # Add link to your CSV or perform other actions as needed
        else:
            print("No sponsored element found.")

        await browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())
