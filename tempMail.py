import requests
import random


class TempMail():

    def __init__(self, login=None, domain='1secmail.com'):
        self.login = login
        self.domain = domain
    def get_single_email(self, message_id=None):
            if self.login is None or self.domain is None:
                self.generate_random_email_address()
            
            if message_id is None:
                email_list = self.get_list_of_emails()
                if email_list:
                    message_id = email_list[0]['id']

            r = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.login}&domain={self.domain}&id={message_id}")
            return r.json()
    def generate_random_email_address(self) -> None:
        r = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=10')
        get_random = f'{random.choice(r.json())}'
        self.login, self.domain = get_random.split('@')

    @property
    def get_list_of_active_domains(self):
        return requests.get('https://www.1secmail.com/api/v1/?action=getDomainList').json()

    def get_list_of_emails(self):
        if self.login is None or self.domain is None:
            self.generate_random_email_address()
        r = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={self.login}&domain={self.domain}')
        return r.json()

    def get_login(self):
        return self.login

    def get_domain(self):
        return self.domain

    def download_attachment_by_id(self, attachment: str, id: str):

        if self.login is None or self.domain is None:
            return 'You cant download anything, your login or domain is None.'

        r = requests.get(f"https://www.1secmail.com/api/v1/?action=download&login="
                         f"{self.login}&domain={self.domain}&id={id}&file={attachment}")
        print(r.text)

        if 'Message not found' in r.text:
            return 'The file could not be found, please check the correctness of the entered data'

        with open(attachment, 'wb') as file:
            file.write(r.content)

    def download_all_files(self):
        emails = self.get_list_of_emails()
        lst_with_files = []
        for i in emails:
            r = requests.get(
                f'https://www.1secmail.com/api/v1/?action=readMessage&login={self.login}&domain={self.domain}&id={i["id"]}').json()
            lst_with_files.append(
                {
                    'filename': f"{r['attachments'][0]['filename']}",
                    'id': f"{i['id']}"
                }
            )
        for i in lst_with_files:
            self.download_attachments_by_id(i['filename'], i['id'])



