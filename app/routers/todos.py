from fastapi import APIRouter

from app.tools.data_generator import TodosGenerator
from app.tools.models import Todo

router = APIRouter(
    prefix="/public/v1/todos",
    tags=["todos"],
)
todos_generator = TodosGenerator()


@router.get("/")
async def todos():
    return todos_generator.get_items()


@router.post("/")
async def create_todo(todo: Todo):
    return todos_generator.create_item(item=todo)


@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: int):
    return todos_generator.get_item(prefix=todo_id)


@router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo):
    return todos_generator.update_item(item_id=todo_id, item=todo)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    return todos_generator.delete_item(item_id=todo_id)


@router.get("?page={page_id}")
async def get_all_todos_specific_page(page_id: int):
    return todos_generator.get_items(page_id=page_id)
