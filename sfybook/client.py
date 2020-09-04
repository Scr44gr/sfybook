"""
Author: Scr44gr

"""
from sfybook.auth import Auth
from sfybook.poster import Poster
from sfybook.comments import Comments
from sfybook import urls


class Client(Poster, Comments):

    def __init__(self, **kwargs):

        self.auth = Auth()
        if kwargs.get('session'):
            self.auth.session = kwargs.get('session')
        Poster.__init__(self, self.auth.session)
        Comments.__init__(self, self.auth.session)

class SfyNode(Client):
    """
        Client Node.
    """
    def __init__(self, session, **kwargs):
        super().__init__(session=session)
        self.url_id = kwargs.get('url_id')
        self.name = kwargs.get('name')