import os
from flask import Flask
from flask import request
from slackclient import SlackClient
from talents import TrelloTalents
from talentbot import TalentBot
from command import Help, FindPeopleByTalent, FindTalentsByPerson

# Set these variables in your local environment
# When deploying to Heroku, these variables can
# be set with the heroku-keys.sh script.
apiKey      = os.environ['TRELLO_API_KEY']
apiSecret   = os.environ['TRELLO_API_SECRET']
tr_token    = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']
token       = os.environ['SLACK_TOKEN']

app = Flask(__name__)

@app.route('/')
def hello():
    request_token = request.args.get('token')
    if (request_token != token):
        return "No!"
    else:
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
