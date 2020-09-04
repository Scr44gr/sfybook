"""
Author: Scr44gr
"""
from requests import Session
from sfybook.utils import Utils
from sfybook import helper
from sfybook import urls
from bs4 import BeautifulSoup
from re import search
from time import sleep


class Comments(Utils):
    """
        This class provides everything needed to work with comments, also includes custom methods.

    """

    def __init__(self, session: Session):
        super().__init__(session)
        self.session = session
        helper.set_session(session)

    @helper.login_required
    def comment(self, post_url: str, text: str, **kwargs) -> bytes:
        """This function the content of the response if the response status_code is 200.

        :params:
            - post_url : str -> The url of the post.
            - text : str -> The text to be posted in the comments.
        :kwargs:
            - images : list -> List of images to be posted in the comments.
        """
        self.comment_url = post_url

        return self.__comment(text=text)

    def __comment(self, **kwargs) -> bytes:

        text = kwargs.get('text', '')
        data, endpoint = helper.get_request_data(self.make_request(self.comment_url),
                                                 get_endpoint=True)

        data['comment_text'] = text

        response = self.session.post(urls.origin_url()+endpoint, data=data)

        if response.status_code == 200:
            return response.content

    @property
    def post_id(self):
        return search(r'story_fbid=(.*)&', self.comment_url).group(1).split('&')[0]

#    def get_top_user_from_post(self, post_url):
#        """This function returns a list of users with more comments in the post. \n
#        It may take a while, depending on the amount of comments. \n
#        :params:
#            - post_url : str ->The url of the post.
#        """
#        self.comment_url = post_url

#        return self.__get_top_user_from_post()


#    def __get_top_user_from_post(self):

#        run = True
#        document = BeautifulSoup(self.make_request(self.comment_url), 'lxml')
#        users = {}

#        while run:
#            sleep(0.2)
#            next_url = document.find('div', {'id': f'see_prev_{self.post_id}'})
#            if next_url is None:
#                break
#            comment_url = urls.origin_url() + next_url.find('a').get('href')
#            for user in document.findAll('h3'):
#                print("fetching {}..".format(user.text))
#                if user.text in users:
#                    users[user.text]['points'] += 1
#                else:
#                    users[user.text] = {'comments': 1,
#                                        'url': user.find('a').get('href')}
#            document = BeautifulSoup(self.make_request(comment_url), 'lxml')
#        return users
