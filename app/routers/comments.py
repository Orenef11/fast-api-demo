from fastapi import APIRouter

from app.tools.data_generator import CommentsGenerator
from app.tools.models import Comment

router = APIRouter(
    prefix="/public/v1/comments",
    tags=["comments"],
)
comments_generator = CommentsGenerator()


@router.get("/")
async def comments():
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


@router.get("?page={page_id}")
async def get_all_comments_specific_page(page_id: int):
    return comments_generator.get_items(page_id=page_id)


@router.get("?page={page_id}")
async def get_all_comments_specific_page(page_id: int):
    return comments_generator.get_items(page_id=page_id)
