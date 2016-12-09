#!usr/bin/env python3

"""
A Reddit bot that thanks other bots

Note: Since the bot is on a new account, it cannot
make a comment more than once every 10 minutes.
"""

import praw
import time

botlist = ['RemindMeBot', 'AutoModerator', 'samacharbot2']
replied_comments = {}
comment_string = """
Thank you {}!

----

"""


def post_reply(botname, submission):
    try:
        if replied_comments[submission.id]:
            return
    except KeyError:
        submission.reply(comment_string.format(botname))
        replied_comments[submission.id] = True
        print("Thanked {}. id: {}".format(botname, submission.id))
        print("waiting 10 minutes because reddit doesn't want spam :)")
        time.sleep(360)


def thank_the_bots():
    reddit = praw.Reddit('thankerbot')
    for botname in botlist:
        bot_object = reddit.redditor(botname)
        # bot_new_submissions includes posts and comments
        bot_new_submissions = bot_object.new(limit=1)
        for submission in bot_new_submissions:
            print("retrieving next comment")
            if isinstance(submission, praw.models.reddit.comment.Comment):
                post_reply(botname, submission)


if __name__ == '__main__':
    while True:
        thank_the_bots()
