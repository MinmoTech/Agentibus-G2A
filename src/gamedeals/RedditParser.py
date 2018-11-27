import re
import praw
from praw.models import Submission, MoreComments


class RedditParser:
    def __init__(self):
        self.fanatical_regex = '(?:https?://)?(?:www.)?fanatical.com/[\w|/|+|&|%|-]*'

    def get_sale_urls(self):
        reddit = praw.Reddit('game_deals_bot')
        for submission in reddit.subreddit('GameDeals').new(limit=50):
            print(self.search_for_urls_of_type(self.fanatical_regex, submission))

    @staticmethod
    def search_for_urls_of_type(regex: str, submission: Submission):
        sale_urls = []
        if 'redd' in submission.url:
            site_urls = re.findall(regex, submission.selftext)
            sale_urls.append(site_urls)
        else:
            sale_urls.append(submission.url)
        for top_level_comment in submission.comments:
            if type(top_level_comment) is not MoreComments:
                comment_site_urls = re.findall(regex, top_level_comment.body)
                sale_urls.append(comment_site_urls)
        return sale_urls

# TODO: test
reddit_parser = RedditParser()
reddit_parser.get_sale_urls()
