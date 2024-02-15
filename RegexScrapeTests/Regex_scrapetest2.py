import asyncio
from pyppeteer import launch
import re

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:5500/HTML%20Files/My%20Care.html')  # Replace with your HTML file path

    # Extract all text content
    html_content = await page.content()

    # Search for email addresses using Regex
    phone_numbers = re.findall(r"((\+91)|(\+91 ))?(\d{3}[ -]?\d{3}[ -]?\d{4})", html_content)
    print("Found Phone Numbers:", phone_numbers) 

    await browser.close()

asyncio.run(main())
