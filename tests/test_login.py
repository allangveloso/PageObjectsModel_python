from conftest import base_url
from conftest import credentials
from pages.login_page import LoginPage
# from pages.inventory_page import InventoryPage


def test_login(driver, base_url, credentials):
    login = LoginPage(driver)
    # inventory = InventoryPage(driver)

    login.load(base_url)
    login.login(credentials["username"], credentials["password"])
    # assert inventory.is_loaded(), "Página Inventory carega após o login"