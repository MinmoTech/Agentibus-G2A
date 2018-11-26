from decimal import Decimal
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class FanaticalHandler:
    def __init__(self, fanatical_driver: webdriver.Chrome, fanatical_url: str):
        self.driver = fanatical_driver
        self.fanatical_url = fanatical_url

    def get_game_name(self):
        fanatical_driver = self.driver
        fanatical_driver.get(self.fanatical_url)
        WebDriverWait(fanatical_driver, 800).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )
        game_name = fanatical_driver.find_element_by_tag_name('h1').text
        return game_name

    def get_sale_price(self):
        fanatical_driver = self.driver
        fanatical_driver.get(self.fanatical_url)
        WebDriverWait(fanatical_driver, 800).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h4'))
        )
        sale_price = fanatical_driver.find_element_by_tag_name('h4').find_element_by_tag_name(
            'span').find_element_by_tag_name(
            'b').find_element_by_tag_name('span').find_element_by_tag_name('span').text
        sale_price = Decimal(sale_price.replace('€', ''))
        return sale_price
