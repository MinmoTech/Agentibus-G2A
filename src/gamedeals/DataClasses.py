from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict


@dataclass
class Game:
    url: str
    name: str
    site: str
    review_count: int
    sale_price: Decimal
    g2a_price: Decimal
    sale_platform: str = 'Steam'


@dataclass
class Bundle:
    url: str
    games: List[Game]
    sale_price: Decimal
    g2a_price: Decimal
