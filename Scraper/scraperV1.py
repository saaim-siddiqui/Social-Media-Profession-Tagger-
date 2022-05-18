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
            os.system("snscrape --jsonl --max-results 10 twitter-search 'from:{}'> user-tweets.json".format(username))
        else:
            continue
        
        # Reads the json generated from the CLI commands above and creates a pandas dataframe
        tweets_df = pd.read_json('user-tweets.json', lines=True)  # storing the fetched data in a dataframe from a json file
        
        
        if(i == 0):
            tweets_df.to_csv(f'../Dataset/raw_tweets_data{header}.csv', mode='a')
        else:
            tweets_df.to_csv(f'../Dataset/raw_tweets_data{header}.csv', mode='a', header=None)
            
            



cleaned_df = pd.read_csv("../Dataset/raw_tweets_datapolitician.csv", skipinitialspace=True)
cleaned_df.columns = cleaned_df.columns.str.rstrip()

scraped_headers = list(cleaned_df)

save_columns = ['content', 'user'] # columns NOT to be dropped  

# cleaning dataset, dropping extra columns

for heading in scraped_headers:
    if heading not in save_columns:
        cleaned_df.drop(heading, axis=1, inplace=True) 


cleaned_df.to_csv('../Dataset/test_tweetv3.csv', mode='a')

# cleaning further data extracting the info we need such as location and bio etc. 

rows = cleaned_df['user']
i = 0
for row in rows:
    row = row.replace("'", "\"")
    row = row.replace("None", "\"\"")
    row = row.replace("True", "1")
    row = row.replace("False", "0")
    row_dict = json.loads(row)
    cleaned_dict = {'url': row_dict['url'], 'description': row_dict['description'], 'verified': row_dict['verified'], 'tweets': cleaned_df.loc[i,'content'], 'location': row_dict['location']}
    temp_df = pd.DataFrame(cleaned_dict, index=[0])

    if(i == 0):
        temp_df.to_csv('/mnt/sda6/Univerisity/Semester 7/Final Year project/CODE/Dataset/cleaned_dataset.csv', mode='a', index=False)
    else :
        temp_df.to_csv('/mnt/sda6/Univerisity/Semester 7/Final Year project/CODE/Dataset/cleaned_dataset.csv', mode='a', index=False, header=None)

    i = i + 1


# To remove row duplicates in the column 

content_df = pd.read_csv("/mnt/sda6/Univerisity/Semester 7/Final Year project/CODE/Dataset/cleaned_dataset.csv", skipinitialspace=True)

i = 0

row_count = len(content_df.index)

for j in range(row_count-1):
    
    tweets = ''
    
    if(i >= row_count-1):
        break
    
    while(content_df.loc[i,'url'] == content_df.loc[i+1,'url']):

        tweets += content_df.loc[i,'tweets'];
            
        content_df.drop([i], inplace = True)   

        i = i+1

        if(i == row_count-1):
            tweets += content_df.loc[i,'tweets'];
            break

            
    content_df.loc[i,'tweets'] = tweets
    i = i+1
   

content_df.to_csv('../Dataset/final_dataser.csv', mode='a')