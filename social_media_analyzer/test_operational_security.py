import unittest
from social_media_analyzer.operational_security import CloudSecurityAI, IoTSecurityAI, OpSecAI

class TestOperationalSecurity(unittest.TestCase):
    def test_cloud_security_scan(self):
        ai = CloudSecurityAI()
        content = "My AWS Key is AKIA1234567890ABCDEF"
        findings = ai.scan_content(content)
        self.assertIn("AWS Access Key ID", findings)
        # Verify redaction: AKIA1234567890ABCDEF -> AKIA...CDEF
        self.assertEqual(findings["AWS Access Key ID"], ["AKIA...CDEF"])

    def test_iot_security_analyze(self):
        ai = IoTSecurityAI()
        # Test warning case
        device_data = {'voltage': 2.5, 'temperature': 80, 'rssi': -95}
        result = ai.analyze_telemetry(device_data)
        self.assertEqual(result["status"], "WARNING")
        self.assertTrue(len(result["findings"]) > 0)

        # Test secure case
        secure_data = {'voltage': 3.3, 'temperature': 25, 'rssi': -50}
        result = ai.analyze_telemetry(secure_data)
        self.assertEqual(result["status"], "SECURE")

    def test_opsec_analyze(self):
        ai = OpSecAI()
        logs = ["unauthorized access attempt", "nmap scan detected"]
        result = ai.analyze_logs(logs)
        self.assertEqual(result["status"], "WARNING")
        self.assertTrue(any("Unauthorized Login Attempt" in f for f in result["findings"]))
        self.assertTrue(any("Internal Scan Activity" in f for f in result["findings"]))

if __name__ == "__main__":
    unittest.main()
