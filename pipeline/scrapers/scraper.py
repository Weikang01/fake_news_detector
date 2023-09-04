from pipeline.scrapers.bbc_search_scraper import BBCSearchScraper
from pipeline.scrapers.cnn_search_scraper import CNNSearchScraper
import pandas as pd


class Scraper:
    def __init__(self):
        self.scrapers = [BBCSearchScraper(), CNNSearchScraper()]

    def search(self, keyword, top_n=10):
        documents = []
        for scraper in self.scrapers:
            documents.append(scraper.search(keyword, top_n))
        return pd.concat(documents)


if __name__ == '__main__':
    scraper = Scraper()
    print(scraper.search('trump', 10))
