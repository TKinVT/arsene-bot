import os

from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from arsenal.slack import parser, get_info

load_dotenv()

app = Flask(__name__)

bolt_app = App(
    token=os.getenv('BOT_TOKEN'),
    signing_secret=os.getenv('SIGNING_SECRET')
)

handler = SlackRequestHandler(bolt_app)


@bolt_app.command('/ars')
def t(ack, respond, command):
    ack()
    if 'text' in command:
        respond(parser(command['text']))
    else:
        respond(get_info())


# Flask Routes
@app.route('/slack/events', methods=['POST'])
def slack_events():
    return handler.handle(request)


@app.route('/')
def test():
    return "Hi!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
