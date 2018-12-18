import configparser
import os


def get_telegram_token():
    parser = configparser.ConfigParser()
    parser.read(f"{os.environ['AGENTIBUS_RESOURCES']}/configuration.ini")
    return parser['telegram']['token']


def get_telegram_chat_id():
    parser = configparser.ConfigParser()
    parser.read(f"{os.environ['AGENTIBUS_RESOURCES']}/configuration.ini")
    return parser['telegram']['chat_id']


def get_net_profit_percentage():
    parser = configparser.ConfigParser()
    parser.read(f"{os.environ['AGENTIBUS_RESOURCES']}/configuration.ini")
    return parser['default']['net_profit_percentage']
