from decimal import Decimal
from selenium import webdriver


class FanaticalHandler:
    def __init__(self, fanatical_driver: webdriver.Chrome, fanatical_url: str):
        self.driver = fanatical_driver
        self.url = fanatical_url

    def get_game_name(self):
        driver = self.driver
        driver.get(self.url)
        game_name = driver.find_element_by_tag_name('h1').text
        return game_name

    def get_sale_price(self):
        driver = self.driver
        driver.get(self.url)
        if not driver.find_elements_by_class_name("stardeal-extras-container"):
            sale_price = driver.find_element_by_tag_name('h4').find_element_by_tag_name(
                'span').find_element_by_tag_name(
                'b').find_element_by_tag_name('span').find_element_by_tag_name('span').text
            sale_price = Decimal(sale_price.replace('€', ''))
            return sale_price
        else:
            promo_div = driver.find_element_by_class_name("promo-price")
            sale_price = promo_div.find_element_by_tag_name('span').find_element_by_class_name('span').text
            return Decimal(sale_price.replace('€', ''))
