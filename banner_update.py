#!/usr/local/bin/python3
# coding: utf-8

'''
Created on Mar 29, 2020

@author: rcurtis
'''
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

handlers = set()
handlers.add(TimedRotatingFileHandler('/var/log/BannerBot.log',
                                      when='W0',
                                      backupCount=4))

logging.basicConfig(level=logging.INFO, handlers=handlers,
                    format='%(asctime)s %(levelname)s update %(module)s:%(funcName)s %(message)s')
logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))

from utils.file_system_helper import remove_file, get_files_in_desc_order
from utils.imagery_helper import generate_thumbnail_file, generate_banner_image
from utils.reddit_helper import reddit
from utils.subreddit_helper import download_contest_winners, update_subreddit

banner_image_name = "banner.jpg"
sidebar_image_name = "sidebar-img.jpg"
working_dir = './winners'

def exec_update():
    logging.info('Connected to Reddit instance as %s', reddit.user.me())
    
    logging.info('Clean up old banner and sidebar files if they exist')
    remove_file(working_dir, banner_image_name)
    remove_file(working_dir, sidebar_image_name)
    
    logging.info('Fetch winning images')
    download_contest_winners(working_dir)
    
    logging.info('Generate new sidebar image')
    thumbnail_max_dimensions = 512,512
    sidebar_input_file = get_files_in_desc_order(working_dir)[0]
    generate_thumbnail_file(working_dir, sidebar_input_file, sidebar_image_name, 
                            thumbnail_max_dimensions)

    logging.info('Generate new banner image')
    banner_size = 1920, 256
    generate_banner_image(working_dir, banner_image_name, banner_size)
    
    logging.info('Update the subreddit')
    update_subreddit(working_dir, sidebar_image_name, banner_image_name)
    logging.info('Done')

    
if __name__ == '__main__':
    exec_update()