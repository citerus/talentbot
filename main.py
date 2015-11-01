import sys, os
from slackclient import SlackClient
from trello import TrelloClient
from talents import TrelloTalents
from talentbot import TalentBot
from command import Help, FindPeopleByTalent, FindTalentsByPerson, GetAllTalents
import logging
from envvars import verifyEnvironmentVariables

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ.get('TRELLO_API_KEY')
apiSecret   = os.environ.get('TRELLO_API_SECRET')
tr_token    = os.environ.get('TRELLO_TOKEN')
tokenSecret = os.environ.get('TRELLO_TOKEN_SECRET')
token       = os.environ.get('SLACK_TOKEN')

def main():
    verifyEnvironmentVariables(TRELLO_API_KEY=apiKey,
                               TRELLO_API_SECRET=apiSecret,
                               TRELLO_TOKEN=tr_token,
                               TRELLO_TOKEN_SECRET=tokenSecret,
                               SLACK_TOKEN=token)

    # TODO Set log level from command line, default to INFO
    logging.basicConfig(filename='talentbot.log', level=logging.INFO)

    slack = SlackClient(token)
    trello_client = TrelloClient(apiKey, apiSecret, tr_token, tokenSecret)
    trello = TrelloTalents(trello_client)
    talentBot = TalentBot(slack)
    talentBot.addCommand(Help(slack))
    talentBot.addCommand(FindPeopleByTalent(slack, trello))
    talentBot.addCommand(FindTalentsByPerson(slack, trello))
    talentBot.addCommand(GetAllTalents(slack, trello))
    talentBot.run()

if __name__ == "__main__":
    main()
