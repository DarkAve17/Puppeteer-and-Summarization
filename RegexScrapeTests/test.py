import asyncio
from pyppeteer import launch
import re
import os

async def main():
    browser = await launch()
    page = await browser.newPage()
    
    file_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub Repos", "Puppeteer and Summarization", "test.html")
    await page.goto(file_path)
    await page.goto("https://www.lightsnovel.com/content/warlock-of-the-magus-world(1)-584-457042/chapter-289")
    # Combine plain text and href methods
    email_addresses = []

    # 1. Extract from plain text using regex:
    webpage = await page.content()
    plain_text_emails = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", webpage)
    email_addresses.extend(plain_text_emails)

    # 2. Extract from href attributes:
    email_elements = await page.querySelectorAll('.footer-menu-item a[href^="mailto:"]')
    for element in email_elements:
        email_address = await element.get_property('href')
        if "mailto:" in email_address:  # Check for mailto: presence
            email_addresses.append(email_address.replace('mailto:', ''))

    # Print or use extracted emails
    print("Extracted email addresses:")
    for email in set(email_addresses):  # Remove duplicates
        print(email)

    await browser.close()

asyncio.run(main())
