import json
import os
from ai_logistics_engine import AILogisticsEngine
from security_tools import InfrastructureProtectionAI, AntivirusIdentificationAI

def load_incoterms():
    path = os.path.join(os.path.dirname(__file__), 'incoterms_data.json')
    with open(path, 'r') as f:
        return json.load(f)

def display_menu():
    print("\n=== Supply Chain & Logistics AI Platform ===")
    print("1. Incoterms Lookup")
    print("2. AI Delivery Delay Predictor")
    print("3. Inventory Risk Analysis")
    print("4. Security Analysis (Infrastructure & AV)")
    print("5. Exit")
    print("============================================")

def main():
    incoterms = load_incoterms()
    ai_engine = AILogisticsEngine()
    infra_ai = InfrastructureProtectionAI()
    av_ai = AntivirusIdentificationAI()

    while True:
        display_menu()
        choice = input("Enter choice (1-5): ").strip()

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
            print("\n--- Security Analysis ---")
            print("1. IoT Tampering Detection")
            print("2. Antivirus Metadata Scan")
            sec_choice = input("Select sub-option (1-2): ").strip()

            if sec_choice == '1':
                v = float(input("Enter device voltage: "))
                t = float(input("Enter device temperature: "))
                r = float(input("Enter signal RSSI: "))
                result = infra_ai.detect_iot_tampering({'voltage': v, 'temperature': t, 'rssi': r})
                print(f"\nResult: {result['status']} (Score: {result['score']})")
                for f in result['findings']:
                    print(f" - {f}")
            elif sec_choice == '2':
                fname = input("Enter filename: ")
                fsize = float(input("Enter file size (KB): "))
                result = av_ai.scan_file_metadata(fname, fsize)
                print(f"\nRisk Level: {result['risk']}")
                print(f"Details: {result['details']}")

        elif choice == '5':
            print("Exiting Supply Chain Platform.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
