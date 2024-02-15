import asyncio
from pyppeteer import launch

async def main():
    searchfor = input("Enter Keyword to search: ")  # Uncomment if using search functionality
    filename = "Search_" + searchfor + ".CSV"

    try:
        browser = await launch()
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()

        await page.goto("http://www.google.com")
        search_bar = await page.querySelector('input[name="q"]')
        await search_bar.type(searchfor)
        await page.keyboard.press("Enter")
        await page.waitForNavigation()


        # Combined selector (adjusted):
        selector = "div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe"

        # Wait for any matching element to appear (adjust timeout if needed):
        await page.waitForSelector(selector, timeout=10000)

        # List to store all sponsor links:
        all_sponsored_links = []

        # Find all sponsor elements using querySelectorAll:
        sponsored_elements = await page.querySelectorAll(selector)

        # Process each element:
        for sponsored_element in sponsored_elements:
            # Two selectors for potentially different link classes:
            link_selectors = ["a.cz3goc.BmP5tf", "a.sVXRqc"]

            for link_selector in link_selectors:
                sponsored_links = await sponsored_element.querySelectorAll(link_selector)

                # Collect links from this element with current selector:
                for link in sponsored_links:
                    href = await link.getProperty('href')
                    href_str = await href.jsonValue()
                    all_sponsored_links.append(href_str)
                    print(f"Found sponsored link: {href_str}")

            # Optional CSV writing (adapt as needed):
            with open(filename, 'w') as f:
                f.write('Sponsored Link\n')
                for link in all_sponsored_links:
                    f.write(f"{link}\n")

        await browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())
