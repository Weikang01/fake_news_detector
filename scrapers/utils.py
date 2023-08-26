import os
import re
import config
import pandas as pd


def sanitize_filename(filename):
    # Remove invalid characters from filename
    return re.sub(r'[\\/*?:"<>|]', '', filename)


def save_html(base_dir, title, response):
    with open(os.path.join(base_dir, f"{sanitize_filename(title)}.html"), "w", encoding="utf-8") as f:
        f.write(response.content.decode("utf-8"))


def generate_raw_pkl(base_dir, paragraphs, title):
    paragraphs = [p.get_text(" ", strip=True).replace("\n", " ") for p in paragraphs]
    data = {"text": paragraphs}
    df = pd.DataFrame(data)
    df.to_pickle(os.path.join(base_dir, f"{sanitize_filename(title)}.pkl"))
