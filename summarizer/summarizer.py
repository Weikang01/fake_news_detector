import os

import config
import pandas as pd


# loop through pkl files in pkl_dir
for filename in os.listdir(config.pkl_dir):
    # load pkl file
    df = pd.read_pickle(os.path.join(config.pkl_dir, filename))

    # loop through each row in pkl file
    print(df.head())