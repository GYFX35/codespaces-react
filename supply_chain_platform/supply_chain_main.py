import json
import os
from ai_logistics_engine import AILogisticsEngine, DataEngineeringPipe, TransportOptimizer
from security_tools import SupplyChainSecurityAnalyzer

def load_incoterms():
    path = os.path.join(os.path.dirname(__file__), 'incoterms_data.json')
    with open(path, 'r') as f:
        return json.load(f)

def display_menu():
    print("\n=== Supply Chain & Logistics AI Platform ===")
    print("1. Incoterms Explorer")
    print("2. AI Logistics & Transport Tools")
    print("3. Security & Risk Analyzer (AI)")
    print("4. Data Engineering Pipeline Simulation")
    print("5. Exit")
    print("============================================")

def main():
    incoterms = load_incoterms()
    ai_engine = AILogisticsEngine()
    transport = TransportOptimizer()
    security = SupplyChainSecurityAnalyzer()
    data_eng = DataEngineeringPipe()

    while True:
        display_menu()
        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            print("\nAvailable Incoterms:", ", ".join(incoterms.keys()))
            term = input("Enter term for details: ").upper()
            if term in incoterms:
                data = incoterms[term]
                print(f"\n[{data['name']} - {term}]")
                print(f"Description: {data['description']}")
                print(f"Responsibilities: {data['responsibilities']}")
                print(f"Risk Transfer: {data.get('risk_transfer', 'N/A')}")
                print(f"Cost Transfer: {data.get('cost_transfer', 'N/A')}")
                print(f"Transport Modes: {data.get('transport_modes', 'N/A')}")
            else:
                print("Term not found.")

        elif choice == '2':
            print("\n--- Logistics & Transport AI ---")
            print("a. Delivery Delay Predictor")
            print("b. Multimodal Transport Cost Estimator")
            print("c. Inventory Risk Analysis")
            sub_choice = input("Select sub-option: ").lower()

            if sub_choice == 'a':
                try:
                    dist = float(input("Enter route distance (km): "))
                    weather = input("Enter weather (clear, rain, storm, snow): ").lower()
                    delay = ai_engine.predict_delivery_delay(dist, weather)
                    print(f"\nAI Prediction: Estimated delay of {delay} hours.")
                except ValueError:
                    print("Invalid input.")
            elif sub_choice == 'b':
                try:
                    dist = float(input("Distance (km): "))
                    weight = float(input("Weight (kg): "))
                    mode = input("Mode (Truck, Rail, Sea, Air): ").capitalize()
                    res = transport.calculate_multimodal_cost(dist, weight, mode)
                    print(f"\nTransport Analysis: {res}")
                except ValueError:
                    print("Invalid input.")
            elif sub_choice == 'c':
                try:
                    inv = float(input("Current Inventory: "))
                    demand = float(input("Demand Forecast: "))
                    risk = ai_engine.analyze_supply_chain_risk(inv, demand)
                    print(f"\nAI Risk Assessment: {risk}")
                except ValueError:
                    print("Invalid input.")

        elif choice == '3':
            print("\n--- Security & Risk AI ---")
            print("a. Shipment Anomaly Detection")
            print("b. IoT Device Cyber Risk Assessment")
            print("c. Invoice Integrity Check")
            sub_choice = input("Select sub-option: ").lower()

            if sub_choice == 'a':
                dev = float(input("Route Deviation % (e.g. 10): "))
                temp = float(input("Current Temp: "))
                max_t = float(input("Max Allowed Temp: "))
                res = security.detect_shipment_anomaly({"route_deviation": dev, "temperature": temp, "max_allowed_temp": max_t})
                print(f"\nSecurity Scan: {res}")
            elif sub_choice == 'b':
                prot = input("IoT Protocol (HTTP, MQTT, etc.): ")
                def_c = input("Uses default credentials? (y/n): ").lower() == 'y'
                res = security.assess_iot_cyber_risk({"protocol": prot, "uses_default_creds": def_c})
                print(f"\nCyber Risk Report: {res}")
            elif sub_choice == 'c':
                amt = float(input("Invoice Amount: "))
                vend = input("Vendor ID: ")
                res = security.verify_invoice_integrity("ID-1", amt, vend)
                print(f"\nFraud Analysis: {res}")

        elif choice == '4':
            print("\n--- Data Engineering Pipeline ---")
            batch = int(input("Enter batch size to process: "))
            results = data_eng.simulate_pipeline(batch)
            print(f"\nPipeline Execution Complete: {results}")

        elif choice == '5':
            print("Exiting Supply Chain Platform.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
