import requests
from bs4 import BeautifulSoup
from pipeline.scrapers.utils import *


class BBCSearchScraper:
    url = "https://www.bbc.co.uk/search?q={keyword}&page={page}"

    def search(self, keyword, top_n=10):
        response = requests.get(self.url.format(keyword=keyword, page=1))

        if response.status_code == 200:
            page_content = response.content.decode("utf-8")

            soup = BeautifulSoup(page_content, "html.parser")
            container = soup.find('div', class_='ssrcss-1izxn3x-NumberedPagesButtonsContainer')
            last_page_link = container.find_all('a')[-1]

            # Get the number from the link text
            last_page_number = int(last_page_link.get_text(strip=True))

            titles = []
            texts = []

            while len(titles) < top_n:
                for page_number in range(1, last_page_number + 1):
                    response = requests.get(self.url.format(keyword=keyword, page=page_number))

                    if response.status_code == 200:
                        page_content = response.content.decode("utf-8")

                        soup = BeautifulSoup(page_content, "html.parser")
                        a_tag = soup.find_all('a', class_='ssrcss-its5xf-PromoLink')

                        for a in a_tag:
                            href = a.get('href')
                            title = a.get_text(strip=True)
                            print("Title:", title)
                            print("Href:", href)
                            print("-" * 50)
                            response = requests.get(href)
                            soup = BeautifulSoup(response.content, "html.parser")
                            paragraphs = soup.find_all('p', class_='ssrcss-1s3rf6l-Paragraph')
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

            return pd.DataFrame({"title": titles, "text": texts})


if __name__ == '__main__':
    scraper = BBCSearchScraper()
    print(scraper.search("coronavirus", top_n=10))
