""" Module to perform searches through Idealista API.
"""
import json

import requests

import pandas as pd
import numpy as np

from datetime import datetime

from .pagination import update_pagination
from .retrieve_data import retrieve_propertyCodes

from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

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
           '&numPage=' + str(Variable.get('pagination')) +
           '&language=' + language)

    kwargs['ti'].xcom_push(key='url', value=url)


def search_api(*args, **kwargs) -> json:
    '''
    Gets personal token and url created previously, and return our search results.
    '''
    
    oauth_token = kwargs['ti'].xcom_pull(task_ids='t1_get_oauth_token', key='oauth_token')
    
    pagination = Variable.get('pagination')

    url = kwargs['ti'].xcom_pull(task_ids='t2_set_url', key='url')

    headers = {'Content-Type': 'Content-Type: multipart/form-data;',
               'Authorization': 'Bearer ' + oauth_token}

    content = requests.post(url, headers=headers)

    if content.status_code == 200:
        result = json.loads(content.text) # Load result as json

        if len(result['elementList']) != 0:
            df = pd.DataFrame.from_dict(result['elementList']) # Load json as dataframe

            propertyCodes_inserted = retrieve_propertyCodes() # Retrieve propertyCodes from database
            df = df[~df['propertyCode'].isin(propertyCodes_inserted)] # Remove already inserted propertyCodes
            
            df = df[~df['propertyCode'].astype(int).isin(propertyCodes_inserted)]

            df.drop_duplicates(subset=['propertyCode'], inplace=True) # Remove duplicates

            # Change dict types to string and replace nan with np.nan --> This is done to avoid having 'nan' in the database
            dict_to_str = ['parkingSpace','detailedType','suggestedTexts','labels','highlight']
            for col in dict_to_str:
                if col in df.columns:
                    df[col] = df[col].astype(str).replace('nan', np.nan)

            df['pagination'] = pagination # Add pagination to dataframe

            df['upload_date'] = datetime.now() # Add upload date to dataframe
            
            # Insert data into database
            postgres_hook = PostgresHook(postgres_conn_id="postgres")
            df.to_sql(name='idealista_homes',
                    con=postgres_hook.get_sqlalchemy_engine(),
                    if_exists='append',
                    index=False,
                    chunksize=1000)
        
        # Update pagination
        update_pagination(result=result,
                          pagination=pagination,
                          task_instance=kwargs['ti'])
    
    elif content.status_code == 429:
        print("Maximum number of calls exceeded.")
        kwargs['ti'].xcom_push(key='task_status', value='Maximum number of calls exceeded.')
    
    else:
        print("Error: " + str(content.status_code))
        kwargs['ti'].xcom_push(key='task_status', value='Error: ' + str(content.status_code))