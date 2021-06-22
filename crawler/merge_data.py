import glob
import os

import pandas as pd


# This is the base directory for combining
def merge_authors(config):
    path = config["storage"]["path"]
    df_list = []
    for file in glob.glob(path + "/*.csv", recursive=True):
        temp_df = pd.read_csv(file)
        df_list.append(temp_df)

    combined_df = pd.concat(df_list)
    # output is created manually within datadir
    combined_df = combined_df.sort_values(by='hindex5y', ascending=False)
    combined_df.to_csv(os.path.join(path, "combined_authors.csv"))
