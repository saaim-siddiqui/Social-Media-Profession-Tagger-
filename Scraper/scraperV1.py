import os

import pandas as pd

test_df = pd.read_csv("dataset.csv", skipinitialspace=True)
test_df.columns = test_df.columns.str.rstrip()

headers = list(test_df)
print(headers)

for header in headers:
    for i in range(len(test_df[header])):
        username = test_df.loc[i, header]
        if(username.startswith('@')):
        # Using OS library to call CLI commands in Python
            os.system("snscrape --jsonl --max-results 1 twitter-search 'from:{}'> user-tweets.json".format(username))
        else:
            continue
        # Reads the json generated from the CLI commands above and creates a pandas dataframe
        tweets_df = pd.read_json('user-tweets.json', lines=True)
        # print(tweets_df)
        tweets_df.to_csv('test_tweetv2.csv', mode='a')

# {'_type': 'snscrape.modules.twitter.User', 'username': 'SuicidalPastaa', 'id': 1073837574999998465, 'displayname': 'IDONTKNOW', 'description': "let's all drift into oblivion \nPronouns: was/were", 'rawDescription': "let's all drift into oblivion \nPronouns: was/were", 'descriptionUrls': None, 'verified': False, 'created': '2018-12-15T07:10:03+00:00', 'followersCount': 30, 'friendsCount': 139, 'statusesCount': 575, 'favouritesCount': 2795, 'listedCount': 0, 'mediaCount': 10, 'location': 'oblivion', 'protected': False, 'linkUrl': None, 'linkTcourl': None, 'profileImageUrl': 'https://pbs.twimg.com/profile_images/1300330701527683072/HKDJVGpC_normal.jpg', 'profileBannerUrl': 'https://pbs.twimg.com/profile_banners/1073837574999998465/1596345683', 'label': None, 'url': 'https://twitter.com/SuicidalPastaa'}
