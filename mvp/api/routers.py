from fastapi import APIRouter

from .endpoints import user_router, task_router, comment_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(task_router)
main_router.include_router(comment_router)
