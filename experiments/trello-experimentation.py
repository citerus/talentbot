import os
from trello import TrelloClient

#Use this file for trying out the trello api
#Usage: python -i trello-experimentation.py

apiKey = os.environ['TRELLO_API_KEY']
apiSecret = os.environ['TRELLO_API_SECRET']
tr_token = os.environ['TRELLO_TOKEN']
tokenSecret = os.environ['TRELLO_TOKEN_SECRET']

trello = TrelloClient(api_key=apiKey, api_secret=apiSecret, token=tr_token, token_secret=tokenSecret)
