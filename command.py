import json
from slackuser import SlackUser
from wraplog import wraplog
import logging

class Command:
    def shouldTriggerOn(self, text):
        return False

    def executeOn(self, text):
        return ""

    def help(self):
        return ""

class FindTalentsByPerson(Command):
    importance = 4

    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def help(self):
        return "`@username` to find out what talents that person has."

    def shouldTriggerOn(self, text):
        return text.rfind('<@') > 0

    @wraplog("Fetching talents for a person")
    def executeOn(self, user_id):
        userDataJson = self.slack.api_call("users.info", user=user_id)

        try:
            user = SlackUser(userDataJson)

            logging.info(user.name + " : " + user.email)

            listOfTalents = self.trello.getTalentsByEmail(user.email)
            if listOfTalents != '':
                return 'Om ' + user.name + ': ' + listOfTalents
            else:
                return user.name + ' har inte lagt till talanger'
        except ValueError:
            self.getMissingUserErrorMsg(text)
        except RuntimeError as re:
            logging.error(re)

    @staticmethod
    def getMissingUserErrorMsg(user_id):
        return 'Ingen person hittades med id ' + user_id


class FindPersonsByTalent(Command):
    importance = 5

    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def help(self):
        return "`talent scrum` to find out who knows scrum."

    def shouldTriggerOn(self, text):
        return True #inputStr in text

    @wraplog("Calling for persons with talent")
    def executeOn(self, text):
        talent = text
        logging.info("Calling for persons that know " + talent)
        if len(talent) > 0:
            person_emails = self.trello.getPersonEmailsByTalent2(talent)
            people = self.persons_by_emails(person_emails)
            return "Personer med talangen " + talent + ": " + people
        else:
            return "Talang saknas i meddelandetexten"

    def persons_by_emails(self, email_addresses):
        all_users = json.loads(self.slack.api_call("users.list"))['members']
        active_users = [u for u in all_users if (not u['deleted'])]
        profiles = [u['profile'] for u in active_users if (u['profile'])]
        matched_profiles = [p['real_name'] for p in profiles if ('email' in p) and p['email'] in email_addresses]
        return '\n- ' + '\n- '.join(matched_profiles)

class GetAllTalents(Command):
    importance = 9

    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def help(self):
        return "`all-talents` to get all known talents."

    def shouldTriggerOn(self, text):
        return 'all-talents' in text

    @wraplog("Executing GetAllTalents command")
    def executeOn(self, text):
        return "Talanger i systemet: " + self.trello.getAllTalents()
