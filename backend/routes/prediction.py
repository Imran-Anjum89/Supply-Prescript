from fastapi import APIRouter

router = APIRouter(
    prefix="/prediction",
    tags=["prediction"]
)

@router.get("/")
def get_prediction():
    return {
        "message": "prediction API is working"
    }
