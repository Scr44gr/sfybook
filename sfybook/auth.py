"""
Author: Scr44gr

"""
from requests import Session
from requests.utils import cookiejar_from_dict, dict_from_cookiejar
from sfybook.poster import Poster
from sfybook import urls
from sfybook import helper
from os.path import exists, isdir
import json


class Auth:

    def __init__(self):
        self.session = Session()

    def login(self, email: str, password: str):
        """
            Sign in on facebook.com.

        :params:
            - email : str
            - password : str

        return: requests.Session
        """
        return self.__login(email=email, password=password)

    def load_session(self, filename: str) -> bytes:

        if exists(filename):
            with open(filename, '+r') as file:
                self.session.cookies = cookiejar_from_dict(json.load(file))
                response = self.session.get(urls.origin_url())
                status = self.status(response)
                return status

    @helper.login_required
    def save_session(self, filename: str):

        with open(filename, '+w') as file:
            cookies = dict_from_cookiejar(self.session.cookies)
            json.dump(cookies, file)


    def __login(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        # Get first session data.
        response = self.session.get(urls.login_url())

        if response.status_code == 200:
            content = response.content
            data = helper.get_request_data(content)

        # Sign in process.

        data['email'] = email
        data['pass'] = password
        data['login'] = 'Log In'  # or Submit
        response = self.session.post(urls.login_url(), data=data)
        return self.status(response)
    
    def status(self, response):
        
        if response.status_code == 200:
            if 'c_user' in self.session.cookies.get_dict():
                helper.set_session(self.session)
                return self.session

        raise Exception(
            'Login failed! Please check your email/password and try again!')

    @helper.login_required
    def logout(self):
        """
        Logout on facebook.com
        """
        pass
