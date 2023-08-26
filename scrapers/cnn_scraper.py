import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from html import unescape
from config import pkl_dir
from utils import *

url = 'https://www.cnn.com'

response = requests.get(url)

# save_html(pkl_dir, 'cnn', response)

soup = BeautifulSoup(response.content, "html.parser")

# Find the <a> element
link_elements = soup.find_all("a", class_="container__link")

# Initialize lists to store titles and hrefs
titles = []
hrefs = []

# Extract titles and hrefs from link_elements that have both attributes
for link_element in link_elements:
    title_span = link_element.find("span", {"data-editable": "headline"})
    if title_span and "href" in link_element.attrs:
        href = link_element.get("href")
        if href.startswith("/"):
            titles.append(sanitize_filename(title_span.get_text(" ", strip=True)))
            hrefs.append(urljoin(url, href))

# Print the extracted titles and hrefs
for title, href in zip(titles, hrefs):
    print("Title:", title)
    print("Href:", href)
    print("---")

    # send request to the href
    response = requests.get(href)




    break
