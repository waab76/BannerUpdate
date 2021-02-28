'''
Created on Feb 27, 2021

@author: rcurtis
'''
import logging

logging.basicConfig(filename='BannerBot.log', level=logging.INFO, 
                    format='%(asctime)s :: %(levelname)s :: submission :: %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

from datetime import datetime
from utils.reddit_helper import reddit, subreddit

post_body = '''
Welcome to this week's sidebar submission contest!

The rules for the contest are as follows:

1) Users should submit only one (1) image of your choice to be voted on to be the sidebar for the week. 
Images must consist of anything related to wet shaving - razors, brushes, SOTD images, etc. In the event multiple images 
from a user are submitted, only the first image, or the image in the top level comment, will count.

1) Image must be Original Content (Not just some picture you found on the internet). Images taken by another photographer 
are allowed as long as: a. You have the photographer's permission. b. The image is connected to you in some meaningful 
way: e.g. It's a image of hardware you commissioned, taken by the maker, or the image is of something you made, taken by 
the purchaser, etc. c. We're not looking to have to verify images, so please use the honor system.

1) All properly submitted images will be entered into the Voting Thread. The Submission thread will be active for ~24 hours 
and will end Saturday. The vote thread will be active for 24 hrs from Saturday through Sunday. This thread is only a submission 
thread. Please do not hold discussion in the vote thread.

1) In the event of a tie, the bot will consult RNGesus to break the tie.

1) Submissions MUST be uploaded to imgur. Any other hosting site will be disqualified and not included in the voting thread.

1) Any submissions containing NSFW material may be removed at the discretion of the Mod Team.

1) While not required, it is suggested you submit square images in order to avoid unintended cropping.

**Please** feel free to respond with a comment to your entry with any background/description/detail about your entry, including gear used.

May the best submission win! Good luck to all!
'''

def do_submission_post():
    logging.info('Connected to Reddit instance as [%s]', reddit.user.me())
    logging.info('Submitting the Friday call for submissions')    
    formatted_date = datetime.today().strftime('%B %d, %Y')
    submission = subreddit.submit(
        title='Weekly Sidebar Contest Submission Thread - %s' % formatted_date,
        selftext=post_body,
        flair_id='fabd3b2e-0d64-11e8-8bed-0ef50fad3baa',
        send_replies=False,
        )
    
    submission.mod.distinguish()
    
    submission.mod.contest_mode()
    
    submission.mod.sticky(state=True, bottom=True)
    
    logging.info('Post submitted with post id [%s]', submission.id)
    
    # save the submission id for use in the voting thread
    f = open('submission_thread.txt', 'w')
    f.write(submission.id)

    
if __name__ == '__main__':
    do_submission_post()