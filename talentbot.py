import time
import sys
import json
import re
import pprint

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

    def getKeywordArguments(self, keyword):
        return self.text().replace(keyword, '').strip()

    def userKey(self):
        return self.jsonStr['text'].strip().replace(':', '')[2:-1]


class SlackUser:

    def __init__(self, userDataJson):
        self.userData = json.loads(userDataJson)
        self.name = self.userData['user']['real_name']
        self.email = self.userData['user']['profile']['email']

class Command (object):
    def shouldTriggerOn(self, event):
        return False

    def executeOn(self, event):
        return
        
class TalentBot:
    def __init__(self, slackClient):
        self.slack = slackClient
        self.commands = []
    
    def addCommand(self, command):
        self.commands.append(command)
        
    def run(self):
        if not self.slack.rtm_connect():
            print "Error: Failed to connect to Slack servers"
            exit(-1)
        else:   
            print "Talentbot is up and running"
            while True:
                try:
                    events = self.slack.rtm_read()
                    self.processEvents(events)
                except Exception as inst:
                    print "Exception caught:", sys.exc_info()
                    pprint.PrettyPrinter(indent=2).pprint(inst)
        
                    # In general Slack allows one message per second,
                    # although it may allow short bursts over the limit
                    # for a limited time. https://api.slack.com/docs/rate-limits
        
                    time.sleep(1)

    def processEvents(self, events):
        if events is None:
            return
        for event in events:
            self.processEvent(SlackEvent(event))

    def processEvent(self, event):
        if not event.hasUser():
            print "Event without user\n-", event
            return
    
        if event.isTalentBot():
            print "Event regarding myself\n-", event
            return
    
        if event.isMessage():
            print "Incoming message\n-", event

        for command in self.commands:
            if command.shouldTriggerOn(event):
                command.executeOn(event)
                break
            