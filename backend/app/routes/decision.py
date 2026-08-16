from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.decision_schema import DecisionRequest, DecisionOut
from app.services.decision_service import DecisionService

router = APIRouter(tags=["Decisions"])

@router.post("/decision", response_model=DecisionOut)
def record_decision(req: DecisionRequest, db: Session = Depends(get_db)):
    return DecisionService.record_decision(db, req)
