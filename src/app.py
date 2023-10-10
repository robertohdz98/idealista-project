import logging
import os

import pandas as pd

from src.modules.auth import get_oauth_token
from src.modules.search import search_api, set_url


def main():

    token = get_oauth_token(api_key=CLIENT_API_KEY,
                            secret=CLIENT_SECRET)

    url = set_url("es", "es", operation="rent", property_type="homes")

    results_first = search_api(url, 1, token)
    total_pages = results_first['totalPages']
    print("Total pages found: ", total_pages)

    df_tot = pd.DataFrame.from_dict(results_first["elementList"])

    for page in range(2, total_pages):
        results = search_api(url, page, token)
        df = pd.DataFrame.from_dict(results['elementList'])

        # Increase 50 records (by default) each iteration
        df_tot = pd.concat([df_tot, df])

    print("Final length:", len(df_tot))

    df_to_file(df_tot)


if __name__ == "__main__":

    logging.info("Initialising scheduled pipelines...")

    # FIXME: Environment variables
    CLIENT_API_KEY = os.environ.get("CLIENT_API_KEY")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

    main()
