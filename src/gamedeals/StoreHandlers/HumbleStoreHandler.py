from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.support.select import Select


class HumbleStoreHandler:
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url

    def get_game_name(self):
        driver = self.driver
        driver.get(self.url)
        self.__do_age_check(driver)
        return driver.find_element_by_class_name('human_name-view').text

    def get_sale_price(self):
        driver = self.driver
        driver.get(self.url)
        self.__do_age_check(driver)
        return Decimal(driver.find_element_by_class_name('current-price').text.replace('€', '').replace(',', '.'))

    @staticmethod
    def __do_age_check(driver: webdriver.Chrome):
        if 'Content in this product may not be appropriate for all ages.' in driver.page_source:
            select = Select(driver.find_element_by_class_name('js-selection-year'))
            select.select_by_value('1990')
            driver.find_element_by_class_name('js-submit-button').click()
