"""
Construct headers for HTTP requests.
"""

def common_headers(token):
    """
    Common headers sent to OpenStack's API's.
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': token
    }
    return headers


def auth_headers():
    """
    Headers to set when authenticating against the API's.
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    return headers
