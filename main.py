import time
import os
import json
from slackclient import SlackClient
from trello import TrelloClient
import pprint

class SlackMsgFormat():
    def __init__(self):
        self.TEXT_KEY = 'text'
        self.TYPE_KEY = 'type'
        self.CHANNEL_KEY = 'channel'
        self.MESSAGE_KEY = 'message'
        self.USER_KEY = 'user'
        self.REAL_NAME_KEY = 'real_name'
        self.PROFILE_KEY = 'profile'
        self.EMAIL_KEY = 'email'

    def __getattr__(self, name):
        return name if name in self else None
msgFormat = SlackMsgFormat()

#Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey = os.environ['TRELLO_API_KEY']
apiSecret = os.environ['TRELLO_API_SECRET']
tr_token = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token = os.environ['SLACK_TOKEN']

TALENTBOT_USER_ID = 'U0CJKS2DD'

class SlackEvent:
    def __init__(self, event):
        self.event = event
        
    def isMessage(self):
        return (msgFormat.TYPE_KEY in self.event) and (msgFormat.MESSAGE_KEY in self.event[msgFormat.TYPE_KEY])
        
    def lacksUser(self):
        return msgFormat.USER_KEY not in self.event 
        
    def isTalentBot(self):
        return self.event[msgFormat.USER_KEY] == TALENTBOT_USER_ID
        
    def channel(self):
        return self.event[msgFormat.CHANNEL_KEY]
        
    def isPersonTalentQuery(self):
        return (msgFormat.TEXT_KEY in self.event) and '@' in self.event[msgFormat.TEXT_KEY]

    def isTalentPersonQuery(self):
        return (msgFormat.TEXT_KEY in self.event) and 'talent' in self.event[msgFormat.TEXT_KEY]
        
    def userKey(self):
        userIdStr = self.event[msgFormat.TEXT_KEY].strip() #remove whitespace
        userIdStr = userIdStr.replace(':','') #remove colons if any
        userIdStr = userIdStr[2:-1] #slice user id from string minus @-sign 
        return userIdStr

def getPersonTalentQueryDataFromTrello(trello, emailAddr):
    board = [b for b in trello.list_boards() if 'Talanger' == b.name][0]
    users_talent_list = [l for l in board.get_lists('open') if l.name == emailAddr][0]
    users_talent_cards = [card.name for card in users_talent_list.list_cards()]
    commatized_string = str(', '.join(users_talent_cards))
    utf_8_string = commatized_string.decode('utf-8')
    return utf_8_string

def getTalentPersonQueryDataFromTrello(trello):
    return "Talanger" #TODO implement

def processMessage(msg, sc, trello):
    if msg is None or len(msg) == 0:
        return
    
    # @todo We must probably process all messages in the list, not just
    # the first one, as now. When reading, the SlackClient fetches everything
    # available on the WebSocket, which might mean several events in the list.    
    event = SlackEvent(msg[0])
    
    if event.lacksUser():
        print "Event without user\n-", msg
        return
    
    if event.isTalentBot():
        print "Event regarding myself\n-", msg
        return
    
    if event.isMessage():
        print "Incoming message\n-", msg

    if event.isPersonTalentQuery():
        print "calling for talents for a person"
        channel = event.channel()
        
        userKey = event.userKey()
        userDataJson = sc.api_call("users.info", user=userKey)
        userData = json.loads(userDataJson)
        if msgFormat.USER_KEY in userData:
            name = userData[msgFormat.USER_KEY][msgFormat.REAL_NAME_KEY]
            email = userData[msgFormat.USER_KEY][msgFormat.PROFILE_KEY][msgFormat.EMAIL_KEY]
            trelloData = getPersonTalentQueryDataFromTrello(trello, email)

            sc.rtm_send_message(channel, 'Om ' + name + ': ' + trelloData)
        else:
            sc.rtm_send_message(channel, 'Ingen person hittades med namnet ' + msg[0][msgFormat.TEXT_KEY].strip()[1:])
        print "called for talents for a person"
    
    if event.isTalentPersonQuery():
        #WORK IN PROGRESS
        print "calling for persons for a talent"
        channel = msg[0][msgFormat.CHANNEL_KEY]
        talentName = msg[0][msgFormat.TEXT_KEY]
        trelloData = getTalentPersonQueryDataFromTrello(trello)
        sc.rtm_send_message(channel, 'Personer med talangen ' + talentName)
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
