import logging
from decimal import Decimal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from src.gamedeals.SteamHandler import SteamHandler


class G2AHandler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.logger = logging.getLogger()

    def lookup_price_of(self, game_name: str):
        driver = self.driver
        steam_review = self.__get_steam_review_count(game_name)
        driver.get('https://www.g2a.com/')
        try:
            modal_options_buttons = driver.find_element_by_class_name('modal-options__buttons')
            cookie_confirm_button = modal_options_buttons.find_element_by_class_name('btn-primary')
            cookie_confirm_button.click()
        except NoSuchElementException:
            pass
        search_bar_parent = driver.find_element_by_class_name('topbar-search-form')
        search_bar = search_bar_parent.find_element_by_tag_name('input')
        search_query = game_name + ' Steam Key Global'
        actions_send_keys(driver, search_bar, search_query)
        search_bar.send_keys(Keys.RETURN)
        product_grids = driver.find_elements_by_class_name('products-grid__item')
        for product_grid in product_grids:
            card_wrapper = product_grid.find_element_by_class_name('card-wrapper')
            card_title_element = card_wrapper.find_element_by_class_name('Card__title')
            card_title = card_title_element.find_element_by_tag_name('a').text
            words_of_game_name = game_name.split()
            self.logger.info(f"Comparing original game title ({search_query}) to g2a game title ({card_title})")
            if all(x in card_title for x in words_of_game_name) and len(search_query) >= len(card_title):
                self.logger.info("Success!")
                card_wrapper.click()
                try:
                    WebDriverWait(driver, 10).until(
                        expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'expander__button'))
                    )
                    offer_expander_button = driver.find_element_by_class_name('expander__button')
                    offer_expander_button.click()
                except TimeoutException:
                    pass
                except NoSuchElementException:
                    pass
                offers = driver.find_elements_by_class_name('offer')
                for offer in offers:
                    rating_count_element = offer.find_element_by_class_name('rating-data')
                    seller_info_percent = rating_count_element.find_element_by_class_name('seller-info__percent')
                    separator = rating_count_element.find_element_by_class_name('separator')
                    rating_count_dirty = rating_count_element.text
                    rating_count = int(
                        rating_count_dirty.replace(seller_info_percent.text, '').replace(separator.text, ''))
                    if steam_review < 500:
                        return self.__get_price(offer)
                    if rating_count > 1000:
                        return self.__get_price(offer)

    @staticmethod
    def __get_steam_review_count(game_name):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1800, 1070)
        driver.implicitly_wait(1)
        steam_handler = SteamHandler(driver)
        review_number = steam_handler.get_game_review_number(game_name)
        driver.quit()
        return review_number

    @staticmethod
    def __get_price(offer):
        price_element = offer.find_element_by_class_name('price')
        currency = price_element.find_element_by_class_name('price__currency')
        price = price_element.text.replace(currency.text, '')
        return Decimal(price)


def actions_click_element(driver: webdriver.Chrome, element):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.click()


def actions_send_keys(driver: webdriver.Chrome, element, text: str):
    # from: https://stackoverflow.com/questions/45442485/cannot-focus-element-using-selenium
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.click()
    actions.send_keys(text)
    actions.perform()
