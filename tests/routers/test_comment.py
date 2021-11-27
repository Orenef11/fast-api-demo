import logging
from random import randint
from time import time

import pytest
from fastapi import status
from requests import Response

from app.tools.models import Comment, CommentPagination
from tests.base_test_class import BaseTest

logger = logging.getLogger(__name__)


class TestComments(BaseTest):
    expected_comment_details: Comment

    @classmethod
    @pytest.fixture(scope="class")
    def new_comment_response(cls) -> Response:
        unique_str = time()
        posts = cls.client.get("/public/v1/posts/", headers=cls.headers).json()
        TestComments.expected_comment_details = Comment(
            post_id=posts["data"][0]["id"],
            name=f"test {unique_str}",
            email=f"test_{unique_str}@15ce1.com",
            body="test"
        )
        return cls.client.post("/public/v1/comments/", headers=cls.headers, data=cls.expected_comment_details.json())

    @pytest.mark.parametrize("is_page", [True, False], ids=["use_page_id", "without_page_id"])
    def test_comments_pagination_response(self, is_page):
        """
        Verify the users pagination are:
         1. The response contains meta field with pagination's fields
         2. The response contains data field that contains all list of comments
        """
        if is_page:
            response: Response = self.client.get(f"/public/v1/comments?page={randint(1, 5)}")
        else:
            response: Response = self.client.get("/public/v1/comments")
        assert response.status_code == status.HTTP_200_OK

        logger.info("Covert response data to model '%s'", CommentPagination.__name__)
        data = CommentPagination(**response.json())
        assert data.meta.pagination.limit == 20
        assert data.meta.pagination.page == 1
        assert data.meta.pagination.links.previous is None
        assert data.meta.pagination.links.current.endswith("?page=1")
        assert data.meta.pagination.links.next.endswith("?page=2")

    def test_create_new_comment(self, new_comment_response):
        """
        Create a new comment and verify the following:
         1. The comment is created without errors
         2. The status code is correct (201)
        """
        logger.info("Verifying the new comment is successfully created")
        assert new_comment_response.status_code == status.HTTP_201_CREATED
        result = new_comment_response.json()
        logger.info("Verifying the response output")
        assert result["meta"] is None
        assert Comment(**result["data"]) == self.expected_comment_details

    def test_verify_new_comment_is_created(self, new_comment_response):
        """
        Create a new comment and verify is exists in the system
        """
        comment_id = new_comment_response.json()['data']['id']
        response: Response = self.client.get(f"/public/v1/comments/{comment_id}")
        logger.info("Verifying the new comment is exists in the system")
        assert response.status_code == status.HTTP_200_OK
        assert Comment(**response.json()["data"]) == self.expected_comment_details

    def test_update_comment_fields(self, new_comment_response):
        """
        Update the name and email fields, and verify the following:
         1. Those fields are updated
         2. The status code is correct (200)
        """
        comment_id = new_comment_response.json()["data"]["id"]
        new_name = f"test_{time()}"
        self.expected_comment_details.name = new_name
        self.expected_comment_details.email = \
            f"{new_name}@{self.expected_comment_details.email.rsplit('@', maxsplit=1)[1]}"
        logger.info("Updating name and email fields for comment-id %s" % comment_id)
        response: Response = self.client.put(url=f"/public/v1/comments/{comment_id}", headers=self.headers,
                                             data=self.expected_comment_details.json())
        logger.info("Verifying the response output")
        assert response.status_code == status.HTTP_200_OK
        assert Comment(**response.json()["data"]) == self.expected_comment_details

    def test_delete_comment(self, new_comment_response):
        """
        Delete the comment and verify the following:
         1. The response code is 204
         2. The comment not exists in the system
        """
        comment_id = new_comment_response.json()['data']['id']
        response: Response = self.client.delete(f"/public/v1/comments/{comment_id}")
        logger.info("Verifying the delete response status is %d", status.HTTP_204_NO_CONTENT)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        logger.info("Verifying the comment-id %s not exists in the system", status.HTTP_404_NOT_FOUND)
        response: Response = self.client.get(f"/public/v1/comments/{comment_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
