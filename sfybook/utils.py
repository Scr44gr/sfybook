"""
Author: Scr44gr
"""
from requests_toolbelt import MultipartEncoder as MPEncoder
from random import getrandbits
from requests import Session
from uuid import UUID
from os.path import exists
from time import sleep


class Utils:

    def __init__(self, session: Session):
        self.session = session

    @property
    def uuid(self) -> str:
        return '-'*28+str(UUID(int=getrandbits(95)).int)

    def make_request(self, url: str) -> bytes:
        return self.session.get(url).content

    def get_files(self, **kwargs) -> list:

        payload = kwargs.get('payload')
        self.data = kwargs.get('data')
        self.images = kwargs.get('images')
        self.limit = 3
        self.size = lambda: len(self.images.nodes)

        items = []
        if payload and self.images:

            while not (fields := self.__files(payload=payload)) is None:
                files = MPEncoder(fields, boundary=self.uuid)
                items.append(files)

        return items

    def __files(self, payload: dict):

        template = {}
        template.update(payload)
        out_size = len(list(template.keys()))

        total = self.size()
        for i in range(total):
            if (i < self.limit):
                image = self.images.nodes.pop(0)
                template[f'file{i+1}'] = image.payload
                continue
            return self.update_payload(template, **self.data)
        size = len(list(template.keys()))

        return self.__fill_empty_spaces(size, out_size, payload=template)

    def __fill_empty_spaces(self, size: int, out_size: int, payload: dict):

        size = size-out_size
        if size < self.limit and not size == 0:

            payloads = self.images.empty_payload(size=size)
            for i in range(len(payloads)):
                size = (i - self.limit)*-1
                payload[f'file{size}'] = payloads[i]
            return self.update_payload(payload, **self.data)

    @staticmethod
    def update_payload(data, **kwargs):
        payload = {}
        payload.update(data)
        payload['add_photo_done'] = 'Preview'
        payload['filter_type'] = kwargs.get('filter_type', '5')
        payload.update(**kwargs)

        return payload


class Image(Utils):

    def __init__(self, image_path: str, **kwargs):

        if kwargs.get('is_child'):
            self.image_path = self.check_image_path(image_path)
            self.filename = self.image_path.split('/')[-1]
            self.file = open(self.image_path, 'rb')
            self.content_type = 'image/{}'.format(self.filename.split('.')[-1])
        self.nodes = []

    def __repr__(self):
        return "<class 'SfyImage'> {} {}".format(self.file, self.content_type)

    def add_child(self, node):
        self.nodes.append(node)

    @property
    def payload(self):
        return (self.filename, self.file, self.content_type.lower())

    @staticmethod
    def check_image_path(image_path: str) -> str:

        if exists(image_path):
            return image_path

        raise Exception('Image not found, please verify the path!')

    @staticmethod
    def empty_payload(size=1, **kwargs) -> dict:

        limit = kwargs.get('limit', 3)
        content_type = 'application/octet-stream'
        file = ''
        filename = ''
        items = []
        if not size == 0:
            for _ in range(limit-size):
                items.append((filename, file, content_type))
        return items
