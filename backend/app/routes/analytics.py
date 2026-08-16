from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["Analytics"])

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    return AnalyticsService.get_dashboard_analytics(db)

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    return AnalyticsService.get_dashboard_analytics(db)
