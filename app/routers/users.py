from fastapi import APIRouter

from app.tools.data_generator import UserGenerator
from app.tools.models import User

router = APIRouter(
    prefix="/public/v1/users",
    tags=["users"],
)
users_generator = UserGenerator()


@router.get("/")
async def users():
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


@router.get("?page={page_id}")
async def get_all_users_specific_page(page_id: int):
    return users_generator.get_items(page_id=page_id)


@router.get("/{user_id}/posts")
async def get_user_posts(user_id: int):
    return users_generator.get_item(prefix=f"/{user_id}/posts")


@router.get("/{user_id}/todos")
async def get_user_todos(user_id: int):
    return users_generator.get_item(prefix=f"/{user_id}/todos")
