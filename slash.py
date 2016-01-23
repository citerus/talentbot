import os, logging
from flask import Flask, request
from slackclient import SlackClient
from slackuser import SlackUser

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
slash_token = os.environ.get('SLASH_TOKEN').strip()
slack_token = os.environ.get('SLACK_TOKEN').strip()
apiKey      = os.environ.get('TRELLO_API_KEY')
apiSecret   = os.environ.get('TRELLO_API_SECRET')
tr_token    = os.environ.get('TRELLO_TOKEN')
tokenSecret = os.environ.get('TRELLO_TOKEN_SECRET')

app = Flask(__name__)

@app.route('/')
def health():
    logger.info('Really, all is ok')
    return "I'm fine"

@app.route('/', methods=['POST'])
def talent():

    request_data = request.form
    if valid(request_data):
        user_id = request_data['user_id']
        text = request_data['text']
        slack = SlackClient(slack_token)
        user = SlackUser(slack.api_call("users.info", user=user_id))
        subject = SlackUser(slack.api_call("users.info", user=user_id))

        return 'Did you, ' + user.name + ', want to talk about ' + subject.name + '?'
    else:
        return 'Sorry, no'

def valid(request_data):
    request_token = request_data['token'].strip()
    if (request_token == slash_token):
        logger.debug('Token is ok')
        return True
    else:
        logger.warn('Invalid request received!')
        logger.debug('Has token: ' + slash_token)
        logger.debug('Received token: ' + request_token)
        return False


if __name__ == "__main__":
    app.run(port=80)
    
