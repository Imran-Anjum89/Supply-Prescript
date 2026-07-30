# SupplyPrescript API Documentation

Base URL: `http://localhost:8000/api/v1`

## Authentication

### `POST /auth/login`
- **Body**: `{ "email": "admin@supplyprescript.com", "password": "password123" }`
- **Response**: Returns JWT token and user info.

### `POST /auth/register`
- **Body**: `{ "email": "user@example.com", "password": "password", "full_name": "Manager", "role": "Logistics Lead" }`

### `GET /auth/me`
- **Headers**: `Authorization: Bearer <token>`

---

## Shipments

### `GET /shipments`
- Returns list of registered logistics shipments.

### `POST /shipment`
- **Body**:
  ```json
  {
    "origin": "Shanghai Port (CN)",
    "destination": "Port of Los Angeles (US)",
    "carrier": "Maersk Line",
    "transit_days": 18,
    "quantity": 850,
    "total_cost": 6200.0,
    "weather_risk_score": 0.72,
    "traffic_risk_score": 0.45
  }
  ```

---

## Predictions (XGBoost ML Engine)

### `POST /predict`
- **Body**: `{ "shipment_id": 1 }`
- **Response**: Returns delay probability, estimated delay days, risk level, feature contributions, and model version.

---

## Optimization (PuLP Prescriptive Solver)

### `POST /recommend`
- **Body**: `{ "shipment_id": 1, "max_budget_extra": 1200.0 }`
- **Response**: Returns PuLP solved optimal mitigation strategy, extra cost, days saved, and ROI score.

---

## Closed-Loop Decisions & Feedback

### `POST /decision`
- **Body**: `{ "recommendation_id": 1, "action_taken": "ACCEPTED", "override_reason": null }`

### `GET /history`
- Returns audit trail of decision recommendations and user actions.

### `POST /feedback`
- **Body**: `{ "decision_id": 1, "actual_delay_days": 1.5, "actual_extra_cost": 250, "outcome_rating": 5, "notes": "Outcome notes" }`

---

## Retraining & Analytics

### `POST /retrain`
- Triggers automated model retraining incorporating closed-loop feedback records.

### `GET /dashboard`
- Aggregates system metrics, risk distributions, decision breakdown, and carrier reliability indices.
