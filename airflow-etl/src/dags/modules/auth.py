""" Module to request a Bearer token for OAuth authentication.
"""

import base64
import json

import requests

from airflow.models import Variable


def get_oauth_token(*args, **kwargs) -> str:
    '''
    Returns personalised token.
    Ref.: https://www.kaggle.com/code/laurabarreda/extract-data-from-idealista-api
    '''

    message = Variable.get('idealista_api_key') + ":" + Variable.get('idealista_api_secret')

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