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

        # List to store all collected sponsor links:
        all_sponsored_links = []

        # Process pages:
        while True:
            # Combined selector (adjusted):
            selector = "div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe"
            sponsored_elements = await page.querySelectorAll(selector)

            # Extract links from current page:
            for sponsored_element in sponsored_elements:
                #Your link extraction logic using link_selectors as before
                #Two selectors for potentially different link classes:
                link_selectors = ["a.cz3goc.BmP5tf", "a.sVXRqc"]

                for link_selector in link_selectors:
                    sponsored_links = await sponsored_element.querySelectorAll(link_selector)
                # Collect links from this element:
                    for link in sponsored_links:
                        href = await link.getProperty('href')
                        href_str = await href.jsonValue()
                        all_sponsored_links.append(href_str)
                        print(f"Found sponsored link: {href_str}")

            # Function to click "Next" or "Show more" button (if exists)
            async def click_next_button():
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
                    return True  # Indicate button was clicked
                else:
                    return False  # No button found

            # Attempt to click "Next" or "Show more" button, break if not found
            button_clicked = await click_next_button()
            if not button_clicked:
                break  # No more buttons, exit loop

            # Wait for new sponsored elements after button click:
            await page.waitForSelector(selector, timeout=10000)  # Adjust timeout if needed

    except Exception as e:
        # Other errors (optional: handle specific errors differently)
        print(f"An error occurred: {e}")
        # Optionally, write collected links here if desired

    # Write collected links to CSV file:
    with open(filename, 'w') as f:
        f.write('Sponsored Link\n')
        for link in all_sponsored_links:
            f.write(f"{link}\n")

    await browser.close()

asyncio.run(main())
