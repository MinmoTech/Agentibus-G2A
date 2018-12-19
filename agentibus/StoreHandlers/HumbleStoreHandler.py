import collections
import time
from decimal import Decimal
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from agentibus import G2AHandler, SteamHandler, Product, Main
from agentibus.Main import managed_chromedriver
from agentibus.Product import Game


def set_game_data(game: Game, driver: webdriver.Chrome):
    driver.get(game.url)
    _do_age_check(driver)
    game.name = driver.find_element_by_class_name('human_name-view').text
    game.sale_price = Decimal(
        driver.find_element_by_class_name('current-price').text.replace('€', '').replace(',', '.'))
    opts = Main.get_chromedriver_options()
    with managed_chromedriver(opts) as nested_driver:
        game.review_count = SteamHandler.get_game_review_number(game.name, nested_driver)
        game.g2a_price = G2AHandler.get_price_of(game, nested_driver)
        game.sale_platform = _get_platform(driver)
    Product.set_game_meta_data(game)


def _get_platform(driver: webdriver.Chrome):
    platform_parent = driver.find_element_by_class_name('availability-section')
    platform = platform_parent.find_element_by_class_name('platform').get_attribute('class')
    if 'steam' in platform:
        return 'Steam'
    else:
        return platform.replace('platform ', '')


def _do_age_check(driver: webdriver.Chrome):
    if 'Content in this product may not be appropriate for all ages.' in driver.page_source:
        select = Select(driver.find_element_by_class_name('js-selection-year'))
        select.select_by_value('1990')
        driver.find_element_by_class_name('js-submit-button').click()


def crawl(driver: webdriver.Chrome) -> List[Game]:
    driver.get('https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale')
    game_list = []
    game_boxes = driver.find_elements_by_class_name('entity-link')
    game_list.append(_get_filled_game(game_boxes))
    counter = 0
    while True:
        counter += 1
        try:
            driver.get(f'https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale&page={counter}')
            time.sleep(2)
            driver.find_element_by_class_name('entity-link')
            game_boxes = driver.find_elements_by_class_name('entity-link')
            game_list.append(_get_filled_game(game_boxes))
        except NoSuchElementException:
            break
    return game_list


def _get_filled_game(game_boxes: collections.Iterable):
    for game_box in game_boxes:
        game = Game()
        game.url = game_box.get_attribute('href')
        game.site = 'HumbleBundle'
        return game
