"""
Author: Scr44gr
"""


def origin_url():
    """Get origin mbasic.facebook URL
    """
    return 'https://mbasic.facebook.com'


def login_url():
    """Get login mbasic.facebook URL
    """
    return origin_url()+'/login'


def profile_url():
    """Get profile mbasic.facebook URL
    """
    return origin_url()+'/profile'


def pages_url():
    """Get pages mbasic.facebook URL
    """
    return origin_url()+'/pages/?viewallpywo=1'
