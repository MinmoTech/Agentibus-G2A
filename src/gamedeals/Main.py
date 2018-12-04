import logging
import pathlib
from decimal import Decimal
from selenium import webdriver
from src.gamedeals import Utility, ini_parser
from src.gamedeals.StoreHandlers.FanaticalHandler import FanaticalHandler
from src.gamedeals.G2AHandler import G2AHandler
from src.gamedeals.SteamHandler import SteamHandler

if __name__ == "__main__":
    pathlib.Path('./logs').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        handlers=[
            logging.FileHandler("./logs/GameDeals.log"),
            logging.StreamHandler()
        ])
    logger = logging.getLogger()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1800, 1070)
    driver.implicitly_wait(2)
    fanatical_handler = FanaticalHandler(driver, 'https://www.fanatical.com/en/game/endless-space-2-collection')
    game_name = Utility.filter_special_characters(fanatical_handler.get_game_name())
    sale_price = fanatical_handler.get_sale_price()
    steam_handler = SteamHandler(driver)
    if steam_handler.get_game_review_number(game_name) > 1000:
        g2a_handler = G2AHandler(driver)
        g2a_price = g2a_handler.lookup_price_of(game_name)
        if g2a_price is not None:
            after_commission_price = Utility.calculate_net_price(sale_price)
            logger.info(f'G2A price: {g2a_price}')
            logger.info(f'Price after commission: {after_commission_price}')
            price_cut = Decimal(after_commission_price / g2a_price)
            logger.info(f'Profit for this deals: {price_cut*100}%')
            if price_cut < ini_parser.get_net_profit_percentage():
                print('this should send a telegram message!')
