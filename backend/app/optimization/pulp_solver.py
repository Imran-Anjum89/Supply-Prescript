import pulp
from typing import Dict, Any

def solve_pulp_prescriptive_recommendation(shipment, delay_prediction: Dict[str, Any], max_budget_extra: float = 1200.0) -> Dict[str, Any]:
    """
    Formulates and solves a PuLP Mixed Integer Linear Programming (MILP) model
    to prescribe optimal delay-mitigation strategies.
    """
    predicted_delay = delay_prediction.get("predicted_delay_days", 2.0)
    current_cost = float(shipment.total_cost or 4500.0)

    options = [
        {
            "name": "Standard Route (No Intervention)",
            "carrier": shipment.carrier,
            "cost_mult": 0.0,
            "time_saved_factor": 0.0,
        },
        {
            "name": "Air Freight Expedite & Expedited Customs Clearance",
            "carrier": "DHL Express (Air Freight)",
            "cost_mult": 0.18,
            "time_saved_factor": 0.70,
        },
        {
            "name": "Priority Express Ocean Line Rerouting",
            "carrier": "FedEx Supply Chain (Air Priority)",
            "cost_mult": 0.10,
            "time_saved_factor": 0.45,
        },
        {
            "name": "Fast-Track Port Terminal Gate Priority",
            "carrier": "OceanNet Logistics",
            "cost_mult": 0.05,
            "time_saved_factor": 0.30,
        }
    ]

    try:
        prob = pulp.LpProblem("SupplyChainPrescription", pulp.LpMaximize)

        x_vars = [pulp.LpVariable(f"x_{i}", cat=pulp.LpBinary) for i in range(len(options))]

        prob += pulp.lpSum(x_vars) == 1, "SelectOneOption"
        prob += pulp.lpSum([x_vars[i] * (options[i]["cost_mult"] * current_cost) for i in range(len(options))]) <= max_budget_extra, "BudgetConstraint"

        VAL_PER_DAY_SAVED = 850.0
        obj_terms = []
        for i in range(len(options)):
            time_saved = predicted_delay * options[i]["time_saved_factor"]
            extra_cost = current_cost * options[i]["cost_mult"]
            net_benefit = (time_saved * VAL_PER_DAY_SAVED) - extra_cost
            obj_terms.append(x_vars[i] * net_benefit)

        prob += pulp.lpSum(obj_terms), "MaximizeNetBenefit"
        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        chosen_idx = 0
        for i in range(len(options)):
            if pulp.value(x_vars[i]) and pulp.value(x_vars[i]) > 0.5:
                chosen_idx = i
                break
    except Exception:
        chosen_idx = 1 if max_budget_extra >= (current_cost * 0.18) else (2 if max_budget_extra >= (current_cost * 0.10) else 3)

    chosen = options[chosen_idx]
    extra_cost = round(current_cost * chosen["cost_mult"], 2)
    time_saved = round(predicted_delay * chosen["time_saved_factor"], 1)

    penalty_avoided = time_saved * 850.0
    roi_score = round((penalty_avoided / max(extra_cost, 100.0)), 1) if extra_cost > 0 else 1.0
    if roi_score < 1.0:
        roi_score = 1.0

    return {
        "suggested_action": chosen["name"],
        "expedited_carrier": chosen["carrier"],
        "estimated_extra_cost": extra_cost,
        "time_saved_days": time_saved,
        "roi_score": roi_score,
        "status": "PENDING"
    }
