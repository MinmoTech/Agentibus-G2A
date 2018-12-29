from decimal import Decimal

from agentibus import Utility
from agentibus.Product import Game

game_mock = Game()
game_mock.sale_price = Decimal(6.80)
game_mock.g2a_price = Decimal(10.60)
game_mock.after_commission_price = Utility.calculate_net_price(game_mock.g2a_price)
game_mock.profit_margin = Decimal((game_mock.after_commission_price - game_mock.sale_price) / game_mock.sale_price)
print(f'game afetr commission price: {game_mock.after_commission_price}')
print(f'game margin: {game_mock.profit_margin}')
