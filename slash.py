import os, logging
from flask import Flask, request
from slackclient import SlackClient
from slackuser import SlackUser
from trello import TrelloClient
from talents import TrelloTalents

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('fileHandler')

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
slash_token = os.environ.get('SLASH_TOKEN').strip()
slack_token = os.environ.get('SLACK_TOKEN').strip()
apiKey      = os.environ.get('TRELLO_API_KEY').strip()
apiSecret   = os.environ.get('TRELLO_API_SECRET').strip()
tr_token    = os.environ.get('TRELLO_TOKEN').strip()
tokenSecret = os.environ.get('TRELLO_TOKEN_SECRET').strip()

app = Flask(__name__)

def getCommands(slack, trello):
    import inspect, new, command
    from command import Command

    commands = []
    for name, obj in inspect.getmembers(command):
        if inspect.isclass(obj) and issubclass(obj, Command) and obj != Command:
            commands.append(new.instance(obj, {'slack': slack, 'trello': trello}))
            logging.info('Found and instantiated command ' + name)
    return sorted(commands, lambda x, y: cmp(y.importance, x.importance))

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
        trello_client = TrelloClient(apiKey, apiSecret, tr_token, tokenSecret)
        trello = TrelloTalents(trello_client)
        logger.warn('Received text ' + text)
        for command in getCommands(slack,trello):
            if command.shouldTriggerOn(text):
                return command.executeOn(text)
        # user = SlackUser(slack.api_call("users.info", user=user_id))
        return 'Did you, ' + user.name + ', want to talk about ' + text + '?'
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
    
