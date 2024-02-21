import asyncio
from pyppeteer import launch
import re
import time
import csv

async def extract_contact_info(page, url):
    """Extracts phone numbers and emails from a given webpage."""
    await page.goto(url)
    webpage = await page.content()
    phone_numbers = re.findall(r"(\+\d{2})[- ]?(\d{10})", webpage)
    email_adresses = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", webpage)

    unique_phone_numbers = set()
    unique_emails = set()

    for number in phone_numbers:
        phone_number_string = number[0] + number[1]
        cleaned_number = re.sub(r"[^\d+\s]", "", phone_number_string)
        unique_identifier = cleaned_number
        unique_phone_numbers.add(unique_identifier)

    for email in email_adresses:
        unique_emails.add(email)

    return unique_phone_numbers, unique_emails

async def main():
    """Main function to search sponsors, extract contact info, and write to CSV."""
    searchfor = input("Enter Keyword to search: ")
    filename = "Details_on_" + searchfor + ".CSV"

    try:
        browser = await launch(headless=False)
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()

        await page.goto("http://www.google.com")
        search_bar = await page.querySelector('input[name="q"]')
        await search_bar.type(searchfor)
        await page.keyboard.press("Enter")
        await page.waitForNavigation()
        time.sleep(15)

        all_sponsored_links = []

        while True:
            selector = "div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe"
            sponsored_elements = await page.querySelectorAll(selector)

            for sponsored_element in sponsored_elements:
                link_selectors = ["a.cz3goc.BmP5tf", "a.sVXRqc"]
                for link_selector in link_selectors:
                    sponsored_links = await sponsored_element.querySelectorAll(link_selector)
                    for link in sponsored_links:
                        href = await link.getProperty('href')
                        href_str = await href.jsonValue()
                        all_sponsored_links.append(href_str)
                        print(f"Found sponsored link: {href_str}")
            await page.evaluate("window.scrollBy(0, 1000)")
            button_clicked = await click_next_button(page)
            if not button_clicked:
                break

            await page.waitForSelector(selector, timeout=10000)

        # Extract contact info for each sponsored link:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Website Link', 'Phone Number', 'Email'])
            id = 1
            for link in all_sponsored_links:
                try:
                    phone_numbers, emails = await extract_contact_info(page, link)
                    writer.writerow([id, link, ', '.join(phone_numbers), ', '.join(emails)])
                    id += 1
                except Exception as e:
                    print(f"Error extracting contact info for {link}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    await browser.close()

async def click_next_button(page):
    button_found = False
    button_selectors = ":text('Next'), :text('Next page'),:text('More results')"
    await page.waitForSelector(button_selectors, visible = True)
    for selector in button_selectors:
        button = await page.querySelector(selector)
        if button:
            await button.click()
            button_found = True
            break
    if button_found:
        return True  # Indicate button was clicked
    else:
        return False

asyncio.run(main())
