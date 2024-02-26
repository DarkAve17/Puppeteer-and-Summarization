import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

async def main():
    # Launch the browser
    browser = await launch(headless=False, defaultViewport=None, args=['--window-size=1920,1080'])
    
    # Create a new page
    page = await browser.newPage()
    
    url = "https://simplicity.com/tools-accessories/buttons/"
    
    # Navigate to the specified website
    await page.goto(url)
    
    # Wait for the main menu toggle button to appear
    try:
        await page.waitForSelector("button.main-menu-toggle", timeout=6000)
        main_menu_toggle_button = await page.querySelector("button.main-menu-toggle")
        await main_menu_toggle_button.click()
        print("Main menu toggle button clicked.")
    except TimeoutError:
        print("Main menu toggle button not found. Skipping...")

    # Wait for a moment for the menu to expand
    await asyncio.sleep(2)  # Adjust the timeout as needed
    
    # Find the submenu toggle button
    submenu_toggle_button = await page.querySelector("button.submenu-toggle")
    if submenu_toggle_button:
        await submenu_toggle_button.click()
        print("Submenu toggle button clicked.")
    else:
        print("Submenu toggle button not found. Skipping...")
    
    # Wait for a moment for the submenu to expand
    await asyncio.sleep(2)  # Adjust the timeout as needed
    
    # Get all buttons on the page again (including those within the submenu)
    buttons = await page.querySelectorAll("button")
    
    # Loop through each button to find one containing the text "Contact"
    for button in buttons:
        text = await page.evaluate('(element) => element.textContent', button)
        print(text)
        if "Accept All Cookies" in text:
            # Click the button
            await button.click()
            break
    else:
        print("Button with text 'Contact' not found.")
    
    await asyncio.sleep(3)
    # Close the browser
    await browser.close()

# Run the asyncio event loop
asyncio.run(main())
