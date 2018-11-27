from decimal import Decimal

from selenium import webdriver


class G2AHandler:
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url

    def get_game_name(self):
        driver = self.driver
        driver.get(self.url)
        return driver.find_element_by_class_name('human_name-view').text

    def get_sale_price(self):
        driver = self.driver
        driver.get(self.url)
        return Decimal(driver.find_element_by_class_name('current-price').text)
