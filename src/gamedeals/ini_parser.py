import configparser


def get_telegram_token():
    parser = configparser.ConfigParser()
    parser.read('./resources/configuration.ini')
    return parser['telegram']['token']


def get_telegram_chat_id():
    parser = configparser.ConfigParser()
    parser.read('./resources/configuration.ini')
    return parser['telegram']['chat_id']
