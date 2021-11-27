from copy import copy
from typing import Dict

import pytest
from aiohttp.test_utils import TestClient


class BaseTest:
    client: TestClient
    headers: Dict[str, str]

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def pre_setup(cls, client: TestClient, headers: Dict[str, str]):
        BaseTest.client = client
        BaseTest.headers = copy(headers)
