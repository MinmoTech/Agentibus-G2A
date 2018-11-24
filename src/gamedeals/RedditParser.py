import praw

reddit = praw.Reddit('game_deals_bot')
print(reddit.user.me())
