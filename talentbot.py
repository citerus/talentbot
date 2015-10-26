import time
import sys
import re

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
        self.text = request.args.get('text')
        self.request = request
        
    def textContains(self, inputStr):
        return inputStr in self.text
        
    def textContainsKeyword(self, keyword):
        return re.compile('^' + keyword + '(\\s|$)', re.IGNORECASE).match(self.text)

    def getKeywordArguments(self, keyword):
        return self.text.replace(keyword, '').strip()

