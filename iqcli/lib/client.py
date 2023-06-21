import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings

from iqcli.config import config

def _ignore_insecure_request(f):
    def wrapper_ignore_insecure_request(*args, **kwargs):
        warnings.simplefilter('ignore', InsecureRequestWarning)
        result = f(*args, **kwargs)
        warnings.simplefilter('default', InsecureRequestWarning)
        return result

    return wrapper_ignore_insecure_request


def _with_json_headers(f):
    def wrapper_with_json_headers(*args, **kwargs):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        
        kwargs.update(headers=headers)
        return f(*args, **kwargs)

    return wrapper_with_json_headers


def _build_url_base(path):
    scheme = 'http' + ('s' if config['server']['secure'] else '')
    return f'{scheme}://{config["server"]["host"]}{path}?apikey={config["apikey"]}'


@_with_json_headers
@_ignore_insecure_request
def get(path, *args, **kwargs):
    return requests.get(
        _build_url_base(path),
        verify=config['server']['verify'],
        *args,
        **kwargs,
    )


@_with_json_headers
@_ignore_insecure_request
def post(path, *args, **kwargs):
    return requests.post(
        _build_url_base(path),
        verify=config['server']['verify'],
        *args,
        **kwargs,
    )
