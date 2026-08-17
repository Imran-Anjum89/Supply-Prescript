from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth, shipment, prediction, optimization, decision, feedback, retraining, history, analytics
import app.models  # Ensure models are loaded for table creation

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SupplyPrescript API",
    description="Prescriptive Analytics System for Supply Chain Logistics Disruption Management",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers under /api/v1 (as expected by frontend) and root fallback
routers = [auth, shipment, prediction, optimization, decision, feedback, retraining, history, analytics]
for r in routers:
    app.include_router(r.router, prefix="/api/v1")
    app.include_router(r.router)

@app.get("/")
def root():
    return {"message": "SupplyPrescript API is running", "status": "online"}
