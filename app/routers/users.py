from typing import Optional

from fastapi import APIRouter

from app.routes_generator.users_routes import UserGenerator
from app.tools.models import User, Post, Todo

router = APIRouter(
    prefix="/public/v1/users",
    tags=["users"],
)
users_generator = UserGenerator()

# http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
@router.get("/")
async def get_users_as_pagination():
    return users_generator.get_items()


@router.post("/")
async def create_user(user: User):
    return users_generator.create_item(item=user)


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    return users_generator.get_item(prefix=user_id)


@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    return users_generator.update_item(item_id=user_id, item=user)


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return users_generator.delete_item(item_id=user_id)


@router.get("/{user_id}/posts")
async def get_user_posts_as_pagination(user_id: int):
    return users_generator.get_item(prefix=f"/{user_id}/posts")


@router.post("/{user_id}/posts")
async def create_user_posts(user_id: int, post: Post):
    return users_generator.create_item(item=post, url_prefix=f"/{user_id}/posts")


@router.get("/{user_id}/todos")
async def get_user_todos_as_pagination(user_id: int):
    return users_generator.get_item(prefix=f"/{user_id}/todos")


@router.post("/{user_id}/todos")
async def create_user_todo(user_id: int, todo: Todo):
    return users_generator.create_item(item=todo, url_prefix=f"/{user_id}/todos")
