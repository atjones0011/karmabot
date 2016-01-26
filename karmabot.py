import json
import re
import subprocess
import sys
import time

import redis
from slackclient import SlackClient


sc = SlackClient(sys.argv[1])
r = redis.StrictRedis(host='localhost', port=6379, db=0)


def poll_client():
    """
    Connects to Slack and listens for new messages on channels that karmabot has joined.
    If an incoming message is of type message and is from a channel, further processing will be
      performed.
    """
    if sc.rtm_connect():
        while True:
            messages = sc.rtm_read()

            try:
                for msg in messages:
                    if msg['type'] == 'message':
                        if (msg['channel'][0] == 'C'
                            or msg['channel'][0] == 'G'):
                            process_message(msg)
            except:
                sys.exc_info()[0]

            time.sleep(1)
    else:
        print 'Connection Failed, invalid token?'


def process_message(json_msg):
    """
    Parses messages posted to a channel and determines whether or not action needs to be taken.
    If the message is a karma message, other messages will be called to update the karma and send
      a message to the channel.

    ---------------------------------------------------------------------------
    THIS METHOD IS UNDER CONSTRUCTION.
    The logic has been put in place, but needs to be adjusted for readability.
    ---------------------------------------------------------------------------
    """
    regex = '^<?@.+>?:* *[\+-]{2,6}'
    splitter_regex = '<*:* *>*'
    text = json_msg['text']
    result = re.search(regex, text)

    if result is not None:
        parsed_text = result.group(0)
        user_and_amount = filter(None, re.split(splitter_regex, parsed_text))
        user_list = get_users()

        if user_list['members'] is not None:
            for user in user_list['members']:
                if ('@' + user['id'] == user_and_amount[0]
                    or '@' + user['name'] == user_and_amount[0]):
                    amount = len(user_and_amount[1]) - 1
                    if user_and_amount[1][0] == '-':
                        amount = -amount

                    new_amount = adjust_karma(user['id'], amount)
                    send_message(user['name'], new_amount, json_msg['channel'])
                    break


def adjust_karma(user_id, amount):
    """
    Increments or decrements a user's karma.
    To prevent spam, the maximum adjustment allowed in a single message is 5 points.
    """
    curr_amount = int(r.get(user_id) or 0)

    if amount >= 5:
        new_amount = curr_amount + 5
    elif amount <= -5:
        new_amount = curr_amount - 5
    else:
        new_amount = curr_amount + amount

    r.set(user_id, new_amount)
    return new_amount


def send_message(user_name, amount, channel):
    """
    Reports the amount of karma for a given user to a given channel.
    """
    msg = user_name + '\'s karma is now ' + str(amount)
    sc.rtm_send_message(channel, msg)


def get_users():
    """
    Fetches a list of user data for all of the users in the Slack team.
    """
    return json.loads(sc.api_call('users.list'))


if __name__ == '__main__':
    poll_client()