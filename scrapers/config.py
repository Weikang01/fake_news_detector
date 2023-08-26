import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_base_dir = os.path.join(base_dir, "data")

bbc_data_dir = os.path.join(data_base_dir, "bbc")

if not os.path.exists(bbc_data_dir):
    os.makedirs(bbc_data_dir)
