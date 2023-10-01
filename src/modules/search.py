""" Module to perform searches through Idealista API.
"""
import json

import requests

BASE_IDEALISTA_API_URL = 'https://api.idealista.com/3.5/'


# TODO: parameters passing
# TODO: reduce number of requests (limited to 100)
def set_url(country, operation, property_type,
            center_coords="40.4167,-3.70325",
            distance_to_center="60000",
            max_price=750,
            max_items=50,
            sort="desc",
            language="es",
            order="priceDown"
            ):
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

    url = (BASE_IDEALISTA_API_URL +
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

    return url


def search_api(url: str, pagination: int, token: str):
    '''
    Gets personal token and url created previously, and return our search results.
    '''

    url = url.format(pagination)

    headers = {'Content-Type': 'Content-Type: multipart/form-data;',
               'Authorization': 'Bearer ' + token}

    content = requests.post(url, headers=headers)

    if content.status_code == 429:
        raise Exception("Maximum number of calls exceeded.")

    result = json.loads(content.text)

    return result
