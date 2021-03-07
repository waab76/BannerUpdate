# coding: utf-8
'''
Created on Feb 27, 2021

@author: rcurtis
'''

import logging
import re
from datetime import datetime
from utils.reddit_helper import reddit, subreddit

logging.basicConfig(filename='BannerBot.log', level=logging.INFO, 
                    format='%(asctime)s :: %(levelname)s :: voting :: %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

def get_submission_id():
    # get the submission thread id
    f = open('submission_thread.txt', 'r')
    id = f.read()
    logging.info('Getting the Friday submission post [%s]', id)    
    return id

def get_entries(submission_post):
    logging.info('Extracting users/images from submission post [%s]', submission_post.id)
    entries = dict()
    # regex solution found here: http://stackoverflow.com/a/28552670
    URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

    submission_post.comment_sort = 'new'
    submission_post.comments.replace_more(limit=0)
   
    for i in submission_post.comments.list():
        logging.info('Comment from %s: [%s]', i.author.name, i.body)
        url = re.findall(URL_REGEX, i.body)
        logging.info('URL found: [%s]', url)
        submitter = i.author.name
        if url:
            entries[submitter] = url[0]
    
    return entries

def do_voting_post():
    logging.info('Connected to Reddit instance as [%s]', reddit.user.me())
    submission_post = reddit.submission(id=get_submission_id())
    
    imgur_links = get_entries(submission_post)
    
    logging.info('Cleaning up Submission post')
    submission_post.mod.lock()
    submission_post.mod.undistinguish()

    logging.info('Building Voting post')
    formatted_date = datetime.today().strftime('%B %d, %Y')
    post_body = 'Voting will remain open for 24 hours. In the event of a tie for 1st place, a winner will be chosen at random. May the best voting_post win! Good luck to all!'
    
    logging.info('Submitting the Voting post')
    voting_post = subreddit.submit(
        title='Weekly Sidebar Contest Voting Thread - %s' % formatted_date,
        selftext=post_body,
        flair_id='fabd3b2e-0d64-11e8-8bed-0ef50fad3baa',
        send_replies=False,
        )
    
    voting_post.mod.distinguish()
    
    voting_post.mod.contest_mode(True)
    
    voting_post.mod.sticky(state=True, bottom=True)
    
    for contestant in imgur_links:
        voting_post.reply('%s - %s' % (contestant, imgur_links[contestant]))
        
    voting_post.mod.lock()
    
    logging.info('Post submitted with post id [%s]', voting_post.id)
    
    # save the submission id for use in the results thread
    f = open('voting_thread.txt', 'w')
    f.write(voting_post.id)
    
if __name__ == '__main__':
    do_voting_post()