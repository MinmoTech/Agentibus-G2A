from decimal import Decimal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class G2AHandler:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def lookup_price_of(self, game_name:str):
        driver = self.driver
        driver.get('https://www.g2a.com/')
        try:
            modal_options_buttons = driver.find_element_by_class_name('modal-options__buttons')
            cookie_confirm_button = modal_options_buttons.find_element_by_class_name('btn-primary')
            cookie_confirm_button.click()
        except NoSuchElementException:
            pass
        search_bar_parent = driver.find_element_by_class_name('topbar-search-form')
        search_bar = search_bar_parent.find_element_by_tag_name('input')
        # from: https://stackoverflow.com/questions/45442485/cannot-focus-element-using-selenium
        actions = ActionChains(driver)
        actions.move_to_element(search_bar)
        actions.click()
        actions.send_keys('"', game_name, '"')
        actions.perform()
        search_bar.send_keys(Keys.RETURN)
        product_grid = driver.find_element_by_class_name('products-grid__item')
        card_wrapper = product_grid.find_element_by_class_name('card-wrapper')
        card_wrapper.click()
        WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'expander__button'))
        )
        offer_expander_button = driver.find_element_by_class_name('expander__button')
        offer_expander_button.click()
        offers = driver.find_elements_by_class_name('offer')
        for offer in offers:
            rating_count_element = offer.find_element_by_class_name('rating-data')
            seller_info_percent = rating_count_element.find_element_by_class_name('seller-info__percent')
            separator = rating_count_element.find_element_by_class_name('separator')
            rating_count_dirty = rating_count_element.text
            rating_count = int(rating_count_dirty.replace(seller_info_percent.text, '').replace(separator.text, ''))
            if rating_count > 10000:
                price_element = offer.find_element_by_class_name('price')
                currency = price_element.find_element_by_class_name('price__currency')
                price = price_element.text.replace(currency.text, '')
                return Decimal(price)
