import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def get_game_review_number(game_name, driver: webdriver.Chrome):
    logger = logging.getLogger()
    driver.get('https://store.steampowered.com/')
    search_box = driver.find_element_by_id('store_nav_search_term')
    search_box.send_keys(game_name)
    search_box.send_keys(Keys.RETURN)
    try:
        search_result_container = driver.find_element_by_id('search_result_container')
        search_result_container.find_element_by_tag_name('a').click()
        _do_age_check(driver)
        user_reviews_count = driver.find_element_by_xpath("//meta[@itemprop='reviewCount']").get_attribute('content')
    except NoSuchElementException:
        return 0
    logger.info(f'Steam reviews of {game_name}: {user_reviews_count}')
    return int(user_reviews_count)


def _do_age_check(driver: webdriver.Chrome):
    if 'not appropriate for all ages' in driver.page_source:
        select = Select(driver.find_element_by_xpath('//select[@name="ageYear"]'))
        select.select_by_value('1990')
        driver.find_element_by_xpath("//*[contains(text(), 'View Page')]").click()
