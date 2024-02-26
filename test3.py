import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

async def click_next_button(page):
    button_found = False

    try:
        # Get all footer buttons with the specified classes
        footer_buttons = await page.querySelectorAll("footer a.nBDE1b.G5eFlf")

        if footer_buttons:
            # Iterate through each footer button to find the "Next" button
            for footer_button in footer_buttons:
                text = await page.evaluate('(element) => element.textContent', footer_button)
                print(text)
                if "Next" in text or ">" in text:
                    # Click the button
                    await footer_button.click()
                    print("Next button found and clicked in the footer.")
                    button_found = True
                    await asyncio.sleep(15)
                    break  # Exit the loop once the button is found
            
            if not button_found:
                print("Button found in the footer but does not contain 'Next' or '>'.")
        else:
            print("Button not found in the footer.")
        
    except TimeoutError:
        print("Timeout occurred while searching for buttons in the footer.")
    
    # If no button found, check for new content:
    if not button_found:
        #Get initial document height:
        initial_height = await page.evaluate("document.body.scrollHeight")

        # Scroll down and wait for potential content load:
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await asyncio.sleep(2)  # Adjust wait time if needed

        # Check if document height changed:
        final_height = await page.evaluate("document.body.scrollHeight")
        if final_height > initial_height:
            button_found = True  # Consider new content loaded

    return button_found


async def main():
    browser = await launch(headless=False, defaultViewport=None, args=['--window-size=1920,1080'])
    page = await browser.newPage()
    
    url = "http://127.0.0.1:5500/HTML%20Files/NExtButtonPressPLEASE.html"
    
    # Navigate to the specified website
    await page.goto(url)
    
    while await click_next_button(page):
        pass
    
    await browser.close()

# Run the main function
asyncio.run(main())
