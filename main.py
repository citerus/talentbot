import time
import sys
import os
import json
import re
from slackclient import SlackClient
from trello import TrelloClient
import pprint

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

TRELLO_BOARD_ID = 'hud22dPi'
TALENTBOT_USER_ID = 'U0CJKS2DD'


class SlackEvent:

    def __init__(self, jsonStr):
        self.jsonStr = jsonStr
        
    def __str__(self):
        return str(self.jsonStr)

    def isMessage(self):
        return ('type' in self.jsonStr) and ('message' in self.jsonStr['type'])
    
    def hasUser(self):
        return 'user' in self.jsonStr
        
    def isTalentBot(self):
        return self.jsonStr['user'] == TALENTBOT_USER_ID
        
    def channel(self):
        return self.jsonStr['channel']
        
    def text(self):
        return self.jsonStr['text']
        
    def textContains(self, inputStr):
        return ('text' in self.jsonStr) and inputStr in self.jsonStr['text']
        
    def textContainsKeyword(self, keyword):
        return ('text' in self.jsonStr) and re.compile('^' + keyword + '\\s', re.IGNORECASE).match(self.jsonStr['text'])

    def userKey(self):
        return self.jsonStr['text'].strip().replace(':', '')[2:-1]


class SlackUser:

    def __init__(self, userDataJson):
        self.userData = json.loads(userDataJson)
        self.name = self.userData['user']['real_name']
        self.email = self.userData['user']['profile']['email']

class TrelloTalents:
    
    def __init__(self, api_key, api_secret, token, token_secret):
        self.client = TrelloClient(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)

    def talentBoard(self):
        return self.client.get_board(TRELLO_BOARD_ID)
    
    def getTalentsByEmail(self, emailAddr):
        users_talent_list = [l for l in self.talentBoard().get_lists('open') if l.name == emailAddr][0]
        users_talent_cards = [card.name for card in users_talent_list.list_cards()]
        return convertListToUtf8String(users_talent_cards)

    def getPersonEmailsByTalent(self, talentName):
        return [l.name for l in self.talentBoard().get_lists('open') if len([c for c in l.list_cards() if talentName.lower() == c.name.decode('utf-8').lower()]) > 0]

def persons_by_emails(slack, email_addresses):
    all_users = json.loads(slack.api_call("users.list"))['members']
    active_users = [u for u in all_users if (not u['deleted'])]
    profiles = [u['profile'] for u in active_users if (u['profile'])]
    matched_profiles = [p['real_name'] for p in profiles if ('email' in p) and p['email'] in email_addresses]
    return ", ".join(matched_profiles)

def convertListToUtf8String(list):
    return str(', '.join(list)).decode('utf-8')

def getTalentFromEvent(event):
    return event.text().replace('talent', '').strip()

def processEvent(event, slack, trello):
    if not event.hasUser():
        print "Event without user\n-", event
        return
    
    if event.isTalentBot():
        print "Event regarding myself\n-", event
        return
    
    if event.isMessage():
        print "Incoming message\n-", event

    if event.textContains('@'):
        print "Fetching talents for a person ..."
        
        userDataJson = slack.api_call("users.info", user=event.userKey())

        user = SlackUser(userDataJson)
        print "-", user.name, user.email
        
        if event.hasUser():
            trelloData = trello.getTalentsByEmail(user.email)
            slack.rtm_send_message(event.channel(), 'Om ' + user.name + ': ' + trelloData)
        else:
            slack.rtm_send_message(event.channel(), 'Ingen person hittades med namnet ' + event.text().strip()[1:])
        
        print "... done fetching talents."
    
    if event.textContainsKeyword('talent'):
        print "calling for persons with a talent"
        talent = getTalentFromEvent(event)
        if len(talent) > 0:
            person_emails = trello.getPersonEmailsByTalent(talent)
            people = persons_by_emails(slack, person_emails)
            slack.rtm_send_message(event.channel(), 'Personer med talangen ' + talent + ': ' + people)
        else:
            slack.rtm_send_message(event.channel(), 'Talangen ' + talent + ' ej funnen')
        print "called for persons with a talent"

def processEvents(events, slack, trello):
    if events is None:
        return
    for event in events:
        processEvent(SlackEvent(event), slack, trello)

def main():
    trello = TrelloTalents(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
    slack = SlackClient(token)
    
    if not slack.rtm_connect():
        print "Error: Failed to connect to Slack servers"
        exit(-1)
    else:   
        print "Talentbot is up and running"
    while True:
        try:
            events = slack.rtm_read()
            processEvents(events, slack, trello)
        except Exception as inst:
            print "Exception caught:", sys.exc_info()
            pprint.PrettyPrinter(indent=2).pprint(inst)
        
        # In general Slack allows one message per second,
        # although it may allow short bursts over the limit
        # for a limited time. https://api.slack.com/docs/rate-limits
        
        time.sleep(1)

if __name__ == "__main__":
    main()
