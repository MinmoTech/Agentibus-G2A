import logging
import pathlib
import time
import traceback
from contextlib import contextmanager
from typing import List

import schedule
from selenium import webdriver
from agentibus import ini_parser
from agentibus.BundleHandlers import HumbleBundleHandler
from agentibus.Product import Game
from agentibus.StoreHandlers import FanaticalHandler, HumbleStoreHandler
from agentibus.TelegramSender import TelegramSender


@contextmanager
def managed_chromedriver(options):
    chrome_driver = webdriver.Chrome(options=options)
    try:
        yield chrome_driver
    finally:
        chrome_driver.quit()


def job():
    pathlib.Path('/logs').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        handlers=[
            logging.FileHandler("/logs/GameDeals.log"),
            logging.StreamHandler()
        ])

    telegram = TelegramSender()
    opts = get_chromedriver_options()
    with managed_chromedriver(opts) as driver:
        driver.set_window_size(1800, 1070)
        driver.implicitly_wait(2)
        fanatical_games: List[Game] = FanaticalHandler.crawl(driver)
        for game in fanatical_games:
            FanaticalHandler.set_game_data(driver, game)
        humble_games: List[Game] = HumbleStoreHandler.crawl(driver)
        for game in humble_games:
            HumbleStoreHandler.set_game_data(game, driver)
        game_list = fanatical_games + humble_games
        for game in game_list:
            if game.profit_margin > ini_parser.get_net_profit_percentage():
                telegram.send(
                    f"Game deal found:\n name: {game.name}\n price: {game.sale_price}\n prifit margin: {game.profit_margin * 100}%\n url: {game.url}")

        humble_bundles = HumbleBundleHandler.crawl(driver)
        for bundle in humble_bundles:
            HumbleBundleHandler.set_bundle_data(driver, bundle)
        bundle_list = humble_bundles
        for bundle in bundle_list:
            if bundle.profit_margin > ini_parser.get_net_profit_percentage():
                telegram.send(
                    f"Bundle deal found:\n name: {bundle.name}\n price: {bundle.sale_price}\n prifit margin: {bundle.profit_margin * 100}%\n url: {bundle.url}")


def get_chromedriver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    return options


def execute():
    schedule.every(6).hours.do(job)
    try:
        job()
    except Exception:
        handle_exception()
    while True:
        try:
            schedule.run_pending()
        except Exception:
            handle_exception()
        time.sleep(30)


def handle_exception():
    time.sleep(60)
    my_stacktrace = traceback.format_exc()
    logging.getLogger().error(my_stacktrace)
    sender = TelegramSender()
    sender.send(my_stacktrace, error_message=True)


if __name__ == '__main__':
    execute()
