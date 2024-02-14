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

        # List to store all sponsor links:
        all_sponsored_links = []

        # Process pages:
        while True:
            # Combined selector (adjusted):
            selector = "div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe"
            sponsored_elements = await page.querySelectorAll(selector)

            # Extract links from current page:
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

            # Find and click "Next" or "Show more" button (if exists):
            button_found = False
            for button_selectors in [
                ["div.Gx5Zad.xpd.EtOod.pkphOe.BmP5tf a.nBDE1b.G5eFlf", ":contains('Next')"],  # Next button
                ["div.GNJvt.ipz2Oe > span.kQdGHd > span.OTvAmd.z1asCe.QFl0Ff", ":contains('More results')"],  # Show more button
            ]:
                for selector in button_selectors:
                    button = await page.querySelector(selector)
                    if button:
                        await button.click()
                        button_found = True
                        break
                if button_found:
                    break  # One of the buttons was found, proceed to next page

            if not button_found:
                break  # No more "Next" or "Show more" buttons, exit loop

            # Wait for new sponsored elements to appear:
            await page.waitForSelector(selector, timeout=10000)

    except Exception as e:
        print(f"An error occurred: {e}")

    await browser.close()

asyncio.run(main())
