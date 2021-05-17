import pandas as pd
import numpy as np
import glob
import os
# This is the base directory for combining
data_dir = "data_dir"
df_list = []
for file in glob.glob(data_dir + "/*.csv", recursive=True):
    author_name = file.split("/")[len(file.split("/")) - 1].split(".")[0]
    temp_df = pd.read_csv(file, delimiter=";")
    temp_df['author_name'] = author_name
    df_list.append(temp_df)

combined_df = pd.concat(df_list)
# output is created manually within datadir
combined_df=combined_df.sort_values(by='hindex5y', ascending=False)
combined_df.to_csv(data_dir + "/output/combined_authors.csv")
