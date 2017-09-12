from functools import wraps
import requests


def w_additional_argument(f, key, value):
    """ Adding kwarg to function call.  """
    @wraps(f)
    def wrapper(*args, **kwargs):
        kwargs[key] = value
        return f(*args, **kwargs)
    return wrapper


def request_and_response(method, url, status_code, body=None, token=None):
    """ Send HTTP-request to the OpenEnergyPlatform API. Returns a
        `requests.Response` object.


    Parameters
    ----------

    method : str
        HTTP method.
    url : str
        Web address.
    body : dict
        Data send in JSON-format.
    token : str
        Authentication token.
    status_code : Integer
        Expected HTTP response code.

    Returns
    -------

        :class: `requests.Response`

    Raises
    ------

    AssertionError
        Expected HTTP code does not match actual response status code.
    """

    f = requests.request

    if token:

        f = w_additional_argument(f,
                                  'headers',
                                  {'Authorization': 'Token %s' % token})

    if body:
        f = w_additional_argument(f, 'json', body)

    res = f(method, url)

    assert res.status_code == status_code

    return res
