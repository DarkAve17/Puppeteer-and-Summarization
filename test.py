import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

async def main():
    # Launch the browser
    browser = await launch(headless=False, defaultViewport=None, args=['--window-size=1920,1080'])
    
    # Create a new page
    page = await browser.newPage()
    
    url = "http://127.0.0.1:5500/HTML%20Files/NExtButtonPressPLEASE.html"
    
    # Navigate to the specified website
    await page.goto(url)
    
    try:
        # Get the footer button
        footer_button = await page.querySelector("footer a.nBDE1b.G5eFlf")
        if footer_button:
            text = await page.evaluate('(element) => element.textContent', footer_button)
            print(text)
            if "Next" in text:
                # Click the button
                await footer_button.click()
                print("Next button found and clicked in the footer.")
            else:
                print("Button found in the footer but does not contain 'Next'.")
        else:
            print("Button not found in the footer.")
    except TimeoutError:
        print("Timeout occurred while searching for buttons in the footer.")
    
    await asyncio.sleep(5)
    # Close the browser
    await browser.close()

# Run the asyncio event loop
asyncio.run(main())
