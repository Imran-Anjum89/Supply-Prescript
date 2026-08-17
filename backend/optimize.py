import pulp

def solve_prescriptive_optimization(shipment, delay_prediction, max_budget_extra=1200.0):
    """
    Formulates a PuLP Mixed Integer Linear Programming (MILP) problem to find
    the optimal intervention strategy for mitigating shipment delay risk.
    """
    predicted_delay = delay_prediction.get("predicted_delay_days", 2.0)
    current_cost = shipment.total_cost or 4500.0
    transit_days = shipment.transit_days or 18

    # Define potential mitigation options:
    # Option 0: Do Nothing (Base) - Cost: 0, Time Saved: 0
    # Option 1: Air Expedite (DHL / FedEx) - Cost: 22% of total_cost, Time Saved: 60% of predicted_delay
    # Option 2: Express Ocean Reroute - Cost: 10% of total_cost, Time Saved: 40% of predicted_delay
    # Option 3: Port Priority Handling - Cost: 5% of total_cost, Time Saved: 25% of predicted_delay

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

        # Binary decision variables x_i in {0, 1}
        x_vars = [pulp.LpVariable(f"x_{i}", cat=pulp.LpBinary) for i in range(len(options))]

        # Exactly 1 option must be chosen
        prob += pulp.lpSum(x_vars) == 1, "SelectOneOption"

        # Budget constraint: Extra cost <= max_budget_extra
        prob += pulp.lpSum([x_vars[i] * (options[i]["cost_mult"] * current_cost) for i in range(len(options))]) <= max_budget_extra, "BudgetConstraint"

        # Objective Function: Maximize (Value of Time Saved in dollars - Extra Cost Incurred)
        # Value of delay day saved is estimated at $800/day in inventory/penalty costs
        VAL_PER_DAY_SAVED = 850.0

        obj_terms = []
        for i in range(len(options)):
            time_saved = predicted_delay * options[i]["time_saved_factor"]
            extra_cost = current_cost * options[i]["cost_mult"]
            net_benefit = (time_saved * VAL_PER_DAY_SAVED) - extra_cost
            obj_terms.append(x_vars[i] * net_benefit)

        prob += pulp.lpSum(obj_terms), "MaximizeNetBenefit"

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        # Retrieve chosen option index
        chosen_idx = 0
        for i in range(len(options)):
            if pulp.value(x_vars[i]) and pulp.value(x_vars[i]) > 0.5:
                chosen_idx = i
                break

    except Exception:
        # Fallback heuristic selection
        chosen_idx = 1 if max_budget_extra >= (current_cost * 0.18) else (2 if max_budget_extra >= (current_cost * 0.10) else 3)

    chosen = options[chosen_idx]
    extra_cost = round(current_cost * chosen["cost_mult"], 2)
    time_saved = round(predicted_delay * chosen["time_saved_factor"], 1)

    # ROI Calculation = (Value of Time Saved - Extra Cost) / Extra Cost (min 1.0)
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
