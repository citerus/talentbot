import os
from flask import Flask, request

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
#slash_token = os.environ.get('SLASH_TOKEN')
apiKey      = os.environ.get('TRELLO_API_KEY')
apiSecret   = os.environ.get('TRELLO_API_SECRET')
tr_token    = os.environ.get('TRELLO_TOKEN')
tokenSecret = os.environ.get('TRELLO_TOKEN_SECRET')
#token       = os.environ.get('SLACK_TOKEN')

app = Flask(__name__)

@app.route('/')
def health():
    return "I'm fine"

@app.route('/', methods=['POST'])
def talent():

    slash_token = os.environ.get('SLASH_TOKEN').strip()
    request_data = request.form
    print 'Has: ', slash_token
    print 'Received: ', request_data['token']
    
    if request_data['token'].strip() == slash_token:
        text = request_data['text']
        return 'Did you say ' + text + '?'
    else:
        return 'Sorry, no'

if __name__ == "__main__":
    app.run(port=80)
    
