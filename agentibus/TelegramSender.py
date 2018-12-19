import telegram

from agentibus import ini_parser


class TelegramSender:
    def __init__(self):
        self.bot = telegram.Bot(ini_parser.get_telegram_token())
        self.MAX_MESSAGE_LENGTH = 4084

    def send(self, message: str, code_in_message=False):
        if code_in_message:
            self.bot.send_message(ini_parser.get_telegram_chat_id(),
                                  f'<code>{message[:self.MAX_MESSAGE_LENGTH]}</code>',
                                  parse_mode='HTML')
            message = message[self.MAX_MESSAGE_LENGTH:]
            if len(message) > 0:
                self.send(f'<code>{message[:self.MAX_MESSAGE_LENGTH]}</code>')
        else:
            self.bot.send_message(ini_parser.get_telegram_chat_id(), message[:self.MAX_MESSAGE_LENGTH],
                                  parse_mode='HTML')
            message = message[self.MAX_MESSAGE_LENGTH:]
            if len(message) > 0:
                self.send(message[:self.MAX_MESSAGE_LENGTH])