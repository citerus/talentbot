import os
from flask import Flask

# Set these variables in your local environment (export TRELLO_TOKEN=abcd)
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
    request_data = request.form
    text = request_data['text']
    return 'Did you say ' + text + '?'

if __name__ == "__main__":
    app.run(port=80)
    
