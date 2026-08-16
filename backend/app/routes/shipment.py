from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.shipment import Shipment
from app.models.supplier import Supplier
from app.schemas.shipment_schema import ShipmentCreate, ShipmentOut, SupplierCreate, SupplierOut
from app.utils.helper import generate_tracking_number

router = APIRouter(tags=["Shipments & Suppliers"])

@router.get("/shipments", response_model=List[ShipmentOut])
def list_shipments(db: Session = Depends(get_db)):
    return db.query(Shipment).order_by(Shipment.created_at.desc()).all()

@router.post("/shipment", response_model=ShipmentOut)
def create_shipment(shipment_in: ShipmentCreate, db: Session = Depends(get_db)):
    is_high_risk = shipment_in.weather_risk_score > 0.5 or shipment_in.traffic_risk_score > 0.5
    status_str = "DELAY_RISK" if is_high_risk else "ON_TIME"

    shipment = Shipment(
        tracking_number=generate_tracking_number(),
        origin=shipment_in.origin,
        destination=shipment_in.destination,
        carrier=shipment_in.carrier,
        transit_days=shipment_in.transit_days,
        quantity=shipment_in.quantity,
        total_cost=shipment_in.total_cost,
        weather_risk_score=shipment_in.weather_risk_score,
        traffic_risk_score=shipment_in.traffic_risk_score,
        status=status_str
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment

@router.get("/shipment/{shipment_id}", response_model=ShipmentOut)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@router.put("/shipment/{shipment_id}", response_model=ShipmentOut)
def update_shipment(shipment_id: int, shipment_in: ShipmentCreate, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    for field, val in shipment_in.model_dump().items():
        setattr(shipment, field, val)
    db.commit()
    db.refresh(shipment)
    return shipment

@router.delete("/shipment/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db.delete(shipment)
    db.commit()
    return {"message": "Shipment deleted"}

@router.get("/suppliers", response_model=List[SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.post("/suppliers", response_model=SupplierOut)
def create_supplier(supplier_in: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**supplier_in.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier
