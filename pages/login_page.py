from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):  #a classe LoginPage herda a classe BasePage
    USERNAME_TXT = (By.ID, "user-name")
    PASSWORD_TXT = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")

    def load(self, base_url: str):
        self.open(base_url)

    def login(self, username: str, password: str):
        self.type(self.USERNAME_TXT, username)
        self.type(self.PASSWORD_TXT, password)
        self.click(self.LOGIN_BTN)