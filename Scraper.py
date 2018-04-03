from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import re

class Article():
    def __init__(self, snopes_url, snopes_title):
        self.snopes_url = snopes_url
        self.snopes_title = snopes_title

        self.article_title = None
        self.article_link = None

        self.snopes_tags = []
        self.snopes_rating = None

    def visible(element):
        # https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    def get_text(self):
        # https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages
        raw_html = requests.get(self.article_url).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        return list(map(lambda x: (x["href"], x.select("h2")[0]), soup.select(".list-wrapper a")))

class Snopes_Scraper():
    def __init__(self):
        self.BASE_URL = 'https://www.snopes.com/fact-check/'
        self.current_page = 1

    def build_url(self):
        if self.current_page == 1:
            return self.BASE_URL
        else:
            return self.BASE_URL + 'page/' + str(self.current_page)

    def get_next_group(self):
        raw_html = requests.get(self.build_url()).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        self.current_page = self.current_page + 1
        return self.parse_raw_group(soup)

    def parse_raw_group(self, soup):
        return list(map(lambda x: Article(x["href"], x.select("h2")[0].text), soup.select(".list-wrapper a")))

if __name__ == '__main__':
    scraper = Snopes_Scraper()
    articles = scraper.get_next_group() + scraper.get_next_group()
    for title in map(lambda x: x.snopes_title, articles):
        print(title)
