from typing import overload

import requests
from fastapi import HTTPException
from pydantic import BaseModel

from app.consts import HEADERS
from app.tools.urls import BaseRequestUrls, UserUrls, PostsUrls, CommentsUrls


class BasicGenerator:
    headers = HEADERS
    urls = BaseRequestUrls()

    @staticmethod
    def _request(method: str, url: str, data: BaseModel = None):
        data = data and data.json()
        if method == "get":
            response = requests.get(url, headers=HEADERS)
        elif method == "post":
            response = requests.post(url, headers=HEADERS, data=data)
        elif method == "put":
            response = requests.put(url, headers=HEADERS, data=data)
        elif method == "delete":
            response = requests.delete(url, headers=HEADERS)
            if response.status_code == 204:
                return {"status_code": 204, "message": f"The user-id {url.rsplit('/', maxsplit=1)[1]} is removed"}
        else:
            raise HTTPException(status_code=500, detail=f"The user-id {url.rsplit('/', maxsplit=1)[1]} is removed")

        return response.json()

    @overload
    def get_item(self, prefix: int):
        ...

    @overload
    def get_item(self, prefix: str):
        ...

    def get_item(self, prefix: str | int):
        if isinstance(prefix, str):
            return self._request(method="get", url=self.urls.root_url + prefix)
        return self._request(method="get", url=self.urls.item_url.format(prefix))

    def get_items(self, page_id: int = 1):
        if page_id:
            url = self.urls.pagination_url.format(page_id)
        else:
            url = self.urls.root_url
        return self._request(method="get", url=url)

    def create_item(self, item: BaseModel):
        return self._request(method="post", url=self.urls.root_url, data=item)

    def update_item(self, item_id: int, item: BaseModel):
        return self._request(method="put", url=self.urls.item_url.format(item_id), data=item)

    def delete_item(self, item_id: int):
        return self._request(method="delete", url=self.urls.item_url.format(item_id))


class UserGenerator(BasicGenerator):
    urls = UserUrls()


class PostsGenerator(BasicGenerator):
    urls = PostsUrls()


class CommentsGenerator(BasicGenerator):
    urls = CommentsUrls()


class TodosGenerator(BasicGenerator):
    urls = CommentsUrls()
