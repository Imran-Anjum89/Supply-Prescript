from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Supplier
from schemas import SupplierCreate, SupplierOut

router = APIRouter(tags=["Suppliers"])

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
