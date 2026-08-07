from fastapi import APIRouter

router = APIRouter(
    prefix="/optimization",
    tags=["optimization"]
)

@router.get("/")
def get_optimization():
    return {
        "message": "optimization API is working"
    }
