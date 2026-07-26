# SupplyPrescript 📦 Prescriptive Supply Chain Analytics

SupplyPrescript is an end-to-end, closed-loop prescriptive analytics system for supply chain logistics disruption management.

## 🚀 Key Features

- **XGBoost Machine Learning Disruption Risk Prediction**: Evaluates delay probabilities, estimated delay days, risk levels, and top risk factors.
- **PuLP Mixed Integer Linear Programming (MILP) Prescriptions**: Computes optimal mitigation strategies (e.g. air freight expediting, rerouting, priority port clearance) under strict extra budget constraints.
- **Human-in-the-Loop PostgreSQL Audit Trail**: Logs user acceptance or override reasons.
- **Closed-Loop Feedback & Retraining Loop**: Captures actual operational outcomes to retrain prediction models automatically.
- **Modern Glassmorphic React Dashboard**: Built with Vite, React, Recharts, and Lucide Icons.

## 🛠 Project Structure

```
SupplyPrescript/
├── backend/
│   ├── app.py                # FastAPI Main Application & Routers
│   ├── database.py           # SQLAlchemy Database Engine & SQLite Fallback
│   ├── models.py             # ORM Models (Shipments, Predictions, Prescriptions, Decisions)
│   ├── schemas.py            # Pydantic Schemas
│   ├── predict.py            # ML Risk Inference Module
│   ├── optimize.py           # PuLP Optimization Prescriptive Solver
│   ├── retrain.py            # Model Retraining Manager
│   ├── routes/               # API Endpoints (/auth, /shipment, /predict, /recommend, etc.)
│   └── requirements.txt      # Python Dependencies
├── frontend/                 # Vite + React Frontend Application
├── ml/
│   ├── preprocess.py         # ML Feature Engineering
│   ├── train.py              # ML Training Pipeline
│   └── model.pkl             # Serialized ML Model
└── docker-compose.yml        # Multi-Container Deployment
```

## 🏁 Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```
API Documentation will be available at: http://localhost:8000/docs

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
Frontend App will be available at: http://localhost:5173
