from app.routes_generator.basic_routes import BasicGenerator
from app.tools.urls import PostsUrls


class PostsGenerator(BasicGenerator):
    urls = PostsUrls()
