from pydantic import BaseModel


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
