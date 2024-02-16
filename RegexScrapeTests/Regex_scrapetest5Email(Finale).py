import asyncio
from pyppeteer import launch
import re

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://sanctushealthcare.com/contact/')      #https://sanctushealthcare.com/contact/ #http://127.0.0.1:5500/HTML%20Files/My%20Care.html

    webpage = await page.content()
    #print(webpage)
    phone_numbers = re.findall(r"(\+\d{2})[- ]?(\d{10})", webpage)   
    email_adresses = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", webpage)

    #print(email_adresses)
    ##print(f"Phone Numbers = {phone_numbers}")
    #print()
    unique_phone_numbers = set()
    unique_emails = set()
    
    for email in email_adresses:
        if email not in unique_emails:
            unique_emails.add(email)
        
        
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
    #print("Unique Phone Numbers:", unique_phone_numbers_list)
    print()
    print()
    print()
    
    Email_List = list(unique_emails)

    cleaned_strings = unique_phone_numbers_list
    number_printer = ""
    for i in cleaned_strings:
        if(i == cleaned_strings[0]):
            number_printer = number_printer+i
        else:
            number_printer = number_printer+ ", "+i
       
    email_printer = ""
    for i in Email_List:
        if(i == Email_List[0]):
            email_printer = email_printer+i
        else:
            email_printer = email_printer+i
            
        
    print("Phone Numbers:", number_printer)
    print("Emails:", email_printer)
    await browser.close()

asyncio.run(main())
