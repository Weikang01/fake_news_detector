from pipeline.scrapers import Scraper
from pipeline.comparators import EmbeddingComparator
from pipeline.keyword_extractor import EmbeddingExtractor


class API:
    def __init__(self):
        self.scraper = Scraper()
        self.comparator = EmbeddingComparator()
        self.extractor = EmbeddingExtractor()


if __name__ == '__main__':
    api = API()
