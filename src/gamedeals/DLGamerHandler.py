from decimal import Decimal

from selenium import webdriver
from selenium.webdriver import ActionChains


class DLGamerHandler:
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url

    def get_game_name(self):
        driver = self.driver
        driver.get(self.url)
        self.__set_currency(driver)
        return driver.find_element_by_class_name('product-title').text

    def get_sale_price(self):
        driver = self.driver
        driver.get(self.url)
        self.__set_currency(driver)
        return Decimal(driver.find_element_by_class_name('product-sheet-price').text.replace('€', ''))

    @staticmethod
    def __set_currency(driver: webdriver.Chrome):
        currency_dropdown = driver.find_element_by_class_name('dropdown-toggle')
        actions = ActionChains(driver)
        actions.move_to_element(currency_dropdown)
        actions.click()
        germany_locale_element = driver.find_element_by_class_name('sprite-flag-de')
        actions.move_to_element(germany_locale_element)
        actions.click()
