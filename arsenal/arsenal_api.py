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


def results():
    r = requests.get(API_URL + '/results')
    return r.json()


def table():
    r = requests.get(API_URL + '/table')
    return r.json()


def meta_info():
    r = requests.get(API_URL + '/meta_info')
    return r.json()


if __name__ == '__main__':
    import pprint
    pprint.pprint(squad())
