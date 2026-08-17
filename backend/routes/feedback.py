from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Decision, Feedback
from schemas import FeedbackRequest, FeedbackOut

router = APIRouter(tags=["Feedback"])

@router.post("/feedback", response_model=FeedbackOut)
def submit_feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    decision = db.query(Decision).filter(Decision.id == req.decision_id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision record not found")
    
    feedback = Feedback(
        decision_id=req.decision_id,
        actual_delay_days=req.actual_delay_days,
        actual_extra_cost=req.actual_extra_cost,
        outcome_rating=req.outcome_rating,
        notes=req.notes
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
