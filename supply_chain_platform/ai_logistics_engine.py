import random
import time

class AILogisticsEngine:
    """Mock AI Engine for Logistics Optimization."""

    def predict_delivery_delay(self, route_distance, weather_condition):
        """Predicts delay based on route distance and weather."""
        # Simple heuristic-based 'AI'
        base_delay = route_distance / 1000  # 1 hour per 1000km base

        weather_multipliers = {
            "clear": 1.0,
            "rain": 1.2,
            "storm": 2.0,
            "snow": 1.8
        }

        multiplier = weather_multipliers.get(weather_condition.lower(), 1.0)
        predicted_delay = base_delay * multiplier * random.uniform(0.9, 1.1)

        return round(predicted_delay, 2)

    def optimize_route(self, checkpoints):
        """Simulates route optimization (Traveling Salesman Problem mock)."""
        # Just shuffles for simulation
        optimized = list(checkpoints)
        random.shuffle(optimized)
        return optimized

    def analyze_supply_chain_risk(self, inventory_level, demand_forecast):
        """Analyzes risk of stockout."""
        if inventory_level < (demand_forecast * 0.5):
            return "HIGH: Risk of stockout within 48 hours."
        elif inventory_level < demand_forecast:
            return "MEDIUM: Low stock, replenishment recommended."
        else:
            return "LOW: Healthy inventory levels."

if __name__ == "__main__":
    engine = AILogisticsEngine()
    print(f"Predicted Delay: {engine.predict_delivery_delay(5000, 'storm')} hours")
