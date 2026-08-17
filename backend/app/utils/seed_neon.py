import sqlite3
import json
from sqlalchemy import create_engine, text
from app.config import settings

def migrate_sqlite_to_neon():
    print("Connecting to local SQLite...")
    sqlite_conn = sqlite3.connect("supplyprescript.db")
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()

    print("Connecting to Neon PostgreSQL:", settings.DATABASE_URL)
    pg_engine = create_engine(settings.DATABASE_URL)

    with pg_engine.begin() as pg_conn:
        # Migrate users
        users = sqlite_cursor.execute("SELECT * FROM users").fetchall()
        for u in users:
            d = dict(u)
            pg_conn.execute(
                text("INSERT INTO users (id, email, hashed_password, full_name, role, created_at) "
                     "VALUES (:id, :email, :hashed_password, :full_name, :role, :created_at) "
                     "ON CONFLICT (id) DO NOTHING"),
                d
            )
        print(f"Migrated {len(users)} users.")

        # Migrate shipments
        shipments = sqlite_cursor.execute("SELECT * FROM shipments").fetchall()
        for s in shipments:
            d = dict(s)
            pg_conn.execute(
                text("INSERT INTO shipments (id, tracking_number, origin, destination, carrier, transit_days, quantity, total_cost, weather_risk_score, traffic_risk_score, status, created_at) "
                     "VALUES (:id, :tracking_number, :origin, :destination, :carrier, :transit_days, :quantity, :total_cost, :weather_risk_score, :traffic_risk_score, :status, :created_at) "
                     "ON CONFLICT (id) DO NOTHING"),
                d
            )
        print(f"Migrated {len(shipments)} shipments.")

        # Migrate predictions
        predictions = sqlite_cursor.execute("SELECT * FROM predictions").fetchall()
        for p in predictions:
            d = dict(p)
            if isinstance(d.get("feature_contributions"), dict):
                d["feature_contributions"] = json.dumps(d["feature_contributions"])
            elif d.get("feature_contributions") is None:
                d["feature_contributions"] = None

            pg_conn.execute(
                text("INSERT INTO predictions (id, shipment_id, delay_probability, predicted_delay_days, risk_level, feature_contributions, model_version, created_at) "
                     "VALUES (:id, :shipment_id, :delay_probability, :predicted_delay_days, :risk_level, :feature_contributions, :model_version, :created_at) "
                     "ON CONFLICT (id) DO NOTHING"),
                d
            )
        print(f"Migrated {len(predictions)} predictions.")

        # Migrate recommendations
        recommendations = sqlite_cursor.execute("SELECT * FROM recommendations").fetchall()
        for r in recommendations:
            d = dict(r)
            pg_conn.execute(
                text("INSERT INTO recommendations (id, shipment_id, suggested_action, expedited_carrier, estimated_extra_cost, time_saved_days, roi_score, status, created_at) "
                     "VALUES (:id, :shipment_id, :suggested_action, :expedited_carrier, :estimated_extra_cost, :time_saved_days, :roi_score, :status, :created_at) "
                     "ON CONFLICT (id) DO NOTHING"),
                d
            )
        print(f"Migrated {len(recommendations)} recommendations.")

        # Migrate decisions
        decisions = sqlite_cursor.execute("SELECT * FROM decisions").fetchall()
        for dec in decisions:
            d = dict(dec)
            pg_conn.execute(
                text("INSERT INTO decisions (id, recommendation_id, shipment_id, action_taken, override_reason, timestamp) "
                     "VALUES (:id, :recommendation_id, :shipment_id, :action_taken, :override_reason, :timestamp) "
                     "ON CONFLICT (id) DO NOTHING"),
                d
            )
        print(f"Migrated {len(decisions)} decisions.")

        # Migrate feedbacks
        feedbacks = sqlite_cursor.execute("SELECT * FROM feedbacks").fetchall()
        for f in feedbacks:
            d = dict(f)
            pg_conn.execute(
                text("INSERT INTO feedbacks (id, decision_id, actual_delay_days, actual_extra_cost, outcome_rating, notes, created_at) "
                     "VALUES (:id, :decision_id, :actual_delay_days, :actual_extra_cost, :outcome_rating, :notes, :created_at) "
                     "ON CONFLICT (id) DO NOTHING"),
                d
            )
        print(f"Migrated {len(feedbacks)} feedbacks.")

        # Reset PostgreSQL serial sequences
        tables = ["users", "shipments", "predictions", "recommendations", "decisions", "feedbacks"]
        for t in tables:
            pg_conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{t}', 'id'), COALESCE(MAX(id), 1)) FROM {t}"))

    print("Data migration to Neon Cloud PostgreSQL finished successfully!")

if __name__ == "__main__":
    migrate_sqlite_to_neon()
