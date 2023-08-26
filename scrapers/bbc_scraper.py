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

if response.status_code == 200:
    page_content = response.content.decode("utf-8")

    # Use regex to find all news titles and href attributes within the specified HTML structure
    news_pattern = r'<a class="gs-c-promo-heading.*?href="(.*?)">.*?<h3.*?>(.*?)<\/h3>'
    news_matches = re.findall(news_pattern, page_content, re.DOTALL)

    for href, title in news_matches:
        cleaned_title = re.sub(r'\s+', ' ', title.strip())

        # Check if href is a partial URL and adjust accordingly
        if href.startswith("/"):
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

        # # save html
        # if response.status_code == 200:
        #     with open(os.path.join(bbc_data_dir, f"{decoded_title}.html"), "w", encoding="utf-8") as f:
        #         f.write(response.content.decode("utf-8"))

        soup = BeautifulSoup(page_content, "html.parser")

        excluded_classes = [
            "qa-sign-in-dialog__description",
            "lx-c-sign-in-dialog__message",
        ]

        # Find paragraphs excluding those with the specified classes
        paragraphs = [
            p.get_text(" ", strip=True).replace("\n", " ")
            for p in soup.find_all("p", attrs={"data-reactid": True})
            if not any(excluded_class in p.get("class", []) for excluded_class in excluded_classes)
        ]

        # print(paragraphs[0])

        for paragraph in paragraphs:
            print(paragraph)
            print("-" * 50)
        break
else:
    print("Failed to retrieve the webpage")
