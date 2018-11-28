import logging
from abc import abstractmethod, ABC
from decimal import Decimal
from typing import List

from selenium import webdriver

from src.gamedeals import Utility
from src.gamedeals.G2AHandler import G2AHandler


class BundleHandler(ABC):
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url
        self.logger = logging.getLogger()

    def get_total_g2a_price_after_deductions(self):
        game_names = self.get_game_names()
        total_price = Decimal(0.0)
        for game_name in game_names:
            g2a_handler = G2AHandler(self.driver)
            g2a_net_price = Utility.calculate_net_price(g2a_handler.lookup_price_of(game_name))
            logging.info(f'{game_name} G2A net price (after sale deductions): {g2a_net_price}')
            total_price += g2a_net_price
        return Decimal(total_price)

    @abstractmethod
    def get_game_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_total_sale_price(self) -> Decimal:
        pass
