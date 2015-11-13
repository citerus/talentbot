import time
import logging
from slackevent import SlackEvent

class TalentBot:

    def __init__(self, slackClient):
        self.slack = slackClient
        self.commands = []
    
    def addCommand(self, command):
        if len(command) > 1:
            for cmd in command:
                self.commands.append(cmd)
        else:
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
