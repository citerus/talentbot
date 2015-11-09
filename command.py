import json
from talentbot import SlackUser
from wraplog import wraplog
import logging

class Command (object):
    def shouldTriggerOn(self, event):
        return False

    def executeOn(self, event):
        pass

class FindTalentsByPerson(Command):
    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.isDirectMsgForTalentBot() \
               or (event.isForTalentBot() and event.hasAdditionalAddressee())

    @wraplog("Fetching talents for a person")
    def executeOn(self, event):
        logging.debug("Raw data: " + str(event))

        userDataJson = self.slack.api_call("users.info", user=event.userKey())

        try:
            user = SlackUser(userDataJson)

            logging.info(user.name + " : " + user.email)

            listOfTalents = self.trello.getTalentsByEmail(user.email)
            if listOfTalents != '':
                self.slack.rtm_send_message(event.channel(), 'Om ' + user.name + ': ' + listOfTalents)
            else:
                self.slack.rtm_send_message(event.channel(), user.name + ' har inte lagt till talanger')
        except ValueError:
            self.slack.rtm_send_message(event.channel(), self.getMissingUserErrorMsg(event))
        except RuntimeError as re:
            logging.error(re)

    @staticmethod
    def getMissingUserErrorMsg(event):
        return 'Ingen person hittades med namnet ' + event.text().strip()[1:]


class FindPersonsByTalent(Command):
    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('talent')

    @wraplog("Calling for persons with talent")
    def executeOn(self, event):
        talent = event.getKeywordArguments('talent')
        logging.info("Calling for persons that know " + talent)
        if len(talent) > 0:
            person_emails = self.trello.getPersonEmailsByTalent2(talent)
            people = self.persons_by_emails(person_emails)
            self.slack.rtm_send_message(event.channel(), "Personer med talangen " + talent + ": " + people)
        else:
            self.slack.rtm_send_message(event.channel(), "Talangen " + talent + " ej funnen")

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

    @wraplog("Executing help command")
    def executeOn(self, event):
        self.slack.rtm_send_message(event.channel(), ":paperclip: It looks like you need help.")

class GetAllTalents(Command):
    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('all-talents')

    @wraplog("Executing GetAllTalents command")
    def executeOn(self, event):
        self.slack.rtm_send_message(event.channel(), "Talanger i systemet: " + self.trello.getAllTalents())
