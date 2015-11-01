import sys, os
from slackclient import SlackClient
from trello import TrelloClient
from talents import TrelloTalents
from talentbot import TalentBot
from command import Help, FindPeopleByTalent, FindTalentsByPerson, GetAllTalents
import logging

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ.get('TRELLO_API_KEY')
apiSecret   = os.environ.get('TRELLO_API_SECRET')
tr_token    = os.environ.get('TRELLO_TOKEN')
tokenSecret = os.environ.get('TRELLO_TOKEN_SECRET')
token       = os.environ.get('SLACK_TOKEN')

def verifyEnvironmentVariables(apiKey, apiSecret, tr_token, tokenSecret, token):
    if apiKey is None or len(apiKey) == 0:
        return "Environment property TRELLO_API_KEY not set, aborting."
    if apiSecret is None or len(apiSecret) == 0:
        return "Environment property TRELLO_API_SECRET not set, aborting."
    if tr_token is None or len(tr_token) == 0:
        return "Environment property TRELLO_TOKEN not set, aborting."
    if tokenSecret is None or len(tokenSecret) == 0:
        return "Environment property TRELLO_TOKEN_SECRET not set, aborting."
    if token is None or len(token) == 0:
        return "Environment property SLACK_TOKEN not set, aborting."
    return None

def main():
    err = verifyEnvironmentVariables(apiKey, apiSecret, tr_token, tokenSecret, token)
    if err is not None:
        sys.exit(err)

    # TODO Set log level from command line, default to INFO
    logging.basicConfig(filename='talentbot.log',level=logging.INFO)
    
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
