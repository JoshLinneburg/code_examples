import requests
import json


def show_obj_head(obj, n_chars=500, n_items=5):
    """

    Parameters
    ----------
    obj : object
        any Python object; has to be a str, list, dict or requests.model.Response to return a value

    n_chars : int (optional)
        number of characters to return if the object is a str or requests.model.Response

    n_items : int (optional)
        number of items to return if the object is a list

    Returns
    -------
    result : obj
        a str, list or dict containing the "head" of the data supplied to the function

    """
    try:

        if isinstance(obj, requests.models.Response):
            print(f'The text of the response object returns a str with {len(obj.text)} characters!')
            print('')
            result = obj.text[:n_chars]  # Only returns the first 500 char's

        elif isinstance(obj, str):
            print(f'The object passed in is a str with {len(obj)} characters!')
            print('')
            result = obj[:n_chars]  # Only returns the first 500 char's

        elif isinstance(obj, list):
            print(f'The object passed in is a list with {len(obj)} items!')
            print('')
            result = obj[:n_items]  # Only returns the first 5 items

        elif isinstance(obj, dict):
            print(f'The object passed in is a dict with {len(obj.keys())} items!')
            print('')
            result = obj

        return result

    except:
        print('Something went wrong... try another URL or try again.')


def equivalence_checker(obj_one, obj_two, expected_value):
    """

    Parameters
    ----------
    obj_one
    obj_two
    expected_value

    Returns
    -------

    """
    actual_value = obj_one == obj_two

    if expected_value == actual_value:
        print('Josh knows a lot about Python - the actual matches expected!')
    else:
        print('Josh is wrong - the actual is different than the expected!')
