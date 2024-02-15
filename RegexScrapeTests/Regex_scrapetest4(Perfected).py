import asyncio
from pyppeteer import launch
import re

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://sanctushealthcare.com/contact/') #http://127.0.0.1:5500/HTML%20Files/My%20Care.html

    html_content = await page.content()

    phone_numbers = re.findall(r"(\+\d{2})[- ]?(\d{10})", html_content)

    print()
    print(f"Phone Numbers = {phone_numbers}")
    print()
    unique_phone_numbers = set()
    for number in phone_numbers:
        # Extract only the phone number part from the tuple
        phone_number_string = number[0] + number[1]

        # Apply the regular expression substitution on the extracted string
        cleaned_number = re.sub(r"[^\d+\s]", "", phone_number_string)

        # Ensure unique identifier is based on cleaned number
        unique_identifier = cleaned_number
        if unique_identifier not in unique_phone_numbers:
            unique_phone_numbers.add(unique_identifier)

    unique_phone_numbers_list = list(unique_phone_numbers)
    print("Unique Phone Numbers:", unique_phone_numbers_list)
    print()
    print()
    print()

    cleaned_strings = unique_phone_numbers_list

    print("Phone Numbers:", cleaned_strings)
    await browser.close()

asyncio.run(main())
