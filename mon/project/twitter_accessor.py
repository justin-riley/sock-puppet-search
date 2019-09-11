#!/home/justin/.local/opt/anaconda2/envs/galvanize/bin/python
#%%
import twitter
from collections import OrderedDict as od
from json import dump,load

#%%
twitter_creds={}
with open('/home/justin/.local/cache/twitter/credentials','r') as creds:
    twitter_creds=load(creds)
    # print(twitter_creds)
api=twitter.Api(consumer_key=twitter_creds['TWITTER_API_KEY'],
                consumer_secret=twitter_creds['TWITTER_API_SECRET_KEY'],
                access_token_key=twitter_creds['TWITTER_ACCESS_TOKEN'],
                access_token_secret=twitter_creds['TWITTER_ACCESS_TOKEN_SECRET'])
#%%
api = twitter.Api(consumer_key=secrets['TWITTER_API_KEY'],
consumer_secret=secrets['TWITTER_API_SECRET_KEY'],
access_token_key=secrets['TWITTER_ACCESS_TOKEN'],
access_token_secret=secrets['TWITTER_ACCESS_TOKEN_SECRET'])

#%%
from twython import Twython
import pandas as pd
python_tweets = Twython(twitter_creds['TWITTER_API_KEY'],twitter_creds['TWITTER_API_SECRET_KEY'])
query = {
    'q':'elon musk nuke mars',
    'result_type':'popular',
    'count':100,
    'lang':'en',
}
d = {'user':[],'date':[],'text':[],'favorite_count':[]}
for status in python_tweets.search(**query)['statuses']:
    d['user'].append(status['user']['screen_name'])
    d['date'].append(status['created_at'])
    d['text'].append(status['text'])
    d['favorite_count'].append(status['favorite_count'])
data = pd.DataFrame(d)
data.head()

#%%
from json import dump,load
from twython import Twython

twitter_creds={}
with open('/home/justin/.local/cache/twitter/credentials','r') as creds:
    twitter_creds=load(creds)
tweets = []
NUMBER_OF_ATTEMPTS=20
TARGET_NUMBER_OF_TWEETS_TO_FETCH=500
python_tweets = Twython(twitter_creds['TWITTER_API_KEY'],twitter_creds['TWITTER_API_SECRET_KEY'])
query = {
    'q':'elon musk nuke mars',
    'result_type':'recent',
    'count':100,
    'lang':'en',
}
d = {'user':[],'date':[],'text':[],'favorite_count':[]}
for i in range(NUMBER_OF_ATTEMPTS):

    if len(tweets) > TARGET_NUMBER_OF_TWEETS_TO_FETCH:
        break
    if i == 0:
        results = python_tweets.search(**query)
    else:
        query['max_id']=next_max_id
        results = python_tweets.search(**query)
    for result in results['statuses']:
        d['user'].append(result['user']['screen_name'])
        d['date'].append(result['created_at'])
        d['text'].append(result['text'])
        d['favorite_count'].append(result['favorite_count'])
    try:
        next_results_url_params = results['search_metadata']['next_results']
        next_max_id=next_results_url_params.split('max_id=')[1].split('&')[0]
    except:
        break


#%%

#%%


#%%
