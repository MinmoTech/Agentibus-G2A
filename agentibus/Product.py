from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from agentibus import Utility


@dataclass
class Game:
    url: str = ''
    name: str = ''
    site: str = ''
    review_count: int = 0
    sale_price: Decimal = Decimal(0)
    g2a_price: Decimal = Decimal(0)
    after_commission_price: Decimal = Decimal(0)
    profit_margin = Decimal(0)
    sale_platform: str = 'Steam'


@dataclass
class Bundle:
    url: str = ''
    name: str = ''
    site: str = ''
    games: List[Game] = field(default_factory=list)
    sale_price: Decimal = Decimal(0)
    g2a_price: Decimal = Decimal(0)
    after_commission_price: Decimal = Decimal(0)
    profit_margin = Decimal(0)


def set_game_meta_data(game: Game):
    if game.sale_price != Decimal(0) and game.g2a_price != Decimal(0):
        game.after_commission_price = Utility.calculate_net_price(game.g2a_price)
        if game.after_commission_price != Decimal(0):
            game.profit_margin = Decimal(game.g2a_price / game.after_commission_price)


def set_bundle_meta_data(bundle: Bundle):
    bundle.profit_margin = Decimal(bundle.g2a_price / bundle.after_commission_price)
