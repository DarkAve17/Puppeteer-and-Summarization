import asyncio
from pyppeteer import launch
import time

async def click_next_button(page):
    button_found = False
    button_selectors = ":text('Next'), :text('Next page'),:text('More results')"
    await page.waitForSelector(button_selectors, visible = True)
    for selector in button_selectors:
        button = await page.querySelector(selector)
        if button:
            await button.click()
            button_found = True
            break
    if button_found:
        return True  # Indicate button was clicked
    else:
        return False


async def main():
    searchfor = input("Enter Keyword to search: ")  
    filename = "Search_" + searchfor + ".CSV"

    try:
        browser = await launch(headless=False)
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()

        await page.goto("http://www.google.com")
        search_bar = await page.querySelector('input[name="q"]')
        await search_bar.type(searchfor)
        await page.keyboard.press("Enter")
        await page.waitForNavigation()
        time.sleep(15)
        # List to store all collected sponsor links:
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
                    # Collect links from this element:
                    for link in sponsored_links:
                        href = await link.getProperty('href')
                        href_str = await href.jsonValue()
                        all_sponsored_links.append(href_str)
                        print(f"Found sponsored link: {href_str}")

            # Click "Next" or "Show more" button (if exists)
            button_clicked = await click_next_button(page)
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
