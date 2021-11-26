from .comments import router as comments_router
from .posts import router as post_router
from .todos import router as todos_router
from .users import router as users_router

page_routers = [comments_router, post_router, todos_router, users_router]
