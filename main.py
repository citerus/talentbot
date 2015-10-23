import time
import sys
import os
import json
import re
from slackclient import SlackClient
from talents import TrelloTalents
import pprint

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

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
            
class FindTalentsByPerson(Command):
    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContains('@')

    def executeOn(self, event):
        print "Fetching talents for a person ..."
        
        userDataJson = self.slack.api_call("users.info", user=event.userKey())

        user = SlackUser(userDataJson)
        print "-", user.name, user.email
 
        if event.hasUser():
            trelloData = self.trello.getTalentsByEmail(user.email)
            self.slack.rtm_send_message(event.channel(), 'Om ' + user.name + ': ' + trelloData)
        else:
            self.slack.rtm_send_message(event.channel(), 'Ingen person hittades med namnet ' + event.text().strip()[1:])
 
        print "... done fetching talents."

class FindPeopleByTalent(Command):
    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('talent')

    def executeOn(self, event):
        print "received request for talent"
        talent = event.getKeywordArguments('talent')
        print "calling for persons with talent " + talent 
        if len(talent) > 0:
            person_emails = self.trello.getPersonEmailsByTalent(talent)
            people = self.persons_by_emails(person_emails)
            self.slack.rtm_send_message(event.channel(), "Personer med talangen " + talent + ": " + people)
        else:
            self.slack.rtm_send_message(event.channel(), "Talangen " + talent + " ej funnen")
            print "called for persons with a talent"

    def persons_by_emails(self, email_addresses):
        all_users = json.loads(self.slack.api_call("users.list"))['members']
        active_users = [u for u in all_users if (not u['deleted'])]
        profiles = [u['profile'] for u in active_users if (u['profile'])]
        matched_profiles = [p['real_name'] for p in profiles if ('email' in p) and p['email'] in email_addresses]
        return '\n- ' + '\n- '.join(matched_profiles)
        
class Help(Command):
    def __init__(self, slack):
        self.slack = slack

    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('help')

    def executeOn(self, event):
        self.slack.rtm_send_message(event.channel(), ":paperclip: It looks like you need help.")
        print "Executed help command"
        return
        
def main():
    slack = SlackClient(token)
    trello = TrelloTalents(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
    talentBot = TalentBot(slack)
    talentBot.addCommand(Help(slack))
    talentBot.addCommand(FindPeopleByTalent(slack, trello))
    talentBot.addCommand(FindTalentsByPerson(slack, trello))
    talentBot.run()

if __name__ == "__main__":
    main()
