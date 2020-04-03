#!/usr/local/bin/python3
# coding: utf-8

'''
Created on Apr 1, 2020

@author: rcurtis
'''
import logging

logging.basicConfig(filename='DownloadWinners.log', level=logging.INFO, 
                    format='%(asctime)s :: %(levelname)s :: %(threadName)s :: %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

import os
import praw

from time import strftime, strptime
from utils.file_system_helper import get_files_in_desc_order
from utils.imgur_helper import download_as

def download_winners():
    target_dir = './winners'
    bot_name='BannerBot'
    user_agent='script:BannerBot:0.1 (by u/BourbonInExile)'
    reddit = praw.Reddit(bot_name, user_agent=user_agent)
    subreddit = reddit.subreddit("WetShaving")

    target_dir_files = get_files_in_desc_order(target_dir)
    
    winners = subreddit.search(query="weekly contest results", sort="new", time_filter="year")
    
    for winner in winners:
        titleDate = winner.title[40:]
        print("Downloading winner for ", titleDate)
        winnerDate = strptime(titleDate, "%B %d, %Y")
        winnerFilename = strftime("%Y-%m-%d", winnerDate) + '.jpg'
        if not winnerFilename in target_dir_files:
            logging.info('Downloading [%s]', winnerFilename)
            firstIndex = winner.selftext.find('1st')
            lastIndex = winner.selftext.find('votes')
            imgurLink = winner.selftext[firstIndex:lastIndex].split(" ")[4]
            download_as(imgurLink, os.path.join(target_dir, winnerFilename))
        else:
            logging.info('[%s] already exists, not downloading', winnerFilename)


if __name__ == '__main__':
    download_winners()