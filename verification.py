import tempMail
from bs4 import BeautifulSoup
import json


while True:
    email = input("email: ")
    login = email.split("@")[0]
    domain = email.split("@")[1]
    mail = tempMail.TempMail(login=login, domain=domain)
    html = mail.get_single_email()['body']
    soup = BeautifulSoup(html, 'html.parser')
    strong_elements = soup.find_all('strong')
    verification_code = strong_elements[2].text if len(strong_elements) > 1 else None
    print("Verification Code:", verification_code)
