import time
import json
import logging
import pprint
import re

TALENTBOT_USER_ID = 'U0CJKS2DD'

class SlackEvent:

    prefixedTalentBotId = '<@{}>'.format(TALENTBOT_USER_ID)

    def __init__(self, jsonStr):
        self.jsonStr = jsonStr
        
    def __str__(self):
        #return str(self.jsonStr)
        return pprint.pformat(self.jsonStr, indent=1, width=60)

    def isMessage(self):
        return ('type' in self.jsonStr) and ('message' in self.jsonStr['type'])
    
    def hasUser(self):
        return 'user' in self.jsonStr
        
    def isTalentBot(self):
        return self.jsonStr['user'] == TALENTBOT_USER_ID

    def isForTalentBot(self):
        return self.jsonStr['text'].find(self.prefixedTalentBotId) == 0

    def hasAdditionalAddressee(self):
        return self.jsonStr['text'].rfind('<@') > 0

    def isDirectMsgForTalentBot(self):
        return self.jsonStr.get('channel','').find('D') == 0

    def channel(self):
        return self.jsonStr['channel']
        
    def text(self):
        return self.jsonStr['text']
        
    def textContains(self, inputStr):
        return ('text' in self.jsonStr) and inputStr in self.jsonStr['text']
        
    def textContainsKeyword(self, keyword):
        return ('text' in self.jsonStr) and re.compile('^' + keyword + '(\\s|$)', re.IGNORECASE).match(self.jsonStr['text'])

    def getKeywordArguments(self, keyword):
        return self.text().replace(keyword, '').strip()

    def userKey(self):
        jsonStrText = self.jsonStr['text']
        jsonStrText = jsonStrText.replace(self.prefixedTalentBotId,'')
        jsonStrText = jsonStrText.replace(':','').strip()[2:-1]
        return jsonStrText

class SlackUser:

    def __init__(self, userDataJson):
        self.userData = json.loads(userDataJson)
        self.verifyUserData(self.userData)

        self.name = self.userData['user']['real_name']
        self.email = self.userData['user']['profile']['email']
        self.links = [v['value'] for v in self.userData['user']['profile']['fields'].values() if len(v['value']) > 0]

    @staticmethod
    def verifyUserData(userData):
        if "ok" in userData and userData["ok"] == False:
            if "error" in userData:
                if userData["error"] == "user_not_found":
                    raise ValueError()
                else:
                    raise RuntimeError(userData["error"])
            else:
                raise RuntimeError("Unknown error from Slack server")

class TalentBot:

    def __init__(self, slackClient):
        self.slack = slackClient
        self.commands = []
    
    def addCommand(self, command):
        self.commands.append(command)
        
    def run(self):
        if not self.slack.rtm_connect():
            logging.critical("Error: Failed to connect to Slack servers")
            exit(-1)
        else:   
            logging.info("Talentbot is up and running")
            while True:
                try:
                    events = self.slack.rtm_read()
                    self.processEvents(events)
                except Exception, e:
                    logging.exception(e)
                            
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
        if not event.isMessage():
            logging.debug("Non-message event\n- %s" % event)
            return
    
        if event.isTalentBot():
            logging.debug("Event regarding myself\n- %s" % event)
            return
    
        if event.isMessage():
            logging.debug("Incoming message\n- %s" % event)

        for command in self.commands:
            if command.shouldTriggerOn(event):
                command.executeOn(event)
                break
