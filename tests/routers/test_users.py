import logging
from random import randint
from time import time

import pytest
from fastapi import status
from requests import Response

from app.tools.models import User, UserPagination
from tests.base_test_class import BaseTest

logger = logging.getLogger(__name__)


class TestUsers(BaseTest):
    expected_user_details: User

    @classmethod
    @pytest.fixture(scope="class")
    def new_user_response(cls) -> Response:
        unique_str = time()
        TestUsers.expected_user_details = User(
            name=f"test {unique_str}",
            email=f"test_{unique_str}@15ce1.com",
            gender="male",
            status="active"
        )
        return cls.client.post("/public/v1/users/", headers=cls.headers, data=cls.expected_user_details.json())

    @pytest.mark.parametrize("is_page", [True, False], ids=["use_page_id", "without_page_id"])
    def test_users_pagination_response(self, is_page):
        """
        Verify the users pagination are:
         1. The response contains meta field with pagination's fields
         2. The response contains data field that contains all list of users
        """
        page_id = 1
        if is_page:
            response: Response = self.client.get(f"/public/v1/users?page={page_id}")
        else:
            response: Response = self.client.get("/public/v1/users")
        assert response.status_code == status.HTTP_200_OK

        logger.info("Covert response data to model '%s'" % UserPagination.__name__)
        data = UserPagination(**response.json())
        assert data.meta.pagination.limit == 20
        assert data.meta.pagination.page == page_id
        assert data.meta.pagination.links.previous is None
        assert data.meta.pagination.links.current.endswith("?page=1")
        assert data.meta.pagination.links.next.endswith("?page=2")

    def test_create_new_user(self, new_user_response: Response):
        """
        Create a new user and verify the following:
         1. The user is created without errors
         2. The status code is correct (201)
        """
        logger.info("Verifying the new user is successfully created")
        assert new_user_response.status_code == status.HTTP_201_CREATED
        result = new_user_response.json()
        logger.info("Verifying the response output")
        assert result["meta"] is None
        assert User(**result["data"]) == self.expected_user_details

    def test_verify_new_user_is_created(self, new_user_response: Response):
        """
        Create a new user and verify is exists in the system
        """
        user_id = new_user_response.json()['data']['id']
        response: Response = self.client.get(f"/public/v1/users/{user_id}")
        logger.info("Verifying the new user is exists in the system")
        assert response.status_code == status.HTTP_200_OK
        assert User(**response.json()["data"]) == self.expected_user_details

    def test_update_user_fields(self, new_user_response: Response):
        """
        Update the name and email fields, and verify the following:
         1. Those fields are updated
         2. The status code is correct (200)
        """
        user_id = new_user_response.json()["data"]["id"]
        new_name = f"test_{time()}"
        self.expected_user_details.name = new_name
        self.expected_user_details.email = f"{new_name}@{self.expected_user_details.email.rsplit('@', maxsplit=1)[1]}"
        logger.info("Updating name and email fields for user-id %s" % user_id)
        response: Response = self.client.put(url=f"/public/v1/users/{user_id}", headers=self.headers,
                                             data=self.expected_user_details.json())
        logger.info("Verifying the response output")
        assert response.status_code == status.HTTP_200_OK
        assert User(**response.json()["data"]) == self.expected_user_details

    def test_delete_user(self, new_user_response):
        """
        Delete the user and verify the following:
         1. The response code is 204
         2. The user not exists in the system
        """
        user_id = new_user_response.json()['data']['id']
        response: Response = self.client.delete(f"/public/v1/users/{user_id}")
        logger.info("Verifying the delete response status is %d" % status.HTTP_204_NO_CONTENT)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        logger.info("Verifying the user-id %s not exists in the system" % status.HTTP_404_NOT_FOUND)
        response: Response = self.client.get(f"/public/v1/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
