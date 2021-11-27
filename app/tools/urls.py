from functools import cached_property

from app.consts import GO_REST_BASIC_URL


class BaseRequestUrls:
    root_url: str

    @cached_property
    def pagination_url(self) -> str:
        return self.root_url + "?page={}"

    @cached_property
    def item_url(self) -> str:
        return self.root_url + "/{}"


class UserUrls(BaseRequestUrls):
    root_url = f"{GO_REST_BASIC_URL}/users"


class PostsUrls(BaseRequestUrls):
    root_url = f"{GO_REST_BASIC_URL}/posts"


class CommentsUrls(BaseRequestUrls):
    root_url = f"{GO_REST_BASIC_URL}/comments"


class TodosUrls(BaseRequestUrls):
    root_url = f"{GO_REST_BASIC_URL}/todos"
