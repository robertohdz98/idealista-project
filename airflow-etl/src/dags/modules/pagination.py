""" Module to perform calculus of pagination number while searching through Idealista API.
"""

from airflow.models import Variable

def update_pagination(result:dict,
                      pagination:int,
                      task_instance:object,
                      *args, **kwargs) -> None:
    """
    Update the pagination number based on the search results and the current page number.

    Args:
        result (dict): A dictionary containing the results of a search through Idealista API.
        pagination (int): An integer representing the current page number.
        task_instance (object): An object representing the current task instance.
        *args: Optional positional arguments.
        **kwargs: Optional keyword arguments.

    Returns:
        None
    """
    
    # Check if the total number of pages in the search results is equal to the current page number
    if result['totalPages'] == pagination:
        # If they are equal, set the pagination variable to 1 and push a message to the task status
        Variable.set("pagination", 1)
        task_instance.xcom_push(key='task_status', value='Number of max pages reached. Please review the search parameters.')
    else:
        # Otherwise, increment the pagination variable by 1
        Variable.set("pagination", int(pagination) + 1)