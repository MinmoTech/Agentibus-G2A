import time
from decimal import Decimal
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from gamedeals import G2AHandler, SteamHandler, Product
from gamedeals.Product import Game


def set_game_data(driver, game: Game):
    driver.get(game.url)
    game.name = driver.find_element_by_tag_name('h1').text
    if driver.find_elements_by_class_name("stardeal-extras-container"):
        game.sale_price = _get_stardeal_price()
    else:
        game.sale_price = _get_regular_sale_price(driver)
    game.review_count = SteamHandler.get_game_review_number(game.name, driver)
    game.g2a_price = G2AHandler.get_price_of(game, driver)
    Product.set_game_meta_data(game)


def _get_regular_sale_price(driver: webdriver.Chrome):
    sale_price = driver.find_element_by_tag_name('h4').find_element_by_tag_name(
        'span').find_element_by_tag_name(
        'b').find_element_by_tag_name('span').find_element_by_tag_name('span').text
    return Decimal(sale_price.replace('€', ''))


def _get_stardeal_price(driver: webdriver.Chrome):
    promo_div = driver.find_element_by_class_name("promo-price")
    sale_price = promo_div.find_element_by_tag_name('span').find_element_by_class_name('span').text
    return Decimal(sale_price.replace('€', ''))


def __click_cookie_banner(driver: webdriver.Chrome):
    driver.find_element_by_class_name('cookie-btn').click()


def crawl(driver: webdriver.Chrome):
    driver.get('https://www.fanatical.com/en/on-sale')
    __click_cookie_banner(driver)
    game_list = []
    while True:
        time.sleep(2)
        bundle_container = driver.find_element_by_class_name('bundle-page')
        link_containers = bundle_container.find_elements_by_class_name('faux-block-link__overlay-link')
        for container in link_containers:
            if 'bundle' not in container.get_attribute('href'):
                game = Game()
                game.url = container.get_attribute('href')
                game.site = 'Fanatical'
                game_list.append(game)
        try:
            driver.find_element_by_xpath('//button[@aria-label="Next"]').click()
        except NoSuchElementException:
            break
    return game_list
