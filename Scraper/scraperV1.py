import os
# from numpy import save
import json
import pandas as pd

# Reading the dataset 
dataset_df = pd.read_csv("../Dataset/test-dataset.csv", skipinitialspace=True)
dataset_df.columns = dataset_df.columns.str.rstrip() # removing spaces before column names
headers = list(dataset_df) # storing header names of all columns 

# looping each column until dataset for all columns is fetched. 
for header in headers:
    for i in range(len(dataset_df[header])):   # loop until whole column is scanned
        username = dataset_df.loc[i, header]   # storing username of a cell
        
        if(username.startswith('@')):
        # Using OS library to call CLI commands in Python
            os.system("snscrape --jsonl --max-results 1 twitter-search 'from:{}'> user-tweets.json".format(username))
        else:
            continue
        
        # Reads the json generated from the CLI commands above and creates a pandas dataframe
        tweets_df = pd.read_json('user-tweets.json', lines=True)  # storing the fetched data in a dataframe from a json file
        tweets_df.to_csv('../Dataset/test_tweetv2.csv', mode='a')


cleaned_df = pd.read_csv("../Dataset/test_tweetv2.csv", skipinitialspace=True)
cleaned_df.columns = cleaned_df.columns.str.rstrip()

scraped_headers = list(cleaned_df)

save_columns = ['content', 'user'] # columns NOT to be dropped  

for heading in scraped_headers:
    if heading not in save_columns:
        cleaned_df.drop(heading, axis=1, inplace=True) # cleaning dataset, dropping extra columns


cleaned_df.to_csv('../Dataset/test_tweetv3.csv', mode='a')


rows = cleaned_df['user']
i = 0
for row in rows:
    row = row.replace("'", "\"")
    row = row.replace("None", "\"\"")
    row = row.replace("True", "1")
    row = row.replace("False", "0")
    row_dict = json.loads(row)
    cleaned_dict = {'url': row_dict['url'], 'description': row_dict['description'], 'verified': row_dict['verified'], 'tweets': cleaned_df.loc[i,'content']}
    temp_df = pd.DataFrame(cleaned_dict, index=[0])
    temp_df.to_csv('../Dataset/cleaned_dataset.csv', mode='a', index=False)
    i = i + 1