from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class Meta(BaseModel):
    class Pagination(BaseModel):
        class Links(BaseModel):
            previous: Optional[HttpUrl]
            current: Optional[HttpUrl]
            next: Optional[HttpUrl]

        total: str
        pages: int
        page: int
        limit: int
        links: Links

    pagination: Pagination


class User(BaseModel):
    name: str
    email: str
    gender: str
    status: str


class Post(BaseModel):
    user_id: int
    title: str
    body: str


class Comment(BaseModel):
    post_id: int
    name: str
    email: str
    body: str


class Todo(BaseModel):
    user_id: int
    title: str
    due_on: str
    status: str


class UserPagination(BaseModel):
    meta: Meta
    data: List[User]


class PostPagination(BaseModel):
    meta: Meta
    data: List[Post]


class CommentPagination(BaseModel):
    meta: Meta
    data: List[Comment]


class TodoPagination(BaseModel):
    meta: Meta
    data: List[Todo]
