from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from src.gamedeals.G2AHandler import G2AHandler
from src.gamedeals.SteamHandler import SteamHandler


class FanaticalHandler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.profit_percentage = Decimal(0.20)

    def get_page(self, url: str):
        driver = self.driver
        driver.get(url)
        WebDriverWait(driver, 800).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h4'))
        )
        game_name = driver.find_element_by_tag_name('h1').text
        WebDriverWait(driver, 800).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h4'))
        )
        sale_price = driver.find_element_by_tag_name('h4').find_element_by_tag_name('span').find_element_by_tag_name('b').find_element_by_tag_name('span').find_element_by_tag_name('span').text
        sale_price = Decimal(sale_price.replace('€', ''))
        steam_handler = SteamHandler(driver)
        if steam_handler.get_game_review_number(game_name) > 1000:
            g2a_handler = G2AHandler(driver)
            g2a_price = g2a_handler.lookup_price_of(game_name)
            tentative_price = (sale_price - (sale_price*Decimal(0.108))) - Decimal(0.20)
            after_commission_price = tentative_price - (tentative_price * Decimal(0.01))
            print(g2a_price)
            print(after_commission_price)
            if after_commission_price/g2a_price < self.profit_percentage:
                # TODO: put into external class, add telegram message
                pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1800, 1070)
    driver.implicitly_wait(1)
    fanatical_handler = FanaticalHandler(driver)
    fanatical_handler.get_page('https://www.fanatical.com/en/game/kerbal-space-program')
