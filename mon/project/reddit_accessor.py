#%%
import requests
import requests.auth
from json import load
creds = {}
with open('/home/justin/.local/cache/reddit/info','r') as credentials:
    creds = load(credentials)
client_auth = requests.auth.HTTPBasicAuth(creds['ID'],creds['SECRET'])
post_data = {'grant_type':'password','username':creds['USER'],'password':creds['PASS']}
headers = {'User-Agent':creds['AGENT']}
response = requests.post('https://www.reddit.com/api/v1/access_token',auth=client_auth,data=post_data,headers=headers)
response.json()
token = response.json()['access_token']

#%%

headers = {"Authorization": token, "User-Agent": creds['AGENT']}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
#%%

#%%
from json import loads,dump
from praw import Reddit
reddit = Reddit(client_id=creds['ID'],
                client_secret=creds['SECRET'],
                user_agent = creds['AGENT'],
                username = creds['USER'],
                password = creds['PASS'])
print(reddit.read_only)

#%%
subreddits = ['news','tech','technewstoday','politics']

sub = reddit.subreddit('news')
for submissions in sub.search('elon musk'):
    

#%%
locals()

#%%
print(token)
#%%
