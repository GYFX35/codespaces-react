import subprocess
import os
import re
import sys

# HACK: This is not ideal, but the project is structured as a collection of
# top-level scripts and not as a single installable package. This allows us
# to import modules from sibling directories.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sensitive_data_scanner.scanner import scan_directory as scan_for_secrets
from social_media_analyzer.scam_detector import analyze_text_for_scams


# Based on Android documentation and security best practices.
# These permissions grant access to sensitive user data or system control.
HIGH_RISK_PERMISSIONS = [
    "android.permission.READ_CALENDAR",
    "android.permission.WRITE_CALENDAR",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.READ_PHONE_NUMBERS",
    "android.permission.CALL_PHONE",
    "android.permission.ANSWER_PHONE_CALLS",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_SIP",
    "android.permission.PROCESS_OUTGOING_CALLS",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "com.android.voicemail.permission.ADD_VOICEMAIL",
    "android.permission.BODY_SENSORS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_WAP_PUSH",
    "android.permission.RECEIVE_MMS",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.WRITE_SETTINGS",
    "android.permission.REQUEST_INSTALL_PACKAGES",
    "android.permission.ACCESS_BACKGROUND_LOCATION",
]

def decompile_apk(apk_path, output_dir):
    """
    Decompiles an APK file using apktool.

    Args:
        apk_path (str): The path to the APK file.
        output_dir (str): The directory to store the decompiled code.

    Returns:
        bool: True if decompilation was successful, False otherwise.
    """
    if not os.path.exists(apk_path):
        print(f"Error: APK file not found at {apk_path}")
        return False

    print(f"Decompiling {apk_path} to {output_dir}...")
    try:
        # Using -f to force overwrite the output directory if it exists
        command = ["apktool", "d", "-f", apk_path, "-o", output_dir]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Decompilation successful.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error during decompilation:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'apktool' not found. Make sure it is installed and in your PATH.")
        return False

def get_permissions(apk_path):
    """
    Extracts permissions from an APK's AndroidManifest.xml using aapt.

    Args:
        apk_path (str): The path to the APK file.

    Returns:
        list: A list of permissions found in the APK.
    """
    if not os.path.exists(apk_path):
        print(f"Error: APK file not found at {apk_path}")
        return []

    print(f"Extracting permissions from {apk_path}...")
    try:
        command = ["aapt", "dump", "permissions", apk_path]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Regex to find package permissions
        permissions = re.findall(r"uses-permission: name='([^']*)'", result.stdout)
        print(f"Found {len(permissions)} permissions.")
        return permissions
    except subprocess.CalledProcessError as e:
        print("Error extracting permissions:")
        print(e.stderr)
        return []
    except FileNotFoundError:
        print("Error: 'aapt' not found. Make sure it is installed and in your PATH.")
        return []

def check_high_risk_permissions(permissions):
    """
    Checks a list of permissions against the high-risk permissions list.

    Args:
        permissions (list): The list of permissions from an APK.

    Returns:
        list: A list of high-risk permissions found in the APK.
    """
    found_high_risk = []
    for perm in permissions:
        if perm in HIGH_RISK_PERMISSIONS:
            found_high_risk.append(perm)

    print(f"Found {len(found_high_risk)} high-risk permissions.")
    return found_high_risk


def scan_for_sensitive_data(decompiled_dir):
    """
    Scans a directory for sensitive data using the sensitive_data_scanner module.

    Args:
        decompiled_dir (str): The path to the directory of decompiled code.

    Returns:
        dict: A dictionary of findings.
    """
    print("\nScanning for sensitive data...")
    findings = scan_for_secrets(decompiled_dir)
    if findings:
        print(f"Found sensitive data in {len(findings)} files.")
    else:
        print("No sensitive data found.")
    return findings

def scan_for_scam_indicators(decompiled_dir):
    """
    Scans files in a directory for scam indicators using the scam_detector module.

    Args:
        decompiled_dir (str): The path to the directory of decompiled code.

    Returns:
        dict: A dictionary of findings, where keys are file paths.
    """
    print("\nScanning for scam indicators (phishing, suspicious URLs)...")
    all_findings = {}

    # Extensions of text-like files to scan.
    # Smali, xml, and yml are common in decompiled APKs.
    scan_extensions = {'.smali', '.xml', '.yml', '.yaml', '.json', '.html', '.js', '.txt'}

    for root, _, files in os.walk(decompiled_dir):
        for filename in files:
            # Check if the file has one of the scannable extensions
            if not any(filename.endswith(ext) for ext in scan_extensions):
                continue

            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Skip very large files to avoid performance issues
                    if len(content) > 1000000: # 1MB limit
                        continue

                    analysis_result = analyze_text_for_scams(content)
                    if analysis_result.get("indicators_found"):
                        all_findings[filepath] = analysis_result
            except Exception:
                # Ignore files that can't be read for any reason
                continue

    if all_findings:
        print(f"Found scam indicators in {len(all_findings)} files.")
    else:
        print("No scam indicators found.")

    return all_findings
