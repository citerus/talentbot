import time
import sys
import os
import json
from slackclient import SlackClient
from trello import TrelloClient
import pprint

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

TRELLO_BOARD_NAME = 'Talanger'  # TODO might be a good idea to replace this with a Trello board ID
TALENTBOT_USER_ID = 'U0CJKS2DD'


class SlackEvent:

    def __init__(self, jsonStr):
        self.jsonStr = jsonStr
        
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
        
    def userKey(self):
        return self.jsonStr['text'].strip().replace(':', '')[2:-1]


class SlackUser:

    def __init__(self, userDataJson):
        self.userData = json.loads(userDataJson)
        self.name = self.userData['user']['real_name']
        self.email = self.userData['user']['profile']['email']

def getTalentsByEmail(trello, emailAddr):
    board = [b for b in trello.list_boards() if TRELLO_BOARD_NAME == b.name][0]
    users_talent_list = [l for l in board.get_lists('open') if l.name == emailAddr][0]
    users_talent_cards = [card.name for card in users_talent_list.list_cards()]
    return convertListToUtf8String(users_talent_cards)

def getPersonEmailsByTalent(trello, talentName):
    board = [b for b in trello.list_boards() if TRELLO_BOARD_NAME == b.name][0]
    matching_persons = [l.name for l in board.get_lists('open') if len([c for c in l.list_cards() if talentName.lower() == c.name.decode('utf-8').lower()]) > 0]
    matching_persons_names = [convertEmailAddressToFullName(p) for p in matching_persons]
    return convertListToUtf8String(matching_persons_names)

def convertListToUtf8String(list):
    return str(', '.join(list)).decode('utf-8')

def convertEmailAddressToFullName(emailAddr):
    return ' '.join(map(lambda x: x.capitalize(), emailAddr.replace('@citerus.se', '').replace('.', ' ').split(' ')))

def getTalentFromEvent(event):
    return event.text().replace('talent', '').strip()

def processMessage(msg, sc, trello):
    if msg is None or len(msg) == 0:
        return
    
    # @todo We must probably process all messages in the list, not just
    # the first one, as now. When reading, the SlackClient fetches everything
    # available on the WebSocket, which might mean several events in the list.    
    event = SlackEvent(msg[0])
    
    if not event.hasUser():
        print "Event without user\n-", msg
        return
    
    if event.isTalentBot():
        print "Event regarding myself\n-", msg
        return
    
    if event.isMessage():
        print "Incoming message\n-", msg

    if event.textContains('@'):
        print "Fetching talents for a person ..."
        
        userDataJson = sc.api_call("users.info", user=event.userKey())

        user = SlackUser(userDataJson)
        print "-", user.name, user.email
        
        if event.hasUser():
            trelloData = getTalentsByEmail(trello, user.email)
            sc.rtm_send_message(event.channel(), 'Om ' + user.name + ': ' + trelloData)
        else:
            sc.rtm_send_message(event.channel(), 'Ingen person hittades med namnet ' + event.text().strip()[1:])
        
        print "... done fetching talents."
    
    if event.textContains('talent'):
        print "calling for persons with a talent"
        talent = getTalentFromEvent(event)
        if len(talent) > 0:
            people = getPersonEmailsByTalent(trello, talent)
            sc.rtm_send_message(event.channel(), 'Personer med talangen ' + talent + ': ' + people)
        else:
            sc.rtm_send_message(event.channel(), 'Talangen ' + talent + ' ej funnen')
        print "called for persons with a talent"

def main():
    trello = TrelloClient(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
    slack = SlackClient(token)
    
    if not slack.rtm_connect():
        print "Error: Failed to connect to Slack servers"
        exit(-1)
    else:   
        print "Server is up and running"
    while True:
        try:
            msg = slack.rtm_read()
            processMessage(msg, slack, trello)
            #pprint.PrettyPrinter(indent=2).pprint(msg)
        except Exception as inst:
            print "Exception caught:", sys.exc_info()
            pprint.PrettyPrinter(indent=2).pprint(inst)
        
        # In general Slack allows one message per second,
        # although it may allow short bursts over the limit
        # for a limited time. https://api.slack.com/docs/rate-limits
        
        time.sleep(1)

if __name__ == "__main__":
    main()
