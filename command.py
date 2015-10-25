import json
from talentbot import Command, SlackUser

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

class GetAllTalents(Command):
    def __init__(self, slack, trello):
        self.slack = slack
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('all-talents')

    def executeOn(self, event):
        print "Executing GetAllTalents command"
        self.slack.rtm_send_message(event.channel(), "Talanger i systemet: " + self.trello.getAllTalents())
        print "Executed GetAllTalents command"
        return
