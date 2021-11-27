from typing import overload

import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.consts import HEADERS
from app.tools.urls import BaseRequestUrls


class BasicGenerator:
    urls = BaseRequestUrls()

    @staticmethod
    def _request(method: str, url: str, data: BaseModel = None):
        if method in ["get", "post", "put", "delete"]:
            response = getattr(requests, method)(url, headers=HEADERS, data=data and data.json())
        else:
            raise HTTPException(status_code=500, detail=f"The user-id {url.rsplit('/', maxsplit=1)[1]} is removed")

        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return JSONResponse(status_code=response.status_code, content=response.text and response.json())

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

    def create_item(self, item: BaseModel, url_prefix: str = ""):
        return self._request(method="post", url=self.urls.root_url + url_prefix, data=item)

    def update_item(self, item_id: int, item: BaseModel):
        return self._request(method="put", url=self.urls.item_url.format(item_id), data=item)

    def delete_item(self, item_id: int):
        return self._request(method="delete", url=self.urls.item_url.format(item_id))
