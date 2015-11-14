import sys, os, signal
from slackclient import SlackClient
from trello import TrelloClient
from talents import TrelloTalents
from talentbot import TalentBot
import logging.config
from envvars import verifyEnvironmentVariables

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
apiKey      = os.environ.get('TRELLO_API_KEY')
apiSecret   = os.environ.get('TRELLO_API_SECRET')
tr_token    = os.environ.get('TRELLO_TOKEN')
tokenSecret = os.environ.get('TRELLO_TOKEN_SECRET')
token       = os.environ.get('SLACK_TOKEN')

def log_and_exit(signal, frame):
    logging.info('Execution interrupted')
    sys.exit(0)

def getCommands(slack, trello):
    import inspect, new, command
    from command import Command

    commands = []
    for name, obj in inspect.getmembers(command):
        if inspect.isclass(obj) and issubclass(obj, Command) and obj != Command:
            commands.append(new.instance(obj, {'slack': slack, 'trello': trello}))
            logging.info('Found and instantiated command ' + name)
    return sorted(commands, lambda x, y: cmp(y.importance, x.importance))

def main():
    verifyEnvironmentVariables(TRELLO_API_KEY=apiKey,
                               TRELLO_API_SECRET=apiSecret,
                               TRELLO_TOKEN=tr_token,
                               TRELLO_TOKEN_SECRET=tokenSecret,
                               SLACK_TOKEN=token)

    logging.config.fileConfig('logging.conf')

    # Register interrupt handler
    signal.signal(signal.SIGINT, log_and_exit)
    signal.signal(signal.SIGTERM, log_and_exit)

    slack = SlackClient(token)
    trello_client = TrelloClient(apiKey, apiSecret, tr_token, tokenSecret)
    trello = TrelloTalents(trello_client)
    talentBot = TalentBot(slack)
    talentBot.addCommand(getCommands(slack, trello))
    talentBot.run()

if __name__ == "__main__":
    main()
