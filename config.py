import os

openai_api_key = os.environ.get("OPENAI_API_KEY")

base_dir = os.path.dirname(os.path.abspath(__file__))

data_base_dir = os.path.join(base_dir, "data")
pkl_dir = os.path.join(data_base_dir, "pkl")


