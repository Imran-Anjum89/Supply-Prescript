from fastapi import APIRouter

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
)

@router.get("/")
def get_feedback():
    return {
        "message": "feedback API is working"
    }
