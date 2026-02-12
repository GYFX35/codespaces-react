import json
import os
from ai_logistics_engine import AILogisticsEngine

def load_incoterms():
    path = os.path.join(os.path.dirname(__file__), 'incoterms_data.json')
    with open(path, 'r') as f:
        return json.load(f)

def display_menu():
    print("\n=== Supply Chain & Logistics AI Platform ===")
    print("1. Incoterms Lookup")
    print("2. AI Delivery Delay Predictor")
    print("3. Inventory Risk Analysis")
    print("4. Exit")
    print("============================================")

def main():
    incoterms = load_incoterms()
    ai_engine = AILogisticsEngine()

    while True:
        display_menu()
        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            print("\nAvailable Incoterms:", ", ".join(incoterms.keys()))
            term = input("Enter term for details: ").upper()
            if term in incoterms:
                data = incoterms[term]
                print(f"\n[{data['name']}]")
                print(f"Description: {data['description']}")
                print(f"Responsibilities: {data['responsibilities']}")
            else:
                print("Term not found.")

        elif choice == '2':
            try:
                dist = float(input("Enter route distance (km): "))
                weather = input("Enter weather (clear, rain, storm, snow): ").lower()
                delay = ai_engine.predict_delivery_delay(dist, weather)
                print(f"\nAI Prediction: Estimated delay of {delay} hours due to {weather} conditions over {dist}km.")
            except ValueError:
                print("Invalid distance.")

        elif choice == '3':
            try:
                inv = float(input("Current Inventory Level: "))
                demand = float(input("Forecasted Demand: "))
                risk = ai_engine.analyze_supply_chain_risk(inv, demand)
                print(f"\nAI Risk Assessment: {risk}")
            except ValueError:
                print("Invalid numbers.")

        elif choice == '4':
            print("Exiting Supply Chain Platform.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
