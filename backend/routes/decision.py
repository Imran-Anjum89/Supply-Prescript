from fastapi import APIRouter

router = APIRouter(
    prefix="/decision",
    tags=["decision"]
)

@router.get("/")
def get_decision():
    return {
        "message": "decision API is working"
    }
