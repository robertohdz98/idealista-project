""" Module to retrieve data from the database.
"""

from airflow.providers.postgres.hooks.postgres import PostgresHook

def retrieve_propertyCodes(*args, **kwargs) -> list:
    """ Retrieves all the propertyCodes from the database.
    """


    # Select data from database
    postgres_hook = PostgresHook(postgres_conn_id="postgres")

    with open("dags/sql/get_all_propertyCodes.sql") as file: query = file.read()
    records = [record[0] for record in postgres_hook.get_records(query)]
    #df = pd.read_sql(sql='SELECT idealista_homes."propertyCode" FROM idealista_homes;',
                    #con=postgres_hook.get_conn())
    
    return records