""" Module to perform searches through Idealista API.
"""
import json

import requests

import pandas as pd

from .pagination import update_pagination

from airflow.models import Variable

# TODO: parameters passing
# TODO: reduce number of requests (limited to 100)
def set_url(country:str,
            operation:str,
            property_type:str,
            center_coords:str="40.4167,-3.70325",
            distance_to_center:str="60000",
            max_price:int=750,
            max_items:int=50,
            sort:str="desc",
            language:str="es",
            order:str="priceDown",
            *args, **kwargs
            ) -> str:
    """ Combines params with the url,
    in order to create our own search url.

    Args:
    -------
    country: search country (es, it, pt)
    language: search language (es, it, pt, en, ca)
    max_items: max items per call, the maximum set by Idealista is 50
    operation: kind of operation (sale, rent)
    property_type: type of property (homes, offices, premises, garages, bedrooms)
    order: order of the listings, consult documentation for all the available orders
    center: coordinates of the search center
    distance_to_center: max distance from the center (in metres)
    sort = 'desc': how to sort the found items
    bankOffer: if the owner is a bank (boolean)
    max_price: max price of the listings (750)
    """

    # TODO: add params validation
    if country not in ["es", "it", "pt"]:
        raise ValueError("Invalid country.")

    if operation not in ["sale", "rent"]:
        raise ValueError("Invalid operation.")

    if property_type not in ["homes", "offices", "premises", "garages", "bedrooms"]:
        raise ValueError("Invalid property type.")

    url = (Variable.get('idealista_api_url') +
           country +
           '/search?operation=' + operation +
           '&maxItems=' + str(max_items) +
           '&order=' + order +
           '&center=' + center_coords +  # required
           '&distance=' + distance_to_center +  # required
           '&propertyType=' + property_type +
           '&sort=' + sort +
           '&numPage=%s' +
           '&language=' + language)

    kwargs['ti'].xcom_push(key='url', value=url)


def search_api(*args, **kwargs) -> json:
    '''
    Gets personal token and url created previously, and return our search results.
    '''
    
    oauth_token = kwargs['ti'].xcom_pull(task_ids='t1_get_oauth_token', key='oauth_token')
    
    pagination = Variable.get('pagination')

    url = kwargs['ti'].xcom_pull(task_ids='t2_set_url', key='url')
    url = url.format(pagination)# Increment pagination with an airflow variable

    headers = {'Content-Type': 'Content-Type: multipart/form-data;',
               'Authorization': 'Bearer ' + oauth_token}

    content = requests.post(url, headers=headers)

    if content.status_code == 200:
        result = json.loads(content.text)
        df = pd.DataFrame.from_dict(result['elementList'])
        print(df.head())
        # Upload df to drive (I think I have to save it first locally and then in another task upload it to drive)

        update_pagination(result=result,
                          pagination=pagination,
                          task_instance=kwargs['ti'])
    
    elif content.status_code == 429:
        print("Maximum number of calls exceeded.")
        kwargs['ti'].xcom_push(key='task_status', value='Maximum number of calls exceeded.')
    
    else:
        print("Error: " + str(content.status_code))
        kwargs['ti'].xcom_push(key='task_status', value='Error: ' + str(content.status_code))