import os.path

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from html import unescape
from config import bbc_data_dir
import pandas as pd
import pickle

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
    page_content = response.content.decode("utf-8")

    # Use regex to find all news titles and href attributes within the specified HTML structure
    news_pattern = r'<a class="gs-c-promo-heading.*?href="(.*?)">.*?<h3.*?>(.*?)<\/h3>'
    news_matches = re.findall(news_pattern, page_content, re.DOTALL)

    for href, title in news_matches:
        cleaned_title = re.sub(r'\s+', ' ', title.strip())

        page_type = None

        print("href:", href)

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
            elif page_type is PAGE_TYPE_ARTICLE:
                # save html
                # with open(os.path.join(bbc_data_dir, f"{decoded_title}.html"), "w", encoding="utf-8") as f:
                #     f.write(response.content.decode("utf-8"))

                paragraphs = []
                for p in soup.find_all("p", class_=["ssrcss-1q0x1qg-Paragraph", "ssrcss-hmf8ql-BoldText"]):
                    paragraphs.append(p)

                # for b in soup.find_all("b", class_="ssrcss-hmf8ql-BoldText"):
                #     paragraphs.append(b)

                print(paragraphs[-2])
                print(paragraphs[-1])
                print("-" * 50)

                for idx, paragraph in enumerate(paragraphs):
                    paragraph_text = paragraph.get_text(" ", strip=True).replace("\n", " ")
                    print(f"Paragraph {idx}: {paragraph_text}")
                    print("-" * 50)

                break

        # paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]
        #
        # data = {"text": paragraphs}
        # df = pd.DataFrame(data)
        #
        # df.to_pickle(os.path.join(bbc_data_dir, f"{decoded_title}.pkl"))

else:
    print("Failed to retrieve the webpage")
