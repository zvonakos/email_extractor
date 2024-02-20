import os
import re
import pytesseract
from PIL import Image

input_path = './input'
output_path = './output'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # to be honest I'm not really keen on regex.
name_pattern = r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'  # I think there is more efficient regex for that


def extract_emails_with_names(text: str) -> dict:
    matches = re.findall(email_pattern, text)  # finding emails
    matches = set(matches)  # getting rid of duplicates
    return {re.match(name_pattern, email).group(1).capitalize(): email for email in matches}  # retrieving names from emails


def extract_emails() -> None:
    all_emails = dict()
    files = os.listdir(input_path)  # getting the list of files inside input directory for further retrieving process
    for file in files:
        with Image.open(f'{input_path}/{file}') as img:
            text = pytesseract.image_to_string(img)  # basic retrieve of text inside image
            extracted_emails = extract_emails_with_names(text)  # retrieving dict of email inside the text
            all_emails = {**all_emails, **extracted_emails}  # I know there is an update in dict, just decided to show another way of updating dicts
    with open(f'{output_path}/emails.txt', 'w') as file:
        counter = 1
        for name, email in all_emails.items():
            file.write(f'{counter}.{name}: {email}\n')  # writing emails to regular text file
            counter += 1


if __name__ == '__main__':
    extract_emails()
