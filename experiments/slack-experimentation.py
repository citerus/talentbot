from slackclient import SlackClient
import os

token = os.environ['SLACK_TOKEN']

slack = SlackClient(token)
