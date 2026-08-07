from fastapi import APIRouter

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"]
)

@router.get("/")
def get_shipments():
    return {
        "message": "Supplier API is working"
    }
