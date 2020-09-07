
"""
Author: Scr44gr
"""
from requests_toolbelt import MultipartEncoder as MPEncoder
from requests import Session
from sfybook.utils import Utils
from sfybook import helper
from sfybook.client import SfyNode, Client
from sfybook import urls
from bs4 import BeautifulSoup


class Pages(Utils):

    def __init__(self, client: Client):
        super().__init__(client.auth.session)
        self.session = client.auth.session
        helper.set_session(self.session)

    @helper.login_required
    def my_pages(self):
        """
            Get all pages managed by the user.
        """
        return self.__my_pages()

    def __my_pages(self) -> SfyNode:

        response = self.make_request(urls.pages_url())
        document = BeautifulSoup(response, 'lxml')
        user_container = document.find('div', 'bw')
        pages = user_container.findAll('td', class_='n')

        for html in pages:
            try:
                page = html.find('a')
                name = page.find('img')['alt'].split(',')[0]
                url = urls.origin_url()+'/'+page['href'].split('/')[1]
                
                yield SfyNode(self.session, url_id=url, name=name)
            except AttributeError:
                continue
