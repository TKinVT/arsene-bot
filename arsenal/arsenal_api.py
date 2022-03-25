import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')


def fixtures():
    r = requests.get(API_URL + '/fixtures')
    return r.json()


def squad():
    r = requests.get(API_URL + '/players')
    return r.json()


def player(number):
    r = requests.get(API_URL + f'/players/{number}')
    return r.json()


def reddit_posts():
    r = requests.get(API_URL + '/reddit_posts')
    return r.json()


def results():
    r = requests.get(API_URL + '/results')
    return r.json()


def table():
    r = requests.get(API_URL + '/table')
    return r.json()


def tweets():
    r = requests.get(API_URL + '/tweets')
    return r.json()


def update(aspect):
    r = requests.post(API_URL + f'/update/{aspect}')
    return r.json()


def meta_info():
    r = requests.get(API_URL + '/meta_info')
    return r.json()
