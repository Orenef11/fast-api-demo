from fastapi import APIRouter

from app.routes_generator.comments_routes import CommentsGenerator
from app.tools.models import Comment

router = APIRouter(
    prefix="/public/v1/comments",
    tags=["comments"],
)
comments_generator = CommentsGenerator()


@router.get("/")
async def get_comments_as_pagination():
    return comments_generator.get_items()


@router.post("/")
async def create_comment(comment: Comment):
    return comments_generator.create_item(item=comment)


@router.get("/{comment_id}")
async def get_comment_by_id(comment_id: int):
    return comments_generator.get_item(prefix=comment_id)


@router.put("/{comment_id}")
async def update_comment(comment_id: int, comment: Comment):
    return comments_generator.update_item(item_id=comment_id, item=comment)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int):
    return comments_generator.delete_item(item_id=comment_id)
