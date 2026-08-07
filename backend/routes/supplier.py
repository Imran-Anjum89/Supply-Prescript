from fastapi import APIRouter

router = APIRouter(
    prefix="/supplier",
    tags=["supplier"]
)

@router.get("/")
def get_suppliers():
    return {
        "message": "Supplier API is working"
    }
