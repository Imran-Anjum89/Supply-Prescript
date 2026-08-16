from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.decision import Decision
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackRequest

class FeedbackService:
    @staticmethod
    def submit_feedback(db: Session, req: FeedbackRequest) -> Feedback:
        decision = db.query(Decision).filter(Decision.id == req.decision_id).first()
        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")

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
