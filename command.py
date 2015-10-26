import json

class Command (object):
    def shouldTriggerOn(self, event):
        return False

    def executeOn(self, event):
        return

class Help(Command):
    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('help')

    def executeOn(self, event):
        return ":paperclip: Clippy is ded."

class FindTalentsByPerson(Command):
    def __init__(self, trello):
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContains('@')

    def executeOn(self, event):
        # TODO Problem - now we have to map slack handles to emails
        # Because asking using a Slack handle is most convenient.
        user_email = "tobias.fors@citerus.se"

        # TODO If we found the requested user
        if True: 
            trelloData = self.trello.getTalentsByEmail(user_email)
            return 'Om ' + user_email + ': ' + trelloData
        else:
            return 'Ingen person hittades med namnet ' + user_email

class FindPeopleByTalent(Command):
    def __init__(self, trello):
        self.trello = trello

    def shouldTriggerOn(self, event):
        return event.textContainsKeyword('talent')

    def executeOn(self, event):
        talent_word = event.getKeywordArguments('talent')

        if talent_word.strip() == "":
            return ""
        
        person_emails = self.trello.getPersonEmailsByTalent(talent_word)
        
        if len(person_emails) > 0:
            return "Personer som kan " + talent_word + ": " + '\n- ' + '\n- '.join(person_emails)
        else:
            return "Ingen har lagt upp att de kan " + talent_word + "."
