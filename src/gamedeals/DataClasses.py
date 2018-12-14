from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Dict


@dataclass
class Game:
    url: str = ''
    name: str = ''
    site: str = ''
    review_count: int = 0
    sale_price: Decimal = Decimal(0)
    g2a_price: Decimal = Decimal(0)
    sale_platform: str = 'Steam'


@dataclass
class Bundle:
    url: str = ''
    name: str = ''
    site: str = ''
    games: List[Game] = field(default_factory=list)
    sale_price: Decimal = Decimal(0)
    g2a_price: Decimal = Decimal(0)
    g2a_price_after_deductions: Decimal = Decimal(0)

