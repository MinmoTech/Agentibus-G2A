from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SteamHandler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def get_game_review_number(self, game_name):
        driver = self.driver
        driver.get('https://store.steampowered.com/')
        search_box = driver.find_element_by_id('store_nav_search_term')
        search_box.send_keys(game_name)
        search_box.send_keys(Keys.RETURN)
        search_result_container = driver.find_element_by_id('search_result_container')
        search_result_container.find_element_by_tag_name('a').click()
        user_reviews_count = driver.find_element_by_xpath("//meta[@itemprop='reviewCount']").get_attribute('content')
        return int(user_reviews_count)
