import random
import hashlib
import time

class SupplyChainSecurityAnalyzer:
    """AI-driven security analyzer for Supply Chain and Logistics."""

    def detect_shipment_anomaly(self, shipment_data):
        """
        Detects anomalies in shipment tracking data.
        shipment_data: dict with 'current_location', 'expected_route', 'temperature', etc.
        """
        anomalies = []

        # 1. Route Deviation Check
        if shipment_data.get('route_deviation', 0) > 15: # > 15% deviation
            anomalies.append(f"CRITICAL: Major route deviation detected ({shipment_data['route_deviation']}%).")

        # 2. Environmental Security (e.g., Cold Chain)
        temp = shipment_data.get('temperature')
        max_temp = shipment_data.get('max_allowed_temp')
        if temp and max_temp and temp > max_temp:
            anomalies.append(f"WARNING: Temperature excursion detected: {temp}°C (Max: {max_temp}°C).")

        # 3. Unscheduled Stops
        if shipment_data.get('unscheduled_stops', 0) > 2:
            anomalies.append("SUSPICIOUS: Multiple unscheduled stops in high-risk zone.")

        if not anomalies:
            return "SECURE: No anomalies detected in current shipment telemetry."
        return " | ".join(anomalies)

    def assess_iot_cyber_risk(self, device_info):
        """
        Assesses cybersecurity risk for IoT sensors used in logistics.
        device_info: dict with 'firmware_version', 'last_patch_date', 'protocol'
        """
        score = 100
        reasons = []

        # Outdated Firmware
        if device_info.get('outdated_firmware', False):
            score -= 30
            reasons.append("Outdated firmware version.")

        # Insecure Protocol
        if device_info.get('protocol') in ['HTTP', 'Telnet', 'MQTT-Unencrypted']:
            score -= 40
            reasons.append(f"Insecure communication protocol: {device_info.get('protocol')}.")

        # Default Credentials (simulated check)
        if device_info.get('uses_default_creds', False):
            score -= 50
            reasons.append("Device using default administrative credentials.")

        risk_level = "LOW"
        if score < 40: risk_level = "CRITICAL"
        elif score < 70: risk_level = "MEDIUM"

        return {
            "risk_score": max(0, score),
            "risk_level": risk_level,
            "vulnerabilities": reasons if reasons else ["None detected"]
        }

    def verify_invoice_integrity(self, invoice_id, amount, vendor_id):
        """
        Simulates AI fraud detection for logistics invoices.
        Checks for duplicate billing or anomalous amounts.
        """
        # Simulated 'AI' logic
        if amount > 50000 and vendor_id == "NEW_VENDOR":
            return "FLAGGED: High-value invoice from unverified new vendor. Manual audit required."

        # Simulate check against previous averages
        if random.random() < 0.05: # 5% chance of simulating a fraudulent match
             return "FLAGGED: Potential duplicate invoice detected (ID match with 2023-X92)."

        return "VERIFIED: Invoice matches historical patterns and vendor profile."

if __name__ == "__main__":
    analyzer = SupplyChainSecurityAnalyzer()

    # Test Shipment Anomaly
    print("--- Shipment Security Check ---")
    shipment = {"route_deviation": 20, "temperature": -2, "max_allowed_temp": -10}
    print(analyzer.detect_shipment_anomaly(shipment))

    # Test IoT Risk
    print("\n--- IoT Cybersecurity Assessment ---")
    device = {"protocol": "HTTP", "uses_default_creds": True}
    print(analyzer.assess_iot_cyber_risk(device))

    # Test Invoice Integrity
    print("\n--- Logistics Fraud Detection ---")
    print(analyzer.verify_invoice_integrity("INV-001", 75000, "NEW_VENDOR"))
