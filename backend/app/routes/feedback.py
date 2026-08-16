from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.feedback_schema import FeedbackRequest, FeedbackOut
from app.services.feedback_service import FeedbackService

router = APIRouter(tags=["Feedback"])

@router.post("/feedback", response_model=FeedbackOut)
def submit_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    return FeedbackService.submit_feedback(db, req)
