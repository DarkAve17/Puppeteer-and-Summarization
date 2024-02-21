import asyncio
from pyppeteer import launch
import re
import time
import csv

async def main():          
    browser = await launch(headless=False)#, args=['--start-maximized'])    
    context = await browser.createIncognitoBrowserContext() 
    page = await context.newPage()
    await page.goto("http://127.0.0.1:5500/HTML%20Files/Best%20Antivirus%202024.html")
    await page.setZoom(245)
    try:
        contact_buttons = await page.xpath("//button[contains(., 'Contact')]")
        if contact_buttons:
        # Click the first found button
            await contact_buttons[0].click()
            await page.waitForNavigation()  # Wait for button click to load new content
        await page.screenshot({'path': 'contTest.png'})
    except Exception as e:
        print(f"Error checking or clicking contact button: {e}")
    await browser.close()
        
asyncio.run(main())