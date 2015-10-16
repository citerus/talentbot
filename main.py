import time
from slackclient import SlackClient
import os
from trello import TrelloClient
import json

keyType = 'type'
keyText = 'text'
keyMessage = 'message'

apiKey = 'a' #os.environ['TRELLO_API_KEY']
apiSecret = 'b' #os.environ['TRELLO_API_SECRET']
tr_token = 'c' #os.environ['TRELLO_TOKEN']
tokenSecret = 'd' #os.environ['TRELLO_TOKEN_SECRET']

def isValidMsg(msg):
    return msg is not None and msg != []

def getTrelloData():
    trello = TrelloClient(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
    board = [b for b in trello.list_boards() if 'Talanger' in b.name][0]
    return board.get_cards()

token = "slack token here"
sc = SlackClient(token)
if sc.rtm_connect():
    print "Up and running"
    while True:
        msg = sc.rtm_read()
        if isValidMsg(msg) and keyType in msg[0] and keyMessage in msg[0][keyType]:
            print msg
        #if isValidMsg(msg) and keyText in msg[0] and 'x' in msg[0][keyText] :
        #    channel = msg[0]['channel']
        #    sc.rtm_send_message(channel, 'Hej from Talentbot') 
        if isValidMsg(msg) and keyText in msg[0] and '@' in msg[0]['text']:
            userKey = msg[0]['text'][2:-1]
            print "userkey",userKey
            print "calling for user.info"
            channel = msg[0]['channel']
            userdata = sc.api_call("users.info", user=userKey)
            name = json.loads(userdata)['user']['real_name']
            reply = getTrelloData()
            print reply 
            print type(reply)
            sc.rtm_send_message(channel, 'Om ' + name + ' ' + str([r.name for r in reply]))
            print "called for user.info"
        time.sleep(1)
else:
    print "ERROR"
