import os

from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from arsenal.slack import parser, get_info
from soccerinvt.utils import post_parser, new_post, search_photos, add_photo
from soccerinvt.views import post_modal, photo_search_modal, photo_search_results, modal_confirmation_view

load_dotenv()

app = Flask(__name__)

bolt_app = App(
    token=os.getenv('BOT_TOKEN'),
    signing_secret=os.getenv('SIGNING_SECRET')
)

handler = SlackRequestHandler(bolt_app)


##############################
# ARSENAL INFO SLACK FUNCTIONS
##############################
@bolt_app.command('/ars')
def arsenal_info(ack, respond, command):
    ack()

    if 'text' in command:
        text = command['text']
        respond(parser(text))
    else:
        respond(get_info())


############################
# SOCCERINVT SLACK FUNCTIONS
############################
@bolt_app.action('search_photos')
def search_photos(ack, body):
    ack()

    view_id = body['view']['id']
    post_id = body['view']['private_metadata']
    search_term = body['view']['state']['values']['search_term']['search_photos']['value']
    photos = search_photos(search_term)

    bolt_app.client.views_update(view_id=view_id, view=photo_search_results(post_id, photos))


@bolt_app.action('image_selection')
def select_photo(ack, action, body, client):
    ack()

    view_id = body['view']['id']
    post_id = body['view']['private_metadata']
    photo = action['value']

    add_photo(post_id, photo)
    client.views_update(view_id=view_id, view=modal_confirmation_view())


# ENTRY POINT
@bolt_app.command('/soccerinvt')
def blog(ack, command, respond):
    ack()

    if 'text' in command:
        text = command['text']
        parsed_text = post_parser(text)
        new_post(parsed_text['text'], tags=parsed_text['tags'])
        respond('Got it :thumbsup:')

    else:
        trigger_id = command['trigger_id']
        bolt_app.client.views_open(trigger_id=trigger_id, view=post_modal())


@bolt_app.view('new_modal_post')
def new_post_modal(ack, body, client):
    post_data = body['view']['state']['values']
    content = post_data['body']['text']['value']
    title = post_data['title']['text']['value']
    photo = post_data['photo_url']['text']['value']
    tags = post_data['tags']['text']['value']
    if tags:
        tags = [tag.strip() for tag in tags.split(',')]
    post = new_post(content, title=title, photo=photo, tags=tags)
    post_id = post.text

    if not photo:
        ack(response_action='update', view=photo_search_modal(post_id))
    else:
        ack(response_action='update', view=modal_confirmation_view())


##############
# Flask Routes
##############
@app.route('/slack/events', methods=['POST'])
def slack_events():
    return handler.handle(request)


@app.route('/')
def test():
    return "Hi!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
