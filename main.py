import os
from flask import Flask
from slackclient import SlackClient
from talents import TrelloTalents
from talentbot import TalentBot
from command import Help, FindPeopleByTalent, FindTalentsByPerson

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, talentbot!"

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
