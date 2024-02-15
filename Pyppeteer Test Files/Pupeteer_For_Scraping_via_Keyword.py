import asyncio
from pyppeteer import launch 
#from 
import time

#<span class="U3A9Ac qV8iec">Sponsored</span>
list_of_sponsored = []
async def main():
    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    #enter your keyword
    searchfor = input(str("Enter Keyword to search: "))
    #searchfor = "Old Age homes in pune"
    page = await context.newPage()
    await page.goto("https://www.google.com")
    #await page.waitFor({3000})
    search_bar = await page.querySelector('input[name="q"]')
    await search_bar.type(searchfor)
    await page.keyboard.press("Enter"),
    await page.waitForNavigation()
    await page.screenshot({'path':'google.png'})
    
    # Capture all links from the page
    all_links = await page.querySelectorAll('a')

    #links = await page.evaluate("return Array.from(document.querySelectorAll('a')).map(a => a.href)")
    #
    #for link in links:
    #    print(f"Found Link: {link}")
    
    
    # Print all links
    for link in all_links:
        href = await link.getProperty('href')
        href_str = await href.jsonValue()
        #href = await page.evaluate("return arguments[0].href", link)
        print(f"Found link: {href_str}")
    
    time.sleep(15)
    await browser.close()
    

try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")

#sponsered_finder = await page.querySelector('<span class="U3A9Ac qV8iec">Sponsored</span>')
#    for i in sponsered_finder:
#        list_of_sponsored.append(i)
#    print(list_of_sponsored)


# Capture sponsored links using the .U3A9Ac qV8iec class
    #sponsored_links = [await link for link in all_links if await link.get_property('class') == 'U3A9Ac qV8iec']

    # Do something with sponsored_links
    #print("Found sponsored links:")
    #for link in sponsored_links:
    #    href = await link.get_attribute('href')
    #    print(f" - {href})")