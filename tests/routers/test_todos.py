import logging
from datetime import datetime
from random import randint
from time import time

import pytest
from fastapi import status
from requests import Response

from app.tools.models import Todo, TodoPagination
from tests.base_test_class import BaseTest

logger = logging.getLogger(__name__)


def create_todo_datetime_format() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+05:30"


class TestTodos(BaseTest):
    expected_todo_details: Todo

    @classmethod
    @pytest.fixture(scope="class")
    def new_todo_response(cls) -> Response:
        unique_str = time()
        users = cls.client.get("/public/v1/users/", headers=cls.headers).json()
        user_id = users["data"][0]["id"]
        TestTodos.expected_todo_details = Todo(
            user_id=users["data"][0]["id"],
            title=f"test {unique_str}",
            due_on=create_todo_datetime_format(),
            status="pending"
        )
        return cls.client.post(f"/public/v1/users/{user_id}/todos", headers=cls.headers,
                               data=cls.expected_todo_details.json())

    @pytest.mark.parametrize("is_page", [True, False], ids=["use_page_id", "without_page_id"])
    def test_todos_pagination_response(self, is_page):
        """
        Verify the todos pagination are:
         1. The response contains meta field with pagination's fields
         2. The response contains data field that contains all list of todos
        """
        if is_page:
            response: Response = self.client.get(f"/public/v1/todos?page={randint(1, 5)}")
        else:
            response: Response = self.client.get("/public/v1/todos")
        assert response.status_code == status.HTTP_200_OK

        logger.info("Covert response data to model '%s'", TodoPagination.__name__)
        data = TodoPagination(**response.json())
        assert data.meta.pagination.limit == 20
        assert data.meta.pagination.page == 1
        assert data.meta.pagination.links.previous is None
        assert data.meta.pagination.links.current.endswith("?page=1")
        assert data.meta.pagination.links.next.endswith("?page=2")

    def test_create_new_todo(self, new_todo_response):
        """
        Create a new todo1 and verify the following:
         1. The todo1 is created without errors
         2. The status code is correct (201)
        """
        logger.info("Verifying the new todo is successfully created")
        assert new_todo_response.status_code == status.HTTP_201_CREATED
        result = new_todo_response.json()
        logger.info("Verifying the response output")
        assert Todo(**result["data"]) == self.expected_todo_details

    def test_verify_new_todo_is_created(self, new_todo_response):
        """
        Create a new todo1 and verify is exists in the system
        """
        todo_id = new_todo_response.json()['data']['id']
        response: Response = self.client.get(f"/public/v1/todos/{todo_id}")
        logger.info("Verifying the new todo is exists in the system")
        assert response.status_code == status.HTTP_200_OK
        assert Todo(**response.json()["data"]) == self.expected_todo_details

    def test_update_todo_fields(self, new_todo_response):
        """
        Update the title and due_on fields, and verify the following:
         1. Those fields are updated
         2. The status code is correct (200)
        """
        todo_id = new_todo_response.json()["data"]["id"]
        self.expected_todo_details.title = f"test_{time()}"
        self.expected_todo_details.due_on = create_todo_datetime_format()
        logger.info("Updating name and email fields for todo-id %s", todo_id)
        response: Response = self.client.put(url=f"/public/v1/todos/{todo_id}", headers=self.headers,
                                             data=self.expected_todo_details.json())
        logger.info("Verifying the response output")
        assert response.status_code == status.HTTP_200_OK
        assert Todo(**response.json()["data"]) == self.expected_todo_details

    def test_delete_todo(self, new_todo_response):
        """
        Delete the todo1 and verify the following:
         1. The response code is 204
         2. The todo1 not exists in the system
        """
        todo_id = new_todo_response.json()['data']['id']
        response: Response = self.client.delete(f"/public/v1/todos/{todo_id}")
        logger.info("Verifying the delete response status is %d", status.HTTP_204_NO_CONTENT)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        logger.info("Verifying the todo-id %s not exists in the system", status.HTTP_404_NOT_FOUND)
        response: Response = self.client.get(f"/public/v1/todos/{todo_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
