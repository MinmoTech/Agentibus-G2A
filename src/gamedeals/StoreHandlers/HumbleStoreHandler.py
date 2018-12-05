import time
from decimal import Decimal
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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


class HumbleStoreHandler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def crawl(self) -> List[str]:
        driver = self.driver
        driver.get('https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale')
        store_links = []
        game_boxes = driver.find_elements_by_class_name('entity-link')
        store_links.append([game_box.get_attribute('href') for game_box in game_boxes])
        counter = 0
        while True:
            counter += 1
            try:
                driver.get(f'https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale&page={counter}')
                time.sleep(2)
                driver.find_element_by_class_name('entity-link')
                game_boxes = driver.find_elements_by_class_name('entity-link')
                store_links.append([game_box.get_attribute('href') for game_box in game_boxes])
            except NoSuchElementException:
                break
        return store_links
