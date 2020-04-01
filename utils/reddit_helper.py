'''
Created on Mar 29, 2020

@author: rcurtis
'''

import logging
import praw

bot_name='BannerBot'
user_agent='script:BannerBot:0.1 (by u/BourbonInExile)'

# Create the connection to Reddit.
# This assumes a properly formatted praw.ini file exists:
#   https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html
reddit = praw.Reddit(bot_name, user_agent=user_agent)

# Get a handle on our preferred subreddit
subreddit = reddit.subreddit("TrueWetShaving")
