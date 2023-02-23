'''
Created on Feb 23, 2023

@author: rcurtis
'''
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

handlers = set()
handlers.add(TimedRotatingFileHandler('/home/ec2-user/BannerBot.log',
                                        when='W0',
                                        backupCount=4))

logging.basicConfig(level=logging.INFO, handlers=handlers,
                    format='%(asctime)s %(levelname)s winner %(module)s:%(funcName)s %(message)s')
logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))

from utils.reddit_helper import reddit, subreddit

if __name__ == '__main__':
    logging.info('Connected to Reddit instance as %s', reddit.user.me())
    post_generator = subreddit.search(query='flair:"Banner"', sort='new', time_filter='week')
    for post in post_generator:
        logging.debug('Found post "{}"'.format(post.title))
        if post.stickied:
            logging.info('Unpinning post "{}"'.format(post.title))
            post.mod.sticky(state=False)
