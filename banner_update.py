#!/usr/local/bin/python3
# coding: utf-8

'''
Created on Mar 29, 2020

@author: rcurtis
'''
import logging

logging.basicConfig(filename='BannerBot.log', level=logging.DEBUG, 
                    format='%(asctime)s :: %(levelname)s :: %(threadName)s :: %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')
import os

from datetime import datetime
from utils.imgur_helper import download_as
from utils.reddit_helper import reddit


def exec_update():
    logging.info('Connected to Reddit instance as [%s]', reddit.user.me())
    
    logging.info('Clean up old banner and sidebar files if they exist')
    
    logging.info('Fetch winning images')
    subreddit = reddit.subreddit('Wetshaving')
    winners = subreddit.search(query="weekly contest results", sort="new", time_filter="month")
    for winner in winners:
        titleDate = winner.title[40:]
        winnerDate = datetime.strptime(titleDate, "%B %d, %Y")
        winnerFilename = winnerDate.strftime("%Y-%m-%d") + '.jpg'
        firstIndex = winner.selftext.find('1st')
        lastIndex = winner.selftext.find('votes')
        imgurLink = winner.selftext[firstIndex:lastIndex].split(" ")[4]
        download_as(imgurLink, os.path.join('/tmp', winnerFilename))
    
    logging.info('Generate new sidebar image')
    
    logging.info('Generate new banner image')
    
    logging.info('Update the subreddit')
    
if __name__ == '__main__':
    exec_update()