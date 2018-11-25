import re
import praw

from src.gamedeals.FanaticalHandler import FanaticalHandler

fanatical_regex = '(?:https?://)?(?:www.)?fanatical.com/[\w|/|+|&|%|-]*'

reddit = praw.Reddit('game_deals_bot')
for submission in reddit.subreddit('GameDeals').new(limit=50):

    if 'reddit' in submission.url:
        fanatical_urls = re.findall(fanatical_regex, submission.selftext)
    else:
        if 'fanatical' in submission.url:
            fanatical_handler = FanaticalHandler
            fanatical_handler.get_page(submission.url)

