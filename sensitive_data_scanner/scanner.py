import re
import os

# Pre-compiled regex patterns for performance
SENSITIVE_DATA_PATTERNS = {
    "AWS Access Key ID": re.compile(r"AKIA[0-9A-Z]{16}"),
    "AWS Secret Access Key": re.compile(r"(?i)[a-z0-9\/+]{40}"), # This is a broad pattern, may have false positives
    "Google API Key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "Generic API Key": re.compile(r"[aA][pP][iI]_?[kK][eE][yY].*['|\"]([a-zA-Z0-9-_.]{16,})['|\"]"),
    "RSA Private Key": re.compile(r"-----BEGIN RSA PRIVATE KEY-----"),
    "SSH Private Key": re.compile(r"-----BEGIN OPENSSH PRIVATE KEY-----"),
    "Credit Card (Visa)": re.compile(r"4[0-9]{12}(?:[0-9]{3})?"),
    "Credit Card (Mastercard)": re.compile(r"5[1-5][0-9]{14}"),
    "Credit Card (Amex)": re.compile(r"3[47][0-9]{13}"),
    "Credit Card (Discover)": re.compile(r"6(?:011|5[0-9]{2})[0-9]{12}"),
    "Social Security Number": re.compile(r"\d{3}-\d{2}-\d{4}")
}

def scan_file(filepath):
    """
    Scans a single file for sensitive data patterns.

    Args:
        filepath (str): The path to the file to scan.

    Returns:
        A dictionary of findings, with the key being the pattern name
        and the value being a list of found strings.
    """
    findings = {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern_name, regex in SENSITIVE_DATA_PATTERNS.items():
                matches = regex.findall(content)
                if matches:
                    if pattern_name not in findings:
                        findings[pattern_name] = []
                    findings[pattern_name].extend(matches)
    except Exception as e:
        # Could be a binary file or a permissions error
        pass  # Silently ignore files that can't be read
    return findings

def scan_directory(directory):
    """
    Recursively scans a directory for files containing sensitive data.

    Args:
        directory (str): The path to the directory to scan.

    Returns:
        A dictionary where keys are file paths and values are dictionaries
        of findings for that file.
    """
    all_findings = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_findings = scan_file(filepath)
            if file_findings:
                all_findings[filepath] = file_findings
    return all_findings
