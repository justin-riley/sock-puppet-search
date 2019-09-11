from json import load
from praw import Reddit
from json import load
from requests import post,get
from requests.auth import HTTPBasicAuth
from os import getcwd,mkdir
from pandas import DataFrame
from copy import deepcopy
# class RedditScraper:
#     def __init__(self, credentials_file='/home/justin/.local/cache/reddit/info'):
#          with open(credentials_file,'r') as credentials:
#             self.creds = load(credentials)
def get_reddit_instance(self):
    """
    Opens credentials file, then creates and returns a reddit instance.
    Parameters:
    -----------
    creds_file: str:
    String representation of path to json file that contains required information
    for connecting to reddit.
    """
    # client_auth = HTTPBasicAuth(creds['ID'],creds['SECRET'])
    # post_data = {'grant_type':'password','username':creds['USER'],'password':creds['PASS']}
    # headers = {'User-Agent':creds['AGENT']}
    # response = post('https://www.reddit.com/api/v1/access_token',auth=client_auth,data=post_data,headers=headers)
    # token = response.json()['access_token']
    return Reddit(client_id=self.creds['ID'], client_secret=self.creds['SECRET'],\
        user_agent=self.creds['AGENT'],username=self.creds['USER'],password=self.creds['PASS'])

def build_dic(self, subreddit_list, search_term, path_to_file=None, \
            file_name='reddit_data_by_subreddit_{j}.csv',j=0):
    """
    Function that creates a dictionary of relevant reddit data.
    parameters:
    -----------
    subreddit_list: list:
    list {:str} of subreddits to search
    search_term: str:
    tearm to look for in each subreddit
    path_to_file: str:
    string representation of directory where backups of
    scrated data will be stored
    file_name: str:
    string represenation of the name of the file where
    backup data will be saved.  j will be incremented
    after every 5000 interations, then be used to create a
    unique file name
    j: int:
    integer placeholder to give unique filenames.
    """
    i=1
    info = {'author':[], 'url':[],'body':[],'subreddit':[],
        'submission_author':[],'sub_id':[],'comment_id':[],
        'comment_permalink':[],'submission_permalink':[]}
    backup = deepcopy(info)
    if not path_to_file:
        path_to_file = getcwd() + '/backup_data'
        mkdir(path_to_file)
    reddit = self.get_reddit_instance()
    for subreddit in subreddit_list:
        subr = reddit.subreddit(subreddit)
        for submission in subr.search(search_term):
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if i % 5000 == 0:
                    DataFrame(info).to_csv(path_to_file + \
                        file_name.format(j=j))
                    j += 1
                    for keys in info:
                        backup[keys].extend(info[keys])
                        info[keys] = []                
                if not comment.author:
                    info[keys].append('None')
                else:
                    info[keys].append(comment.author.name)
                info['body'].append(comment.body)
                info['subreddit'].append(submission.subreddit.display_name)
                info['submission_author'].append(submission.author_fullname)
                info['sub_id'].append(submission.id)
                info['url'].append(submission.url)
                info['comment_id'].append(comment.id)
                info['comment_permalink'].append(comment.permalink)
                info['submission_permalink'].append(submission.permalink)
                i += 1
    for keys in info:
        backup[keys].extend(info[keys])
    del info
    DataFrame(backup).to_csv(path_to_file + file_name.format(j='all_data_collected'))
    return backup