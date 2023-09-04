import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from html import unescape
from pipeline.config import pkl_dir
from pipeline.scrapers.utils import *

url = "https://www.bbc.com/news"  # BBC News URL

response = requests.get(url)

PAGE_TYPE_LIVE = "live"
PAGE_TYPE_ARTICLE = "article"

excluded_classes = {
    PAGE_TYPE_LIVE: [
        "qa-sign-in-dialog__description",
        "lx-c-sign-in-dialog__message",
        "qa-tv-licence-subheading",
        "lx-commentary__meta-reporter",
        "lx-commentary__meta-timezone",
        "qa-contributor-name",
        "qa-contributor-role"
    ]
}

if response.status_code == 200:

    titles = []
    texts = []

    page_content = response.content.decode("utf-8")

    # Use regex to find all news titles and href attributes within the specified HTML structure
    news_pattern = r'<a class="gs-c-promo-heading.*?href="(.*?)">.*?<h3.*?>(.*?)<\/h3>'
    news_matches = re.findall(news_pattern, page_content, re.DOTALL)

    for href, title in news_matches:
        cleaned_title = re.sub(r'\s+', ' ', title.strip())

        page_type = None

        print("href:", href)

        if not href[-1].isdigit():
            continue

        if href.startswith("/"):
            if href.startswith("/news/"):
                page_type = "article"
            if href.startswith("/news/live/"):
                page_type = "live"
            full_href = urljoin(url, href)
        else:
            full_href = href

        # Decode HTML entities in the title
        decoded_title = unescape(cleaned_title)

        if decoded_title in titles:
            print("Duplicate title:", decoded_title)
            continue

        print("Title:", decoded_title)
        print("Href:", full_href)
        print("-" * 50)

        # send request to the full_href

        response = requests.get(full_href)

        page_content = response.content

        soup = BeautifulSoup(page_content, "html.parser")

        # Find paragraphs excluding those with the specified classes
        if response.status_code == 200:
            if page_type is PAGE_TYPE_LIVE:
                paragraphs = [
                    p for p in soup.find_all("p", attrs={"data-reactid": True})
                    if not any(excluded_class in p.get("class", []) for excluded_class in excluded_classes[page_type])
                ]

                paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]
                paragraphs = "\n".join(paragraphs)

                titles.append(decoded_title)
                texts.append(paragraphs)

            elif page_type is PAGE_TYPE_ARTICLE:
                paragraphs = []
                for p in soup.find_all("p", class_=["ssrcss-1q0x1qg-Paragraph", "ssrcss-hmf8ql-BoldText"]):
                    paragraphs.append(p)

                paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]
                paragraphs = "\n".join(paragraphs)

                titles.append(decoded_title)
                texts.append(paragraphs)

    df = pd.DataFrame({"title": titles, "text": texts})

    df.to_pickle(os.path.join(pkl_dir, "bbc.pkl"))
    print("Done")
else:
    print("Failed to retrieve the webpage")
