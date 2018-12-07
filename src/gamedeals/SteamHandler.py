import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_game_review_number(game_name, driver: webdriver.Chrome):
    logger = logging.getLogger()
    driver.get('https://store.steampowered.com/')
    search_box = driver.find_element_by_id('store_nav_search_term')
    search_box.send_keys(game_name)
    search_box.send_keys(Keys.RETURN)
    search_result_container = driver.find_element_by_id('search_result_container')
    search_result_container.find_element_by_tag_name('a').click()
    user_reviews_count = driver.find_element_by_xpath("//meta[@itemprop='reviewCount']").get_attribute('content')
    logger.info(f'Steam reviews of {game_name}: {user_reviews_count}')
    return int(user_reviews_count)
