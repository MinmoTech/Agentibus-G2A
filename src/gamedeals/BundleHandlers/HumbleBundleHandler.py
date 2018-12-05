import re
from decimal import Decimal
from typing import List

from selenium import webdriver

from src.gamedeals.BundleHandlers.BundleHandler import BundleHandler


class HumbleBundleHandler(BundleHandler):
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url

    def get_game_names(self) -> List[str]:
        driver = self.driver
        driver.get(self.url)
        game_name_containers = driver.find_elements_by_class_name('dd-image-box-text ')
        game_name_list = []
        for container in game_name_containers:
            game_name_list.append(container.text)
        return game_name_list

    def get_total_sale_price(self) -> Decimal:
        driver = self.driver
        driver.get(self.url)
        headlines = driver.find_elements_by_class_name('dd-header-headline')
        prices = []
        for headline in headlines:
            matches = re.findall('€\\d.?\\d?\\d?', headline.text)
            if len(matches) > 0:
                prices.append(Decimal(matches[0].replace('€', '')))
        return max(prices)


class HumbleCrawler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def crawl(self):
        driver = self.driver
        driver.get('https://www.humblebundle.com/')
        bundle_dropdown = driver.find_element_by_xpath('//div[@data-dropdown-type="bundle-dropdown"]')
        bundle_dropdown.click()
        bundle_parent = bundle_dropdown.find_element_by_xpath('..')
        bundles = bundle_parent.find_elements_by_class_name('image-link')
        return [bundle.get_attribute('href') for bundle in bundles]

