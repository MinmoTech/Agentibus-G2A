import configparser


def get_client_id():
    parser = configparser.ConfigParser()
    parser.read('./praw.ini')
    return parser['default']['client_id']


def get_client_secret():
    parser = configparser.ConfigParser()
    parser.read('./praw.ini')
    return parser['default']['client_secret']


def get_password():
    parser = configparser.ConfigParser()
    parser.read('./praw.ini')
    return parser['default']['password']


def get_username():
    parser = configparser.ConfigParser()
    parser.read('./praw.ini')
    return parser['default']['username']
