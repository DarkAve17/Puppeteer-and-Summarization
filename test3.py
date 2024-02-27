import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

async def click_next_button(page):
    button_found = False

    try:
        # Get all footer buttons with the specified classes
        footer_buttons = await page.querySelectorAll("footer button")
        await asyncio.sleep(10)
        for footer_button in footer_buttons:
            text = await page.evaluate('(element) => element.textContent', footer_button)
            print(text)
    
    except TimeoutError:
        print("Timeout occurred while searching for buttons in the footer.")
    
    
    return button_found


async def main():
    browser = await launch(headless=False, defaultViewport=None, args=['--window-size=1920,1080'])
    page = await browser.newPage()
    
    url = "https://www.amd.com/en.html"
    
    # Navigate to the specified website
    await page.goto(url)
    
    while await click_next_button(page):
        pass
    
    await browser.close()

# Run the main function
asyncio.run(main())
