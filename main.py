import os
from slackclient import SlackClient
from trello import TrelloClient
from talents import TrelloTalents
from talentbot import TalentBot
from command import Help, FindPeopleByTalent, FindTalentsByPerson, GetAllTalents
import logging

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

def main():
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
