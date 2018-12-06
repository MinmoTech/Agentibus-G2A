from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict


@dataclass
class Game:
    url: str
    name: str
    site: str
    sale_price: Decimal
    g2a_price: Decimal


@dataclass
class Bundle:
    url: str
    games: List[str]
    game_singe_prices: Dict[str, Decimal]
    site: str
    sale_price: Decimal
    g2a_price: Decimal
