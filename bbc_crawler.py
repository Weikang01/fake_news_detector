import requests
import re
from urllib.parse import urljoin
from html import unescape

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

        break
else:
    print("Failed to retrieve the webpage")
