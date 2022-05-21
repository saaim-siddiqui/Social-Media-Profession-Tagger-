import os
# from numpy import save
import json
import pandas as pd

# Reading the dataset 
dataset_df = pd.read_csv("./Dataset/dataset.csv", skipinitialspace=True)
dataset_df.columns = dataset_df.columns.str.rstrip() # removing spaces before column names
headers = list(dataset_df) # storing header names of all columns 

# looping each column until dataset for all columns is fetched. 
for header in headers:
    for i in range(len(dataset_df[header])):   # loop until whole column is scanned
        username = dataset_df.loc[i, header]   # storing username of a cell
        username = str(username)               # converting username to string 
        if(username.startswith('@')):
        # Using OS library to call CLI commands in Python
            os.system("snscrape --jsonl --max-results 10 twitter-search 'from:{}'> user-tweets.json".format(username))
        else:
            continue
        
        # Reads the json generated from the CLI commands above and creates a pandas dataframe
        tweets_df = pd.read_json('user-tweets.json', lines=True)  # storing the fetched data in a dataframe from a json file
        
        
        if(i == 0):
            tweets_df.to_csv(f'./Dataset/raw_tweets_data{header}.csv', mode='a')
        else:
            tweets_df.to_csv(f'./Dataset/raw_tweets_data{header}.csv', mode='a', header=None)