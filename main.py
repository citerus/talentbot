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

TALENTBOT_USER_ID = 'U0CJKS2DD'

class SlackEvent:
    TEXT_KEY = 'text'
    TYPE_KEY = 'type'
    CHANNEL_KEY = 'channel'
    MESSAGE_KEY = 'message'
    USER_KEY = 'user'
    REAL_NAME_KEY = 'real_name'
    PROFILE_KEY = 'profile'
    EMAIL_KEY = 'email'
    
    def __init__(self, event):
        self.event = event
        
    def isMessage(self):
        return (self.TYPE_KEY in self.event) and (self.MESSAGE_KEY in self.event[self.TYPE_KEY])
    
    def hasUser(self):
        return self.USER_KEY in self.event
        
    def isTalentBot(self):
        return self.event[self.USER_KEY] == TALENTBOT_USER_ID
        
    def channel(self):
        return self.event[self.CHANNEL_KEY]
        
    def text(self):
        return self.event[SlackEvent.TEXT_KEY]
        
    def isPersonTalentQuery(self):
        return (self.TEXT_KEY in self.event) and '@' in self.event[self.TEXT_KEY]

    def isTalentPersonQuery(self):
        return (self.TEXT_KEY in self.event) and 'talent' in self.event[self.TEXT_KEY]
        
    def userKey(self):
        userIdStr = self.event[self.TEXT_KEY].strip()
        userIdStr = userIdStr.replace(':','')
        userIdStr = userIdStr[2:-1] #slice user id from string minus @-sign 
        return userIdStr

def getTalentsByEmail(trello, emailAddr):
    board = [b for b in trello.list_boards() if 'Talanger' == b.name][0]
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

    if event.isPersonTalentQuery():
        print "calling for talents for a person"
        
        userDataJson = sc.api_call("users.info", user=event.userKey())
        userData = json.loads(userDataJson)
        
        if event.hasUser():
            name = userData[SlackEvent.USER_KEY][SlackEvent.REAL_NAME_KEY]
            email = userData[SlackEvent.USER_KEY][SlackEvent.PROFILE_KEY][SlackEvent.EMAIL_KEY]
            trelloData = getTalentsByEmail(trello, email)

            sc.rtm_send_message(event.channel(), 'Om ' + name + ': ' + trelloData)
        else:
            sc.rtm_send_message(event.channel(), 'Ingen person hittades med namnet ' + event.text().strip()[1:])
        
        print "called for talents for a person"
    
    if event.isTalentPersonQuery():
        # TODO Implement
        print "calling for persons for a talent"
        people = getPersonsByTalent(trello)
        sc.rtm_send_message(event.channel(), 'Personer med talangen: ' + people)
        print "called for persons for a talent"

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
