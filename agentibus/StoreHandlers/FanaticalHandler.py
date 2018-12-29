import logging
import time
from decimal import Decimal
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from agentibus import Product
from agentibus.Product import Game


def set_game_data(driver, game: Game):
    driver.get(game.url)
    try:
        logging.getLogger().info(f'Getting {game.name} info.')
        game.name = driver.find_element_by_tag_name('h1').text

        if driver.find_elements_by_class_name("stardeal-extras-container"):
            game.sale_price = _get_stardeal_price(driver)
        else:
            try:
                game.sale_price = _get_regular_sale_price(driver)
            except NoSuchElementException:
                logging.getLogger().error(f'Could not get proper info at {game.url}')
        Product.set_game_meta_data(game, driver)
    except NoSuchElementException:
        logging.getLogger().error(f'Could not get game name at {game.url}')


def _get_regular_sale_price(driver: webdriver.Chrome):
    sale_price = driver.find_element_by_tag_name('h4').find_element_by_tag_name('span').find_element_by_tag_name(
        'b').find_element_by_tag_name('span').find_element_by_tag_name('span').text
    return Decimal(sale_price.replace('€', ''))


def _get_stardeal_price(driver: webdriver.Chrome):
    promo_div = driver.find_element_by_class_name("promo-price")
    sale_price = promo_div.find_element_by_tag_name('span').find_element_by_class_name('span').text
    return Decimal(sale_price.replace('€', ''))


def __click_cookie_banner(driver: webdriver.Chrome):
    driver.find_element_by_class_name('cookie-btn').click()


def crawl(driver: webdriver.Chrome):
    logging.getLogger().info('Crawling Fanatical')
    driver.get('https://www.fanatical.com/en/on-sale')
    if 'Apply this code to get an extra' in driver.page_source:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    __click_cookie_banner(driver)
    if 'Apply this code to get an extra' in driver.page_source:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    game_list = []
    counter = 0
    while True:
        time.sleep(2)
        if 'Apply this code to get an extra' in driver.page_source:
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
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
            counter += 1
        except NoSuchElementException:
            logging.getLogger().info(f'Craweled {counter} pages and found {len(game_list)} games.')
            break
    return game_list
