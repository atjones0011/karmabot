import json
import re
import sys
import time

from slackclient import SlackClient


sc = None


def poll_client(token):
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
                        if msg['channel'][0] == 'C':
                            process_message(msg)
            except:
                pass

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
    regex = '^<@.+>:* *[\+-]{2}'
    splitter_regex = '<*:* *>*'
    text = json_msg['text']
    result = re.search(regex, text)

    if result is not None:
        parsed_text = result.group(0)
        user_and_amount = re.split(splitter_regex, parsed_text)
        user_list = get_users()

        if user_list['members'] is not None:
            for user in user_list['members']:
                if '@' + user['id'] == user_and_amount[1]:
                    amount = len(user_and_amount[2])
                    if user_and_amount[2][0] == '-':
                        amount = -amount

                    new_amount = adjust_karma(user['id'], amount)
                    send_message(user['name'], new_amount, json_msg['channel'])
                    break


def adjust_karma(user_id, amount):
    """
    Increments or decrements a user's karma.
    To prevent spam, the maximum adjustment allowed in a single message is 5 points.

    ---------------------------------------------------------------------
    THIS METHOD IS UNDER CONSTRUCTION.
    The datastore and logic for adjusting karma needs to be implemented.
    ---------------------------------------------------------------------
    """
    if amount >= 5:
        return 5
    elif amount <= -5
        return -5
    else
        return amount


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
    token = sys.argv[1]
    sc = SlackClient(token)

    poll_client(token)