import logging
import time
from contextlib import suppress
from decimal import Decimal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from src.gamedeals import Utility
from src.gamedeals.Product import Game


def get_price_of(game: Game, driver: webdriver.Chrome):
    driver.get('https://www.g2a.com/')
    time.sleep(2)
    with suppress(NoSuchElementException):
        modal_options_buttons = driver.find_element_by_class_name('modal-options__buttons')
        cookie_confirm_button = modal_options_buttons.find_element_by_class_name('btn-primary')
        cookie_confirm_button.click()
    search_bar_parent = driver.find_element_by_class_name('topbar-search-form')
    search_bar = search_bar_parent.find_element_by_tag_name('input')
    search_query = game.name.lower() + f' {game.sale_platform} key global'.lower()
    _actions_send_keys(driver, search_bar, search_query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(2)
    product_grids = driver.find_elements_by_class_name('products-grid__item')
    for product_grid in product_grids:
        if _find_proper_card(product_grid, game.name, search_query):
            time.sleep(1)
            offers = driver.find_elements_by_class_name('offer')
            for offer in offers:
                if 'Official developer' not in offer.get_attribute('innerHTML'):
                    try:
                        rating_count = _get_g2a_rating_count(offer)
                    except ValueError:
                        continue
                    if game.review_count < 500:
                        return _get_price(offer)
                    if rating_count > 1000:
                        return _get_price(offer)
    return Decimal(0)


def _find_proper_card(product_grid, game_name: str, search_query: str):
    logger = logging.getLogger()
    card_wrappers = product_grid.find_elements_by_class_name('card-wrapper')
    for card_wrapper in card_wrappers:
        card_title_element = card_wrapper.find_element_by_class_name('Card__title')
        card_title = Utility.filter_special_characters(card_title_element.find_element_by_tag_name('a').text).lower()
        words_of_game_name = Utility.filter_special_characters(game_name.lower()).split()
        logger.info(f"Comparing original game title ({search_query}) to g2a game title ({card_title})")
        if all(x in card_title for x in words_of_game_name) and len(search_query) >= len(card_title):
            card_wrapper.click()
            return True
        else:
            logger.info("Could not find game on G2A")
    return False


def _get_g2a_rating_count(offer):
    try:
        rating_count_element = offer.find_element_by_class_name('rating-data')
        seller_info_percent = rating_count_element.find_element_by_class_name('seller-info__percent')
        separator = rating_count_element.find_element_by_class_name('separator')
        rating_count_dirty = rating_count_element.text
    except NoSuchElementException:
        return 0
    return int(rating_count_dirty.replace(seller_info_percent.text, '').replace(separator.text, ''))


def _get_price(offer):
    try:
        price_element = offer.find_element_by_class_name('price')
        currency = price_element.find_element_by_class_name('price__currency')
        price = price_element.text.replace(currency.text, '')
    except NoSuchElementException:
        return Decimal(0)
    return Decimal(price)


def _actions_click_element(driver: webdriver.Chrome, element):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.click()


def _actions_send_keys(driver: webdriver.Chrome, element, text: str):
    # from: https://stackoverflow.com/questions/45442485/cannot-focus-element-using-selenium
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.click()
    actions.send_keys(text)
    actions.perform()
