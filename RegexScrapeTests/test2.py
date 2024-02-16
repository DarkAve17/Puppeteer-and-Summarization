import asyncio
from pyppeteer import launch
import re

async def main():
  # Replace with the actual URL you want to scan
  url = "https://sanctushealthcare.com/contact/"

  # Launch Puppeteer and open the page
  browser = await launch()
  page = await browser.newPage()
  await page.goto(url,timeout=60000)

  # Extract the entire page content
  webpage = await page.content()

  # Apply the regex and print matches
  matches = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", webpage)
  print(f"Found {len(matches)} matches:")
  for match in matches:
    print(match)

  # Close the browser
  await browser.close()

asyncio.run(main())
