import telegram

from agentibus import ini_parser


class TelegramSender:
    def __init__(self):
        self.bot = telegram.Bot(ini_parser.get_telegram_token())
        self.MAX_MESSAGE_LENGTH = 4096

    def send(self, message: str):
        self.bot.send_message(ini_parser.get_telegram_chat_id(), message[:self.MAX_MESSAGE_LENGTH], parse_mode='HTML')
        if len(message) > 0:
            message = message[self.MAX_MESSAGE_LENGTH:]
            self.send(ini_parser.get_telegram_chat_id(), message[:self.MAX_MESSAGE_LENGTH], parse_mode='HTML')
