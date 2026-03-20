import re

class CloudSecurityAI:
    """AI for auditing cloud configurations and identifying security misconfigurations."""

    def audit_config(self, config_text):
        findings = []
        if "0.0.0.0/0" in config_text and "SSH" in config_text:
            findings.append("Open SSH port (22) to the world (0.0.0.0/0).")
        if "Allow" in config_text and "All" in config_text and "Inbound" in config_text:
            findings.append("Overly permissive inbound security group rule.")
        if "s3" in config_text.lower() and "public-read" in config_text.lower():
            findings.append("S3 bucket with public read access detected.")

        if not findings:
            return {"status": "SECURE", "findings": ["No immediate cloud misconfigurations detected."]}
        return {"status": "RISK_DETECTED", "findings": findings}

class IoTSecurityAI:
    """AI for analyzing IoT telemetry and detecting tampering or anomalies."""

    def analyze_telemetry(self, telemetry_data):
        # Expecting telemetry_data to be a dict
        findings = []
        voltage = telemetry_data.get('voltage')
        temp = telemetry_data.get('temperature')

        if voltage is not None and voltage < 3.0:
            findings.append(f"Low voltage ({voltage}V) - potential battery tampering or exhaustion.")
        if temp is not None and temp > 85:
            findings.append(f"High temperature ({temp}°C) - possible hardware stress or cooling failure.")

        if not findings:
            return {"status": "STABLE", "findings": ["IoT telemetry within normal parameters."]}
        return {"status": "ANOMALY", "findings": findings}

class OpSecAI:
    """AI for scanning operational logs and detecting security-sensitive patterns."""

    def scan_logs(self, log_text):
        findings = []
        # Basic secret detection (similar to sensitive_data_scanner)
        if re.search(r"AKIA[0-9A-Z]{16}", log_text):
            findings.append("Potential AWS Access Key ID found in logs.")
        if re.search(r"AIza[0-9A-Za-z\-_]{35}", log_text):
            findings.append("Potential Google API Key found in logs.")
        if "password" in log_text.lower() and ":" in log_text:
            findings.append("Possible plaintext password found in log entry.")

        if not findings:
            return {"status": "CLEAR", "findings": ["No operational security threats found in logs."]}
        return {"status": "THREAT_DETECTED", "findings": findings}
