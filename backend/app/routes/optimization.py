from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.recommendation import Recommendation
from app.schemas.recommendation_schema import RecommendRequest, RecommendationOut
from app.services.optimization_service import OptimizationService

router = APIRouter(tags=["Optimization"])

@router.post("/recommend", response_model=RecommendationOut)
def recommend_prescription(req: RecommendRequest, db: Session = Depends(get_db)):
    return OptimizationService.generate_recommendation(db, req.shipment_id, req.max_budget_extra)

@router.get("/recommendations/shipment/{shipment_id}", response_model=List[RecommendationOut])
def get_recommendations(shipment_id: int, db: Session = Depends(get_db)):
    return db.query(Recommendation).filter(Recommendation.shipment_id == shipment_id).order_by(Recommendation.created_at.desc()).all()
