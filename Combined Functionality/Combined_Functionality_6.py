import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
import re
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
    button_found = False

    try:
        # Get all footer buttons with the specified classes
        footer_buttons = await page.querySelectorAll("footer a.nBDE1b.G5eFlf")

        if footer_buttons:
            # Iterate through each footer button to find the "Next" button
            for footer_button in footer_buttons:
                text = await page.evaluate('(element) => element.textContent', footer_button)
                print(text)
                if "Next" in text or ">" in text:
                    # Click the button
                    await footer_button.click()
                    print("Next button found and clicked in the footer.")
                    button_found = True
                    await asyncio.sleep(2)
                    break  # Exit the loop once the button is found
            
            if not button_found:
                print("Button found in the footer but does not contain 'Next' or '>'.")
        else:
            print("Button not found in the footer.")
        
    except TimeoutError:
        print("Timeout occurred while searching for buttons in the footer.")
    
    # If no button found, check for new content:
    if not button_found:
        #Get initial document height:
        initial_height = await page.evaluate("document.body.scrollHeight")

        # Scroll down and wait for potential content load:
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await asyncio.sleep(2)  # Adjust wait time if needed

        # Check if document height changed:
        final_height = await page.evaluate("document.body.scrollHeight")
        if final_height > initial_height:
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

async def find_sponsored_links_on_page(page):
    

    sponsored_elements = await page.querySelectorAll("div.vdQmEd.fP1Qef.xpd.EtOod.pkphOe, div.Gx5Zad.fP1Qef.xpd.EtOod.pkphOe")

    current_sponsored_links = []
    for sponsored_element in sponsored_elements:
        link_selectors = ["a.cz3goc.BmP5tf", "a.sVXRqc"]
        for link_selector in link_selectors:
            sponsored_links = await sponsored_element.querySelectorAll(link_selector)
            for link in sponsored_links:
                href = await link.getProperty('href')
                href_str = await href.jsonValue()

                if href_str not in current_sponsored_links:  
                    current_sponsored_links.append(href_str)

    return current_sponsored_links

async def find_all_sponsored_links(page):
    """Iterates through pages and collects sponsored links until no new ones are found.

    This function calls `find_sponsored_links_on_page` on each page, handles scrolling,
    clicks "Next" buttons, and keeps track of seen links to avoid duplicates.
    """

    all_sponsored_links = []
    #consecutive_iterations_without_new_links = 0

    while True:
        current_sponsored_links = await find_sponsored_links_on_page(page)

        # Check if all current links are already seen or limit reached
        if set(current_sponsored_links).issubset(set(all_sponsored_links)) or len(all_sponsored_links) >= 100:
            break

        # Update seen links and try clicking "Next" button
        all_sponsored_links.extend(current_sponsored_links)
        next_button_found = await click_next_button(page)

        if next_button_found:
            # Wait for new content to load after clicking next
            await asyncio.sleep(2)  # Adjust wait time as needed

        # Scroll down
        try:
            await page.evaluate("window.scrollBy(0, 1000)")
        except:
            pass

    return all_sponsored_links

    
async def main():
    """Main function to search sponsors, extract contact info, and write to CSV."""

    searchfor = input("Enter Keyword to search: ")
    filename = "Details_on_" + searchfor + ".CSV"

    try:
        browser = await launch(headless=False, defaultViewport=None, args=['--window-size=1920,1080'])
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()

        # Initial Google search
        await page.goto("http://www.google.com")
        search_bar = await page.querySelector('input[name="q"]')
        await search_bar.type(searchfor)
        await page.keyboard.press("Enter")
        await page.waitForNavigation()

        # Collect sponsored links
        sponsored_links = await find_all_sponsored_links(page)

        # Write data to CSV
        await write_data_to_csv(filename, sponsored_links,page)

    except Exception as e:
        print(f"An error occurred: {e}")
    #await launcher.killChrome()
    await browser.close()


async def write_data_to_csv(filename, sponsored_links, page):
    """Writes extracted data to a CSV file."""

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



asyncio.run(main())

