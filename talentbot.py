import time
import sys
import json
import re
import pprint

class TalentCommand:
    def __init__(self):
        self.commands = []

    def addCommand(self, command):
        self.commands.append(command)

    def processEvent(self, event):
        return_string = ""
        for command in self.commands:
            if command.shouldTriggerOn(event):
                return_string = return_string + command.executeOn(event)
                break
        return return_string

class SlackEvent:

    def __init__(self, request):
        self.jsonStr = ""
        self.request = request
        
    def __str__(self):
        return str(self.jsonStr)
    
    def hasUser(self):
        return 'user' in self.jsonStr
        
    def channel(self):
        return self.jsonStr['channel']
        
    def text(self):
        return self.jsonStr['text']
        
    def textContains(self, inputStr):
        return ('text' in self.jsonStr) and inputStr in self.jsonStr['text']
        
    def textContainsKeyword(self, keyword):
        #txt = self.jsonStr['text']
        txt = self.request.args.get('text')
        return re.compile('^' + keyword + '(\\s|$)', re.IGNORECASE).match(txt)

    def getKeywordArguments(self, keyword):
        return self.text().replace(keyword, '').strip()

    def userKey(self):
        return self.jsonStr['text'].strip().replace(':', '')[2:-1]
