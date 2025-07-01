from fastapi import APIRouter

from .endpoints import (comment_router, meeting_router, review_router,
                        task_router, team_router, user_router)

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(task_router)
main_router.include_router(comment_router)
main_router.include_router(team_router)
main_router.include_router(review_router)
main_router.include_router(meeting_router)
