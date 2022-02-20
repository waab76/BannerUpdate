'''
Created on Feb 27, 2021

@author: rcurtis
'''

import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

handlers = set()
handlers.add(TimedRotatingFileHandler('/home/pi/BannerBot.log',
                                      when='W0',
                                      backupCount=4))

logging.basicConfig(level=logging.INFO, handlers=handlers,
                    format='%(asctime)s %(levelname)s winner %(module)s:%(funcName)s %(message)s')
logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))

import os
from utils.reddit_helper import reddit, subreddit

def get_voting_id():
    # get the voting thread id
    f = open('voting_thread.txt', 'r')
    id = f.read()
    logging.info('Getting the Saturday voting post [%s]', id)    
    return id

def get_winners(voting_post):
    logging.info('Collecting votes from voting post [%s]', voting_post.id)
    entries = []
    for i in voting_post.comments:
        entrant = {'user': i.body.split(" - ")[0], 'submission': i.body.split(" - ")[1], 'score': i.score}
        entries.append(entrant)

    prelim_winners = sorted(entries, key=lambda k: k['score'], reverse=True)

    winners = check_for_tie(prelim_winners[:3])

    #re-sort winners
    final_winners = sorted(winners, key=lambda k: k['score'], reverse=True)

    return final_winners

def check_for_tie(winners):
    if len(winners) > 1 and winners[0]['score'] == winners[1]['score']:
        logging.info("there's a tie")
        lucky_winner = random.choice(winners[:2])
        lucky_winner_index = winners.index(lucky_winner)
        winners[lucky_winner_index]['score'] = (winners[lucky_winner_index]['score'] + 1)

    return winners

def delete_old_files():
    try:
        os.remove('submission_thread.txt')
        os.remove('voting_thread.txt')
    except:
        pass

def do_banner_winner():
    logging.info('Connected to Reddit instance as %s', reddit.user.me())
    voting_post = reddit.submission(id=get_voting_id())
    
    try:
        voting_post.mod.undistinguish()
        voting_post.mod.sticky(state=False)
    except:
        pass
    
    # ordered as 1st, 2nd, 3rd
    winners = get_winners(voting_post)
    
    content = ''
    date = datetime.datetime.today().strftime('%B %d, %Y')
    title = 'Weekly Sidebar Contest Results Thread - {}'.format(date)
    
    if len(winners) < 3:
        content = """Congrats to our winner:
        
1st - {} - {} [{} votes]

Thanks to everyone who entered and voted!""".format(winners[0]['user'], winners[0]['submission'], winners[0]['score'])
    else:
        content = """Congrats to our winners:
        
1st - {} - {} [{} votes]

2nd - {} - {} [{} votes]

3rd - {} - {} [{} votes]

Thanks to everyone who entered and voted!""".format(winners[0]['user'], winners[0]['submission'], winners[0]['score'],
                                                    winners[1]['user'], winners[1]['submission'], winners[1]['score'],
                                                    winners[2]['user'], winners[2]['submission'], winners[2]['score'])

    # create the post and mark it distinguished
    winner_post = subreddit.submit(
        title = title, 
        selftext = content,
        flair_id='fabd3b2e-0d64-11e8-8bed-0ef50fad3baa',
        send_replies=False)

    # mark the post as a mod post (for visibility)
    winner_post.mod.distinguish()
    winner_post.mod.sticky(state=True, bottom=True)


if __name__ == '__main__':
    do_banner_winner()
    delete_old_files()