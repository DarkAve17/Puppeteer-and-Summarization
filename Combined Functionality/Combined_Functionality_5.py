import asyncio
from pyppeteer import launch
import re
import time
import csv

async def try_click_contact_button(page):
    """to click on a Button labelled as contact info"""
    try:
        contact_buttons = await page.xpath("//button[contains(., 'Contact')]")

        if contact_buttons:
        # Click the first found button
            await contact_buttons[0].click()
            await page.waitForNavigation()  # Wait for button click to load new content

    except Exception as e:
        print(f"Error checking or clicking contact button: {e}")

async def click_next_button(page):
    """
    Tries to find and click the "Next" button using generic selectors,
    followed by scroll monitoring. Returns True if a button was clicked
    or new content was loaded, False otherwise.
    """

    button_found = False

    # Try with various generic selectors:
    xpath_expressions = [
        "//button[contains(., 'Next')]",
        "//button[contains(., 'Next page')]",
        "//button[contains(., 'More results')]",
    ]

    for xpath_expression in xpath_expressions:
        try:
            button = await page.xpath(xpath_expression)
            if button:
                await button[0].click()  # Click the first found button
                button_found = True
                break
        except Exception as e:
            print(f"Error finding button with XPath '{xpath_expression}': {e}")

    # If no button found, check for new content:
    if not button_found:
        # Get initial scroll position and document height:
        initial_scroll = await page.evaluate("window.scrollY")
        initial_height = await page.evaluate("document.body.scrollHeight")

        # Scroll down and wait for potential content load:
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await asyncio.sleep(2)  # Adjust wait time if needed

        # Check if scroll position or document height changed:
        final_scroll = await page.evaluate("window.scrollY")
        final_height = await page.evaluate("document.body.scrollHeight")

        if final_scroll > initial_scroll or final_height > initial_height:
            button_found = True  # Consider new content loaded

    return button_found


async def extract_contact_info(page, url):
    """Extracts phone numbers and emails from a given webpage."""
    await page.goto(url)
    webpage = await page.content()

    # Search for phone numbers and email addresses:
    phone_numbers = re.findall(r"(\+\d{2})[- ]?(\d{10})", webpage)
    email_adresses = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", webpage)

    # Collect unique phone numbers and emails:
    unique_phone_numbers = set()
    unique_emails = set()

    for number in phone_numbers:
        phone_number_string = number[0] + number[1]
        cleaned_number = re.sub(r"[^\d+\s]", "", phone_number_string)
        unique_identifier = cleaned_number
        unique_phone_numbers.add(unique_identifier)

    for email in email_adresses:
        unique_emails.add(email)

    # Extract contact info after potential button click:
    await try_click_contact_button(page)
    return unique_phone_numbers, unique_emails

async def find_sponsored_links(page):
    """Finds sponsored links on the current page and returns a list of their URLs.

    This function attempts to load more sponsored links by scrolling and,
    if necessary, clicking "Next" buttons using generic selectors.
    """

    all_sponsored_links = []
    consecutive_iterations_without_new_links = 0

    while True:
        # Find sponsored elements based on existing selectors
        selector = "div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe"
        sponsored_elements = await page.querySelectorAll(selector)

        current_sponsored_links = []
        for sponsored_element in sponsored_elements:
            link_selectors = ["a.cz3goc.BmP5tf", "a.sVXRqc"]
            for link_selector in link_selectors:
                sponsored_links = await sponsored_element.querySelectorAll(link_selector)
                for link in sponsored_links:
                    href = await link.getProperty('href')
                    href_str = await href.jsonValue()
                    current_sponsored_links.append(href_str)

        # Check if all current links are already seen
        if set(current_sponsored_links).issubset(set(all_sponsored_links)):
            consecutive_iterations_without_new_links += 1
        else:
            consecutive_iterations_without_new_links = 0

        # Break if no new links for several iterations or limit reached
        if consecutive_iterations_without_new_links >= 3 or len(all_sponsored_links) >= 100:  # Adjust limit as needed
            break

        # Extend all_sponsored_links and try clicking "Next" button
        all_sponsored_links.extend(current_sponsored_links)

        # Scroll down
        try:
            await page.evaluate("window.scrollBy(0, 1000)")
        except:
            pass

        # Try clicking "Next" buttons (adjust selectors as needed)
        next_button_found = await click_next_button(page)
        if next_button_found:
            # Wait for new content to load after clicking next
            await asyncio.sleep(2)  # Adjust wait time as needed

    return all_sponsored_links

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

        sponsored_links = await find_sponsored_links(page)

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Website Link', 'Phone Number', 'Email'])
            id = 1
            for link in sponsored_links:
                try:
                    phone_numbers, emails = await extract_contact_info(page, link)
                    writer.writerow([id, link, ', '.join(phone_numbers), ', '.join(emails)])
                    id += 1
                except Exception as e:
                    print(f"Error extracting contact info for {link}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    await browser.close()



asyncio.run(main())
