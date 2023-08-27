import json
import math

import requests
from bs4 import BeautifulSoup
from .utils import *


class CNNSearchScraper:
    url = 'https://search.prod.di.api.cnn.io/content?q={keyword}&size=10&from=0&page={page}&sort=relevance&types=article'

    def search(self, keyword, top_n=10):
        response = requests.get(self.url.format(keyword=keyword, page=1))

        if response.status_code == 200:
            page_content = response.content.decode("utf-8")

            json_data = json.loads(page_content)

            last_page_number = math.floor(json_data['meta']['total'] / 10)

            titles = []
            texts = []

            while len(titles) < top_n:
                for page_number in range(1, last_page_number + 1):
                    response = requests.get(self.url.format(keyword=keyword, page=page_number))

                    if response.status_code == 200:
                        page_content = response.content.decode("utf-8")

                        json_data = json.loads(page_content)

                        for result in json_data['result']:
                            title = result['headline']
                            href = result['url']
                            print("Title:", title)
                            print("Href:", href)
                            print("-" * 50)
                            response = requests.get(href)
                            soup = BeautifulSoup(response.content, "html.parser")
                            paragraphs = soup.find_all('div', class_='zn-body__paragraph')
                            paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]
                            if len(paragraphs) == 0:
                                paragraphs = soup.find_all("p")
                                paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]
                                if len(paragraphs) == 0:
                                    continue
                            paragraphs = "\n".join(paragraphs)
                            titles.append(title)
                            texts.append(paragraphs)
                            if len(titles) == top_n:
                                break
                        if len(titles) == top_n:
                            break
                    if len(titles) == top_n:
                        break
                if len(titles) == top_n:
                    break

            return pd.DataFrame({'title': titles, 'text': texts})


if __name__ == '__main__':
    scraper = CNNSearchScraper()
    print(scraper.search('coronavirus', top_n=10))
