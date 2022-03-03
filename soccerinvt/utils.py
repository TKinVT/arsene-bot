import os
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

BLOG_URL = 'https://soccer.tkinvt.com'
PICAPI_URL = 'https://1midq92xie.execute-api.us-east-1.amazonaws.com/dev'
PICAPI_TOKEN = os.getenv('PICAPI_TOKEN')


def post_parser(text: str):
    # Deal with tags if they exist
    tags = None
    if "#" in text:
        split = text.split("#")
        text = split[0].strip()
        tags = [tag.strip() for tag in split[1:]]

    return {"text": text, "tags": tags}


def new_post(content: str, title: str = None, tags: List[str] = None, photo: str = None):
    json_payload = {'content': content, 'title': title, 'tags': tags, 'photo': photo}
    post = requests.post(f"{BLOG_URL}/new", json=json_payload)

    return post


def add_photo(post_id: str, photo_url: str):
    json_payload = {'photo': photo_url}
    update = requests.post(f"{BLOG_URL}/update/{post_id}", json=json_payload)

    return update


def search_photos(search_term):
    r = requests.post(PICAPI_URL, auth=('searcher', PICAPI_TOKEN), json={'q': search_term, 'count': 5})
    photos = r.json()

    return photos
