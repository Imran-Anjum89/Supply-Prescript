from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Shipment
from schemas import ShipmentCreate, ShipmentResponse

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"]
)

@router.get("/", response_model=list[ShipmentResponse])
def get_shipments(db: Session = Depends(get_db)):
    return db.query(Shipment).all()


@router.post("/", response_model=ShipmentResponse)
def create_shipment(
    shipment: ShipmentCreate,
    db: Session = Depends(get_db)
):
    new_shipment = Shipment(**shipment.model_dump())
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment
