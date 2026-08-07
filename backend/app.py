from fastapi import FastAPI

from routes import (
    analytics,
    auth,
    decision,
    feedback,
    optimization,
    prediction,
    retraining,
    shipment,
    supplier,
)

app = FastAPI(title="SupplyPrescript API")

app.include_router(auth.router)
app.include_router(shipment.router)
app.include_router(supplier.router)
app.include_router(prediction.router)
app.include_router(optimization.router)
app.include_router(decision.router)
app.include_router(feedback.router)
app.include_router(analytics.router)
app.include_router(retraining.router)

@app.get("/")
def root():
    return {
        "message": "SupplyPrescript Backend Running",
        "status": "healthy"
    }
