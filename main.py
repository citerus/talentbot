import time
import os
import json
from slackclient import SlackClient
from trello import TrelloClient

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

#TODO this func should filter messages not sent directly to slackbot
def isValidMsg(msg):
    return msg is not None and len(msg) > 0 \
        and (msgFormat.USER_KEY not in msg[0] \
        or msg[0][msgFormat.USER_KEY] != TALENTBOT_USER_ID)

def getPersonTalentQueryDataFromTrello(trello, emailAddr):
    board = [b for b in trello.list_boards() if 'Talanger' == b.name][0]
    talentList = [l for l in board.get_lists('open') if l.name == emailAddr][0]

    #replacing UTF-8 chars with XML-escapes to prevent error in SlackClient
    talentListStr = str(', '.join([c.name for c in talentList.list_cards()]))
    unicode_content = talentListStr.decode('utf-8')
    xml_content = unicode_content.encode('ascii', 'xmlcharrefreplace')

    return xml_content

def getTalentPersonQueryDataFromTrello(trello):
    return "Talanger" #TODO implement

def isPersonTalentQuery(msg):
    return msgFormat.TEXT_KEY in msg and '@' in msg[msgFormat.TEXT_KEY]

def isTalentPersonQuery(msg):
    return msgFormat.TEXT_KEY in msg and 'talent' in msg[msgFormat.TEXT_KEY]

def extractUserKey(msg):
    userIdStr = msg[msgFormat.TEXT_KEY].strip() #remove whitespace
    userIdStr = userIdStr.replace(':','') #remove colons if any
    userIdStr = userIdStr[2:-1] #slice user id from string minus @-sign 
    return userIdStr

def main():
    trello = TrelloClient(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
    sc = SlackClient(token)
    if not sc.rtm_connect():
        print "Error: Failed to connect to Slack servers"
    else:   
        print "Server is up and running"
    while True:
        try:
            msg = sc.rtm_read()
            if isValidMsg(msg) and msgFormat.TYPE_KEY in msg[0] and msgFormat.MESSAGE_KEY in msg[0][msgFormat.TYPE_KEY]:
                print msg
            #if isValidMsg(msg) and KEYTEXT in msg[0] and 'x' in msg[0][KEYTEXT]:
            #    channel = msg[0]['channel']
            #    sc.rtm_send_message(channel, 'Hej from Talentbot')
            if isValidMsg(msg) and isPersonTalentQuery(msg[0]):
                print "calling for talents for a person"
                channel = msg[0][msgFormat.CHANNEL_KEY]
                
                userKey = extractUserKey(msg[0])
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
            if isValidMsg(msg) and isTalentPersonQuery(msg[0]):
                #WORK IN PROGRESS
                print "calling for persons for a talent"
                channel = msg[0][msgFormat.CHANNEL_KEY]
                talentName = msg[0][msgFormat.TEXT_KEY]
                trelloData = getTalentPersonQueryDataFromTrello(trello)
                sc.rtm_send_message(channel, 'Personer med talangen ' + talentName)
                print "called for persons for a talent"
        except:
            print "Exception thrown"
        time.sleep(1)

if __name__ == "__main__":
    main()
