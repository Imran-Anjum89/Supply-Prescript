from typing import Dict, Any

class ConstraintService:
    @staticmethod
    def validate_budget_constraint(extra_cost: float, max_budget: float) -> bool:
        return extra_cost <= max_budget

    @staticmethod
    def calculate_max_allowed_delay(transit_days: int, sla_margin: float = 0.2) -> float:
        return transit_days * sla_margin
