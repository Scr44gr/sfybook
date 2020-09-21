"""
Author: Scr44gr
"""
from requests_toolbelt import MultipartEncoder as MPEncoder
from requests import Session
from sfybook.utils import Utils, Image
from sfybook import helper
from sfybook import urls

EMPTY = None


class Poster(Utils):

    def __init__(self, session: Session):
        super().__init__(session)
        self.session = session
        helper.set_session(session)
        self.url_id = urls.origin_url()

    def post(self, text: str, **kwargs):
        """This function submit a facebook post.

            :params:
                - text : str
            :kwargs:
                - image : str
                - images : list
        """

        image = kwargs.get('image')
        images = kwargs.get('images')
        filter_type = kwargs.get('filter_type', '5')
        node = Image(EMPTY)

        if image or images:
            if image:
                node.add_child(Image(image, is_child=True))
            else:
                for image in images:
                    node.add_child(Image(image, is_child=True))
            return self.__post_image_to_facebook(text=text, images=node, filter_type=filter_type)
        kwargs['text'] = text
        return self.__post(**kwargs)

    def set_content_type(self, files): self.session.headers.update(
        {'Content-Type': files.content_type})

    def __post(self, **kwargs) -> bytes:

        data = kwargs.get('data')
        endpoint = kwargs.get('endpoint')

        if data is None:
            data, endpoint = helper.get_request_data(
                self.make_request(self.url_id), get_endpoint=True)
        if not isinstance(data, MPEncoder):

            image = kwargs.get('images')
            text = kwargs.get('text', '')
            if image:
                data['view_photo'] = 'Photo'
            else:
                data['view_post'] = 'Post'
            data['xc_message'] = text
        else:
            self.set_content_type(data)

        response = self.session.post(urls.origin_url()+endpoint, data=data)
        if response.status_code == 200:
            return response.content

    def submit_images_to_form(self, **kwargs):

        images = kwargs.get('images')
        data, endpoint = self.get_post_params(**kwargs)
        payload = {'fb_dtsg': data['fb_dtsg'], 'jazoest': data['jazoest']}
        files = self.get_files(payload=payload, data=data, images=images)

        for fields in files:
            self.set_content_type(fields)
            response = self.session.post(
                urls.origin_url()+endpoint, data=fields, headers=self.session.headers)

        text = kwargs.get('text', '')
        return self.post_image_to_facebook(response, text)

    def post_image_to_facebook(self, response, text):

        if response.status_code == 200:
            data, endpoint = helper.get_request_data(
                response.content, get_endpoint=True)
            data['xc_message'] = text
            data['view_post'] = 'Post'
            payload = MPEncoder(data, boundary=self.uuid)
            return self.__post(data=payload, endpoint=endpoint)

    def __post_image_to_facebook(self, **kwargs):

        return self.submit_images_to_form(**kwargs)

    def get_post_params(self, **kwargs):

        images = kwargs.get('images')
        text = kwargs.get('text')
        content = self.__post(images=images, text=text)
        data, endpoint = helper.get_request_data(content, get_endpoint=True)

        return (data, endpoint)
