from app.routes_generator.basic_routes import BasicGenerator
from app.tools.urls import CommentsUrls


class CommentsGenerator(BasicGenerator):
    urls = CommentsUrls()
