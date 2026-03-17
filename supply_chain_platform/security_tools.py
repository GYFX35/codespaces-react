import re
import random

class InfrastructureProtectionAI:
    """AI role for protecting critical infrastructure and IoT devices."""

    def detect_iot_tampering(self, device_data):
        """
        Analyzes IoT device telemetry for signs of physical or digital tampering.

        Args:
            device_data (dict): Telemetry data including voltage, temperature, and signal strength.
        """
        anomalies = []

        # Heuristic: Rapid voltage drop might indicate a power-side attack or battery tampering
        if device_data.get('voltage', 3.3) < 2.8:
            anomalies.append("Low voltage detected - possible power source tampering.")

        # Heuristic: Temperature spikes outside industrial operating range
        if device_data.get('temperature', 25) > 75:
            anomalies.append("Extreme temperature spike - potential hardware stress or overheating attack.")

        # Heuristic: Signal RSSI fluctuations
        if device_data.get('rssi', -50) < -90:
            anomalies.append("Weak signal (low RSSI) - potential signal jamming or interference.")

        if not anomalies:
            return {"status": "SECURE", "score": 0, "findings": ["Normal operating parameters."]}
        else:
            return {
                "status": "WARNING",
                "score": len(anomalies) * 3,
                "findings": anomalies
            }

    def assess_facility_vulnerability(self, access_logs):
        """
        AI assessment of facility security based on access logs.
        """
        unauthorized_attempts = [log for log in access_logs if log.get('status') == 'DENIED']

        if len(unauthorized_attempts) > 5:
            return "HIGH RISK: Multiple unauthorized access attempts detected at perimeter."
        elif len(unauthorized_attempts) > 0:
            return "MEDIUM RISK: Occasional unauthorized access attempts detected."
        else:
            return "LOW RISK: Perimeter security appears intact."


class AntivirusIdentificationAI:
    """AI role for identifying malware signatures and suspicious file behaviors."""

    SUSPICIOUS_EXTENSIONS = ['.exe', '.sh', '.bat', '.bin', '.scr']

    def scan_file_metadata(self, filename, filesize_kb):
        """
        Identifies potential threats based on file metadata heuristics.
        """
        findings = []
        ext = '.' + filename.split('.')[-1] if '.' in filename else ''

        if ext.lower() in self.SUSPICIOUS_EXTENSIONS:
            findings.append(f"Suspicious executable extension: {ext}")

        if filesize_kb < 1:
            findings.append("Unusually small file size - potential dropper or script.")

        if not findings:
            return {"risk": "LOW", "details": "File metadata appears standard."}
        else:
            return {"risk": "MEDIUM", "details": findings}

    def identify_malware_behavior_patterns(self, execution_logs):
        """
        Scans execution logs for behavior patterns consistent with malware (e.g. ransomware, spyware).
        """
        patterns = {
            "Ransomware": ["mass_file_rename", "encryption_started", "delete_shadow_copies"],
            "Spyware": ["unauthorized_camera_access", "keystroke_logging", "exfiltrating_data"],
            "Worm": ["rapid_network_scanning", "self_replication_attempt"]
        }

        detected_threats = []
        logs_flat = " ".join(execution_logs).lower()

        for threat, indicators in patterns.items():
            for indicator in indicators:
                if indicator in logs_flat:
                    detected_threats.append(f"{threat} indicator: {indicator}")

        return detected_threats if detected_threats else ["No malicious behavior patterns detected."]

if __name__ == "__main__":
    # Test Infrastructure Protection
    infra_ai = InfrastructureProtectionAI()
    test_device = {'voltage': 2.5, 'temperature': 80, 'rssi': -95}
    print("IoT Tampering Analysis:", infra_ai.detect_iot_tampering(test_device))

    # Test Antivirus ID
    av_ai = AntivirusIdentificationAI()
    print("File Scan:", av_ai.scan_file_metadata("update.bat", 0.5))
    print("Behavior Analysis:", av_ai.identify_malware_behavior_patterns(["encryption_started", "delete_shadow_copies"]))
