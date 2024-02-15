import re
import asyncio
from pyppeteer import launch


async def extract_phone_numbers(url):
  
  browser = await launch()
  page = await browser.newPage()
  await page.goto(r'http://127.0.0.1:5500/HTML%20Files/My%20Care.html')
  html_content = await page.content()
  await browser.close()
  
  phone_numbers = re.findall(r"(?:\+91)?(\d{3}[ -]?\d{3}[ -]?\d{4})", html_content)
  return phone_numbers

# Example usage
#html_file = r"C:\Users\mridu\Documents\GitHub Repos\Puppeteer and Summarization\HTML Files\My Care.html"
#extracted_numbers = extract_phone_numbers(html_file)

#print("Extracted phone numbers:")
#for number in extracted_numbers:
#  print(number)


asyncio.run(extract_phone_numbers("http://localhost:8000/your_file.html"))
