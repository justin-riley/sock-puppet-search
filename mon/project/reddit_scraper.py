#%%
from requests.auth import HTTPBasicAuth
from requests import auth,post, get
from json import load
from praw import Reddit
from copy import deepcopy
from datetime import datetime
from pandas import DataFrame

creds = {}
CREDENTIALS_FILE = '/home/justin/.local/cache/reddit/info'
with open(CREDENTIALS_FILE,'r') as info:
    creds = load(info)

client_auth = HTTPBasicAuth(creds['ID'],creds['SECRET'])
post_data = {'grant_type':'password','username':creds['USER'],'password':creds['PASS']}
headers = {'User-Agent':creds['AGENT']}
response = post('https://www.reddit.com/api/v1/access_token',auth=client_auth,data=post_data,headers=headers)
token = response.json()['access_token']

headers = {"Authorization": token, "User-Agent": creds['AGENT']}
response = get("https://oauth.reddit.com/api/v1/me", headers=headers)

reddit = Reddit(client_id=creds['ID'],
                client_secret=creds['SECRET'],
                user_agent = creds['AGENT'],
                username = creds['USER'],
                password = creds['PASS'])
#%%
info = {'author':[], 'url':[],'body':[],'subreddit':[],
        'submission_author':[],'sub_id':[],'comment_id':[],
        'comment_permalink':[],'submission_permalink':[],
        'date':[]}
backup = deepcopy(info)
i = 0
directory = '/home/justin/.local/share/xdg/media/documents/textfiles/galvanize/w4'
day = 'wed'
file = 'reddit_data'
j = 0

for subreddit in ['tech','technewstoday','politics','news']:
    subr = reddit.subreddit(subreddit)
    for submission in subr.search('elon musk'):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if i % 500 == 0:
                print(comment.permalink)
                print(submission.permalink)
                print(i)
            if i % 5000 == 0:
                print(comment.author)
                print(comment.body)
                print(i)
                print()
                DataFrame(info).to_csv(f'{directory}/{day}/{file}_{str(j)}.csv')
                j += 1
                for keys in info:
                    backup[keys].extend(info[keys])
                    info[keys] = []
                print('info length = ',len(info['author']))
                print('backup length = ',len(backup['author']))
            if not comment.author:
                info['author'].append('None')
            else:
                info['author'].append(comment.author.name)
            info['body'].append(comment.body)
            info['subreddit'].append(submission.subreddit.display_name)
            info['submission_author'].append(submission.author_fullname)
            info['sub_id'].append(submission.id)
            info['url'].append(submission.url)
            info['comment_id'].append(comment.id)
            info['comment_permalink'].append(comment.permalink)
            info['submission_permalink'].append(submission.permalink)
            info['date'].append(datetime.utcfromtimestamp(comment.created))

            i += 1
#%%