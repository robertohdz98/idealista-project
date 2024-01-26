""" Module to request a Bearer token for OAuth authentication.
"""

import base64
import json

import requests

from airflow.models import Variable


def choose_api_auth(*args, **kwargs) -> str:
    '''
    Distribute burden between available tokens.
    '''

    choose_api_auth = int(Variable.get('choose_api_auth'))

    api_key = Variable.get('idealista_api_key').split(',')
    api_secret = Variable.get('idealista_api_secret').split(',')

    if choose_api_auth == len(api_key)-1:
        Variable.set("choose_api_auth", 0)
    else: 
        Variable.set("choose_api_auth", choose_api_auth+1)

    return api_key[choose_api_auth], api_secret[choose_api_auth]

def get_oauth_token(*args, **kwargs) -> str:
    '''
    Returns personalised token.
    Ref.: https://www.kaggle.com/code/laurabarreda/extract-data-from-idealista-api
    '''

    api_key, api_secret = choose_api_auth(*args, **kwargs)
    message = api_key + ":" + api_secret

    auth = "Basic " + base64.b64encode(message.encode("ascii")).decode("ascii")

    headers_dic = {"Authorization": auth,
                   "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

    params_dic = {"grant_type": "client_credentials",   # Define the request params
                  "scope": "read"}

    response = requests.post("https://api.idealista.com/oauth/token",
                             headers=headers_dic,
                             params=params_dic)

    token = json.loads(response.text)['access_token']

    kwargs['ti'].xcom_push(key='oauth_token', value=token)