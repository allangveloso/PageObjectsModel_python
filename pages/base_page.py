"""
A classe BasePage é a classe base para todas as páginas do aplicativo. 
Ela encapsula as operações comuns de interação com a interface do usuário, 
como clicar em elementos, preencher campos de texto e verificar a visibilidade de elementos. 
Isso promove a reutilização de código e torna os testes mais legíveis e fáceis de manter.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver): # O construtor da classe BasePage recebe o driver do Selenium, que é passado pelas classes filhas (como LoginPage, InventoryPage, etc.) quando elas são instanciadas nos testes.
        self.driver = driver
        self.wait = WebDriverWait(driver, 10) 

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: tuple) -> str:
        return self.find(locator).text.strip()

    def is_visible(self, locator: tuple) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except:
            return False