import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pipeline.config import pkl_dir
from utils import *

url = 'https://www.cnn.com'

response = requests.get(url)

# save_html(pkl_dir, 'cnn', response)

soup = BeautifulSoup(response.content, "html.parser")

# Find the <a> element
link_elements = soup.find_all("a", class_="container__link")

href_pattern = re.compile(r'^/\d{4}/[^?]+/index\.html$')

# Initialize lists to store titles and hrefs
titles = []
hrefs = []
texts = []

# Extract titles and hrefs from link_elements that have both attributes
for link_element in link_elements:
    title_span = link_element.find("span", {"data-editable": "headline"})
    if title_span and "href" in link_element.attrs:
        href = link_element.get("href")
        if href and href_pattern.match(href):
            decoded_title = sanitize_filename(title_span.get_text(" ", strip=True))
            href = urljoin(url, href)

            print("Title:", decoded_title)
            print("Href:", href)
            print("-" * 50)

            response = requests.get(href)

            soup = BeautifulSoup(response.content, "html.parser")

            paragraphs = soup.find_all("p", class_="paragraph")

            paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]

            if len(paragraphs) == 0:
                paragraphs = soup.find_all("p")

                soup.find_all("span", class_="zn-body__paragraph")

                paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]

                if len(paragraphs) == 0:
                    continue

            paragraphs = "\n".join(paragraphs)

            titles.append(decoded_title)
            texts.append(paragraphs)

df = pd.DataFrame({"title": titles, "text": texts})

df.to_pickle(os.path.join(pkl_dir, "cnn.pkl"))
