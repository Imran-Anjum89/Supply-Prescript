import os
import random
import pandas as pd
import numpy as np

def generate_raw_dataset(num_records=1200, output_path="dataset/raw/supply_chain.csv"):
    np.random.seed(42)
    random.seed(42)
    
    origins = ["Shanghai Port (CN)", "Ningbo-Zhoushan (CN)", "Hamburg Port (DE)", "Shenzhen Port (CN)", "Yokohama (JP)", "Rotterdam (NL)", "Singapore (SG)"]
    destinations = ["Port of Los Angeles (US)", "Port of Long Beach (US)", "Port of New York (US)", "Port of Seattle (US)", "Port of Oakland (US)", "Port of Vancouver (CA)"]
    carriers = ["Maersk Line", "DHL Express", "FedEx Supply Chain", "OceanNet Logistics", "Global Freight Air"]

    data = []
    for i in range(1, num_records + 1):
        trk = f"TRK-{random.randint(100000, 999999)}"
        orig = random.choice(origins)
        dest = random.choice(destinations)
        carr = random.choice(carriers)
        
        transit_days = int(np.random.randint(5, 35))
        quantity = int(np.random.randint(100, 2500))
        unit_cost = float(np.random.uniform(2.5, 12.0))
        total_cost = round(transit_days * np.random.uniform(120, 280) + (quantity * unit_cost * 0.1), 2)
        
        weather_risk = round(float(np.random.uniform(0.05, 0.95)), 2)
        traffic_risk = round(float(np.random.uniform(0.05, 0.95)), 2)
        supplier_reliability = round(float(np.random.uniform(0.70, 0.99)), 2)
        
        # Risk score computation
        risk_score = (weather_risk * 0.40) + (traffic_risk * 0.35) + (transit_days / 40.0 * 0.15) + ((1.0 - supplier_reliability) * 0.10)
        is_delayed = 1 if risk_score > 0.46 else 0
        
        if is_delayed:
            actual_delay_days = round(risk_score * (transit_days * 0.35) + np.random.uniform(1.0, 4.5), 1)
        else:
            actual_delay_days = 0.0

        data.append({
            "tracking_number": trk,
            "origin": orig,
            "destination": dest,
            "carrier": carr,
            "transit_days": transit_days,
            "quantity": quantity,
            "total_cost": total_cost,
            "weather_risk_score": weather_risk,
            "traffic_risk_score": traffic_risk,
            "supplier_reliability": supplier_reliability,
            "delayed": is_delayed,
            "actual_delay_days": actual_delay_days
        })

    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Raw dataset created with {len(df)} records at: {output_path}")
    return df

if __name__ == "__main__":
    generate_raw_dataset()
