import re
from sensitive_data_scanner.scanner import SENSITIVE_DATA_PATTERNS
from supply_chain_platform.security_tools import InfrastructureProtectionAI

class CloudSecurityAI:
    """AI for scanning cloud credentials and sensitive information."""

    def _redact(self, value):
        """Redacts a sensitive string, keeping only the first 4 and last 4 characters."""
        if len(value) <= 10:
            return "****"
        return f"{value[:4]}...{value[-4:]}"

    def scan_content(self, text_content):
        findings = {}
        for pattern_name, regex in SENSITIVE_DATA_PATTERNS.items():
            matches = regex.findall(text_content)
            if matches:
                # Redact each match to avoid full exposure
                findings[pattern_name] = [self._redact(m) for m in matches]
        return findings

class IoTSecurityAI:
    """AI for monitoring IoT device telemetry and detecting anomalies."""

    def __init__(self):
        self.infra_protection = InfrastructureProtectionAI()

    def analyze_telemetry(self, device_data):
        """
        Wraps the InfrastructureProtectionAI logic for IoT telemetry analysis.
        """
        return self.infra_protection.detect_iot_tampering(device_data)

class OpSecAI:
    """AI for Operational Security (OpSec) analysis of logs and procedures."""

    SUSPICIOUS_OPSEC_PATTERNS = {
        "Unauthorized Login Attempt": re.compile(r"failed login|unauthorized access|invalid credentials", re.I),
        "Privilege Escalation": re.compile(r"sudo usage|root access granted|privilege elevation", re.I),
        "Data Exfiltration Pattern": re.compile(r"large outbound transfer|data dump|exfiltrating", re.I),
        "Internal Scan Activity": re.compile(r"nmap scan|port sweep|internal reconnaissance", re.I),
        "Insecure Communication": re.compile(r"http transfer|unencrypted channel|plaintext password", re.I)
    }

    def analyze_logs(self, log_entries):
        """
        Analyzes a list of log strings for operational security risks.
        """
        risk_score = 0
        findings = []

        log_blob = "\n".join(log_entries)

        for threat_name, regex in self.SUSPICIOUS_OPSEC_PATTERNS.items():
            matches = regex.findall(log_blob)
            if matches:
                findings.append(f"{threat_name} detected: {len(matches)} occurrences.")
                risk_score += len(matches) * 2

        if not findings:
            return {"status": "SECURE", "score": 0, "findings": ["No operational security threats detected."]}
        else:
            status = "CRITICAL" if risk_score > 10 else "WARNING"
            return {
                "status": status,
                "score": min(risk_score, 100),
                "findings": findings
            }

def analyze_cloud_security(content):
    scanner = CloudSecurityAI()
    return scanner.scan_content(content)

def analyze_iot_security(device_data):
    scanner = IoTSecurityAI()
    return scanner.analyze_telemetry(device_data)

def analyze_opsec_security(logs):
    scanner = OpSecAI()
    return scanner.analyze_logs(logs)
