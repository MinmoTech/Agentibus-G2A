import re
from contextlib import contextmanager
from decimal import Decimal
from typing import List

from selenium import webdriver

from agentibus import Utility, G2AHandler, SteamHandler, Product, Main
from agentibus.Product import Bundle, Game


@contextmanager
def managed_chromedriver(options):
    chrome_driver = webdriver.Chrome(options=options)
    try:
        yield chrome_driver
    finally:
        chrome_driver.quit()


def set_bundle_data(driver: webdriver.Chrome, bundle: Bundle) -> List[str]:
    driver.get(bundle.url)
    bundle.name = driver.find_element_by_class_name('hero-title').text
    bundle.site = 'HumbleBundle'
    game_name_containers = driver.find_elements_by_class_name('dd-image-box-text')
    opts = Main.get_chromedriver_options()
    with managed_chromedriver(opts) as nested_driver:
        nested_driver.set_window_size(1800, 1070)
        nested_driver.implicitly_wait(2)
        for container in game_name_containers:
            game = Game()
            game.site = 'HumbleBundle'
            game.name = container.text
            game.review_count = SteamHandler.get_game_review_number(game.name, nested_driver)
            game.g2a_price = G2AHandler.get_price_of(game, nested_driver)
            bundle.games.append(game)
            print(f'G2A price of {game.name}: {str(game.g2a_price)}')
    bundle.sale_price = _get_total_sale_price(driver)
    for game in bundle.games:
        bundle.g2a_price = bundle.g2a_price + game.g2a_price
        bundle.after_commission_price = bundle.after_commission_price + Utility.calculate_net_price(
            game.g2a_price)
    Product.set_bundle_meta_data(bundle)


def _get_total_sale_price(driver: webdriver.Chrome) -> Decimal:
    headlines = driver.find_elements_by_class_name('dd-header-headline')
    prices = []
    for headline in headlines:
        matches = re.findall('€\\d.?\\d?\\d?', headline.text)
        if len(matches) > 0:
            prices.append(Decimal(matches[0].replace('€', '')))
    return max(prices)


def crawl(driver: webdriver.Chrome) -> List[Bundle]:
    driver.get('https://www.humblebundle.com/')
    bundle_dropdown = driver.find_element_by_xpath('//div[@data-dropdown-type="bundle-dropdown"]')
    bundle_dropdown.click()
    bundle_parent = bundle_dropdown.find_element_by_xpath('..')
    bundles = bundle_parent.find_elements_by_class_name('image-link')
    bundle_list = []
    for bundle in bundles:
        bundle = Bundle(url=bundle.get_attribute('href'))
        bundle_list.append(bundle)
    return bundle_list
