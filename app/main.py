from typing import Dict

from fastapi import FastAPI

from app.routers import page_routers

app = FastAPI()

_ = [app.include_router(router) for router in page_routers]


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}
