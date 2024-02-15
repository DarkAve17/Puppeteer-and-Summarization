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
  phone_numbers = re.findall(r"((\+91)|(\+91 ))?(.*?\d{3}[ -]?\d{3}[ -]?\d{4})", html_content)

  # Create a set to store unique phone numbers and their additional parts
  unique_phone_numbers = set()

  # Iterate through each phone number and add unique ones to the set
  for number in phone_numbers:
    # Join the individual parts to create a unique identifier
    unique_identifier = "".join(number)
    # If the identifier is not already in the set, add it
    if unique_identifier not in unique_phone_numbers:
      unique_phone_numbers.add(unique_identifier)

  # Convert the set back to a list and print the unique phone numbers
  unique_phone_numbers_list = list(unique_phone_numbers)
  print("Unique Phone Numbers:", unique_phone_numbers_list)

  cleaned_strings = []
  for string in unique_phone_numbers_list:
    # Use a regular expression to match only digits and '+'
    cleaned_string = re.sub(r"[^\d+]", "", string)
    cleaned_strings.append(cleaned_string)  
  
  
  print("Phone Numbers:", cleaned_strings)
  await browser.close()

asyncio.run(main())
