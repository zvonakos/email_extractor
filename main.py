import os
import re
import pytesseract
from PIL import Image


class EmailExtractor:
    def __init__(self, input_path='./input'):  # decided to make input and output hardcoded if you're willing you can choose your own =)
        self.input_path = input_path
        self.output_path = './output'
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # to be honest I'm not really keen on regex.
        self.name_pattern = r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'  # I think there is more efficient regex for that
        self.text_filename = 'emails.txt'

    def extract_emails_with_names(self, text: str) -> dict:
        matches = re.findall(self.email_pattern, text)  # finding emails
        matches = set(matches)  # getting rid of duplicates
        return {re.match(self.name_pattern, email).group(1).capitalize(): email for email in matches}  # retrieving names from emails


    def sort_emails(self, emails: dict) -> dict:  # just decided to make as a separate function
        return dict(sorted(emails.items()))  # sorting emails

    def get_emails_from_files(self, files: list) -> dict:
        all_emails = dict()
        for file in files:
            with Image.open(f'{self.input_path}/{file}') as img:
                text = pytesseract.image_to_string(img)  # basic retrieve of text inside image
                extracted_emails = self.extract_emails_with_names(text)  # retrieving dict of email inside the text
                all_emails = {**all_emails, **extracted_emails}  # I know there is an update in dict, just decided to show another way of updating dicts

        return all_emails


    def write_emails_to_file(self, all_emails: dict) -> None:
        with open(f'{self.output_path}/{self.text_filename}', 'w') as file:
            counter = 1
            for name, email in all_emails.items():
                file.write(f'{counter}.{name}: {email}\n')  # writing emails to regular text file
                counter += 1


    def extract_emails(self) -> None:
        files = os.listdir(self.input_path)  # getting the list of files inside input directory for further retrieving process

        all_emails = self.get_emails_from_files(files)

        sorted_all_emails = self.sort_emails(all_emails)

        self.write_emails_to_file(sorted_all_emails)
        print(os.path.abspath(self.text_filename))


if __name__ == '__main__':
    email_extractor = EmailExtractor()
    email_extractor.extract_emails()
