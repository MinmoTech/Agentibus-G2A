import requests
from bs4 import BeautifulSoup

reddit_page = requests.get("https://old.reddit.com/r/GameDeals/")
reddit_soup = BeautifulSoup(reddit_page.content, 'html.parser')
print(reddit_soup.prettify())
