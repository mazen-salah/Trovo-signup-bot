from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from faker import Faker
import random
import time
from tempMail import tempMail


class MyTempMail:
    def __init__(self, username):
        self.username = username
        self.domain = random.choice(tempMail.TempMail().get_list_of_active_domains)
        self.email = f"{self.username}@{self.domain}"
        self.tempmail = tempMail.TempMail(login=self.username, domain=self.domain)

    def get_code(self):
        email_data = self.tempmail.get_single_email()
        code = email_data['subject'].split(" ")[0]
        return code


class User:
    def __init__(self):
        fake = Faker()
        self.username = fake.user_name() + str(random.randint(1000, 3000))
        self.password = fake.password()
        self.day = str(random.randint(1, 28))
        self.month = str(random.randint(1, 12))
        self.year = str(random.randint(1980, 2003))
        self.tempmail = MyTempMail(self.username)


class Bot:
    def __init__(self):
        self.user = User()
        self.URL = f"https://cdn.trovo.live/page/login-page.html?state=0&minState=0&r_url=https%3A%2F%2Fstudio.trovo.live%2F"
        self.selectors = {
            "SIGN_UP": "body > div.login-box > div.content-box > div.content-left > ul > li:nth-child(2)",
            "USERNAME": "body > div.login-box > div.content-box > div.content-left > div > div:nth-child(3) > div > input",
            "EMAIL": "body > div.login-box > div.content-box > div.content-left > div > div.input-el.email-input > div > input",
            "PASSWORD": "body > div.login-box > div.content-box > div.content-left > div > div:nth-child(4) > div > input",
            "DAY": "body > div.login-box > div.content-box > div.content-left > div > div.wrapper > div > div:nth-child(2) > div.day > input",
            "YEAR": "body > div.login-box > div.content-box > div.content-left > div > div.wrapper > div > div:nth-child(3) > div.year > input",
            "MONTH": "body > div.login-box > div.content-box > div.content-left > div > div.wrapper > div > div:nth-child(1) > div.month > span",
            "MONTH_VALUE": f"body > div.login-box > div.content-box > div.content-left > div > div.wrapper > div > div:nth-child(1) > div.drop-list > ul > li:nth-child({self.user.month})",
            "SUBMIT": "body > div.login-box > div.content-box > div.content-left > div > button.cat-button.button-sign-up.large.primary.block",
            "VERIFY_CODE": "body > div.login-box > div.content-box > div.content-left > section > div.wrapper.verify-code > input"
        }
        options = uc.ChromeOptions()

        self.driver = uc.Chrome(options=options)

    def navigate_to_url(self):
        time.sleep(5)
        self.driver.get("https://www.croxyproxy.com/")
        self.driver.find_element(By.CSS_SELECTOR, "#url").send_keys(self.URL)
        self.driver.find_element(By.CSS_SELECTOR, "#requestSubmit").click()

    def wait_for_element(self, selector):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.quit()

    def click_element(self, selector):
        self.wait_for_element(selector)
        self.driver.find_element(By.CSS_SELECTOR, selector).click()

    def fill_form(self):
        self.wait_for_element(self.selectors["SIGN_UP"])
        self.click_element(self.selectors["SIGN_UP"])
        self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["USERNAME"]).send_keys(self.user.username)
        self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["PASSWORD"]).send_keys(self.user.password)
        self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["DAY"]).send_keys(self.user.day)
        self.click_element(self.selectors["MONTH"])
        self.click_element(self.selectors["MONTH_VALUE"])
        self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["YEAR"]).send_keys(self.user.year)
        self.driver.find_element(By.CSS_SELECTOR, self.selectors["EMAIL"]).send_keys(
            self.user.tempmail.email)
        self.click_element(self.selectors["SUBMIT"])

    def solve_captcha(self):
        time.sleep(5)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(
            By.XPATH, ".//iframe[@title='reCAPTCHA']"))
        self.driver.find_element(By.ID, "recaptcha-anchor-label").click()
        self.driver.switch_to.default_content()
        input("Please, Solve the captcha and press enter to continue...")
        code = self.user.tempmail.get_code()

        self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["VERIFY_CODE"]).send_keys(code)
        time.sleep(10)

    def start(self):
        try:
            self.navigate_to_url()
            self.fill_form()
            self.solve_captcha()
            with open("accounts.txt", "a") as f:
                f.write(
                    f"{self.user.tempmail.email}:{self.user.password}:{self.user.username},{self.user.day}/{self.user.month}/{self.user.year}\n")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    while True:
        Bot().start()
