from app.routes_generator.basic_routes import BasicGenerator
from app.tools.urls import TodosUrls


class TodosGenerator(BasicGenerator):
    urls = TodosUrls()
