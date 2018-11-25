from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class FanaticalHandler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

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
        print(game_name, ': ', sale_price)
        driver.quit()


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    fanatical_handler = FanaticalHandler(driver)
    fanatical_handler.get_page('https://www.fanatical.com/en/game/kerbal-space-program')
