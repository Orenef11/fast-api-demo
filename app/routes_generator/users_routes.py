from app.routes_generator.basic_routes import BasicGenerator
from app.tools.urls import UserUrls


class UserGenerator(BasicGenerator):
    urls = UserUrls()
