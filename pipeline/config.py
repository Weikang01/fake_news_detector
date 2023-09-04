import os
import openai

openai_api_key = os.environ.get("OPENAI_API_KEY")
if openai_api_key is None:
    print("OPENAI_API_KEY environment variable is not set.")

openai.api_key = openai_api_key

base_dir = os.path.dirname(os.path.abspath(__file__))

data_base_dir = os.path.join(base_dir, "data")
pkl_dir = os.path.join(data_base_dir, "pkl")


