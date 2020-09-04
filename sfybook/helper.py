"""
Author: Scr44gr
"""
from bs4 import BeautifulSoup
from functools import wraps
from sfybook import urls
from bs4 import BeautifulSoup

default_exclude_keys = ['search', 'refid', 'search_source']
default_get_endpoint = False
__session = None


def get_request_data(content: bytes, **kwargs) -> tuple:
    
    remove_keys = lambda items, ex_key: [items.pop(key, '') for key in ex_key]
    get_endpoint = kwargs.get('get_endpoint', default_get_endpoint)
    exclude_key = kwargs.get('exclude_key', default_exclude_keys)

    data = {}
    i = 0
    document = BeautifulSoup(content, 'lxml')
    for item in document.findAll('input', {'type': 'hidden'}):
        key = item.get('name')
        value = item.get('value', '')

        if key.endswith('[]'):
            data[key.replace('[]', f'[{i+1}]')] = value
            i += 1
        else:
            data[key] = value

    remove_keys(data, exclude_key)

    if get_endpoint:
        endpoint = document.findAll('form', {'method': 'post'})[
            0].get('action')
        return (data, endpoint)
    return data

def set_session(session):
    global __session
    __session = session

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global __session
        if not 'c_user' in __session.cookies.get_dict():
            raise Exception('Please, login before call this method.')
        return f(*args, **kwargs)
    return wrapper