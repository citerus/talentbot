import time
import os
import json
from slackclient import SlackClient
from trello import TrelloClient
import pprint

#Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

TRELLO_BOARD_NAME = 'Talanger'
TALENTBOT_USER_ID = 'U0CJKS2DD'

class SlackEvent:    
    def __init__(self, json):
        self.json = json
        
    def isMessage(self):
        return ('type' in self.json) and ('message' in self.json['type'])
    
    def hasUser(self):
        return 'user' in self.json
        
    def isTalentBot(self):
        return self.json['user'] == TALENTBOT_USER_ID
        
    def channel(self):
        return self.json['channel']
        
    def text(self):
        return self.json['text']
        
    def textContains(self, str):
        return ('text' in self.json) and str in self.json['text']
        
    def userKey(self):
        return self.json['text'].strip().replace(':','')[2:-1]
        
class SlackUser:
    def __init__(self, userDataJson):
        self.userData = json.loads(userDataJson)
        self.name = self.userData['user']['real_name']
        self.email = self.userData['user']['profile']['email']

def getTalentsByEmail(trello, emailAddr):
    board = [b for b in trello.list_boards() if TRELLO_BOARD_NAME == b.name][0]
    users_talent_list = [l for l in board.get_lists('open') if l.name == emailAddr][0]
    users_talent_cards = [card.name for card in users_talent_list.list_cards()]
    commatized_string = str(', '.join(users_talent_cards))
    utf_8_string = commatized_string.decode('utf-8')
    return utf_8_string

def getPersonsByTalent(trello):
    # TODO Implement
    return "Anna Anka, Bengt Baron, Carl Clocka"

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
        # TODO Implement
        print "calling for persons with a talent"
        talent = ''
        people = getPersonsByTalent(trello)
        sc.rtm_send_message(event.channel(), 'Personer med talangen ' + talent + ': ' + people)
        print "called for persons with a talent"

def main():
    trello = TrelloClient(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
    slack = SlackClient(token)
    
    if not slack.rtm_connect():
        print "Error: Failed to connect to Slack servers"
    else:   
        print "Server is up and running"
    while True:
        try:
            msg = slack.rtm_read()
            processMessage(msg, slack, trello)
            #pprint.PrettyPrinter(indent=2).pprint(msg)
        except Exception as inst:
            print "Exception caught:", inst
            pprint.PrettyPrinter(indent=2).pprint(inst)
        
        # In general Slack allows one message per second,
        # although it may allow short bursts over the limit
        # for a limited time. https://api.slack.com/docs/rate-limits
        
        time.sleep(1)

if __name__ == "__main__":
    main()
