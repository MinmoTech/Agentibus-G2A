from decimal import Decimal

from selenium import webdriver


class IndiegalaHandler:
    def __init__(self, indiegala_driver: webdriver.Chrome, indiegala_url: str):
        self.driver = indiegala_driver
        self.indiegala_url = indiegala_url

    def get_game_name(self):
        driver = self.driver
        url = self.indiegala_url
        driver.get(url)
        if 'crackerjack' not in driver.page_source:
            return driver.find_element_by_tag_name('h1').text
        else:
            return self._get_game_name_crackerjack(driver)

    @staticmethod
    def _get_game_name_crackerjack(driver: webdriver.Chrome):
        game_info = driver.find_element_by_class_name('game-info')
        return game_info.find_element_by_class_name('title').text

    def get_sale_price(self):
        driver = self.driver
        driver.get(self.indiegala_url)
        if 'crackerjack' not in driver.page_source:
            sale_price = driver.find_element_by_class_name('current-price').text
            return Decimal(sale_price.replace('€', ''))
        else:
            return self._get_sale_price_crackerjack(driver)

    @staticmethod
    def _get_sale_price_crackerjack(driver: webdriver.Chrome):
        return Decimal(driver.find_element_by_id('price').text)
