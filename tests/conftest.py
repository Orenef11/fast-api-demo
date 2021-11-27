import json
import os
from pathlib import Path
from typing import Dict

# import localstack_client.session
import pytest
from fastapi.testclient import TestClient

from app.consts import HEADERS
from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as _client:
        yield _client


@pytest.fixture(scope="module")
def headers() -> Dict[str, str]:
    HEADERS["Authorization"] = "Bearer 80dc8410463333e3dd615b241ae8ee337700e51dc01b23276ec1ee0d9819e39e"
    return HEADERS


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        file_path, class_name, test_name = item.nodeid.split("::")
        item.session.results.setdefault(file_path, {}).setdefault(class_name, {})[test_name] = result.outcome


def pytest_sessionfinish(session, exitstatus):
    result_path = Path(os.getcwd()) / "pytest_result.json"
    with open(file=result_path, mode="w", encoding="utf-8") as file:
        json.dump(session.results, file)

#     s3_resource = localstack_client.session.Session().resource('s3')
#     my_bucket = s3_resource.Bucket("go-rest-demo")
#     if not my_bucket.creation_date:
#         my_bucket.create()
#     s3_resource.meta.client.upload_file(Filename=str(result_path), Bucket=my_bucket.name, Key=result_path.name)
#     result_path.unlink()
