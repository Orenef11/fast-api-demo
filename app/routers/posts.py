from fastapi import APIRouter

from app.routes_generator.posts_routes import PostsGenerator
from app.tools.models import Post

router = APIRouter(
    prefix="/public/v1/posts",
    tags=["posts"],
)
posts_generator = PostsGenerator()


@router.get("/")
async def get_posts_as_pagination():
    return posts_generator.get_items()


@router.post("/")
async def create_post(post: Post):
    return posts_generator.create_item(item=post)


@router.get("/{post_id}")
async def get_post_by_id(post_id: int):
    return posts_generator.get_item(prefix=post_id)


@router.put("/{post_id}")
async def update_post(post_id: int, post: Post):
    return posts_generator.update_item(item_id=post_id, item=post)


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    return posts_generator.delete_item(item_id=post_id)


@router.get("?page={page_id}")
async def get_all_posts_by_page_id(page_id: int):
    return posts_generator.get_items(page_id=page_id)

