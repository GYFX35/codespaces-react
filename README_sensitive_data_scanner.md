# Sensitive Data Scanner CLI

This tool recursively scans a specified directory to find sensitive data patterns within files, such as API keys, private keys, and credit card numbers.

## Features

*   Scans all files within a directory and its subdirectories.
*   Uses a predefined set of regular expressions to identify potential sensitive information.
*   Reports the file path and the type of sensitive data found.

## Patterns Detected

The scanner looks for the following patterns:
*   AWS Access Key ID
*   AWS Secret Access Key (Note: this pattern is broad and may cause false positives)
*   Google API Key
*   Generic API Key patterns
*   RSA and SSH Private Keys (looks for the header)
*   Credit Card Numbers (Visa, Mastercard, American Express, Discover)
*   U.S. Social Security Numbers

## Prerequisites

*   Python 3.6+
*   No external libraries are required.

## How to Run

1.  **Navigate to the project directory.**
    Ensure you have the `scanner_main.py` script and the `sensitive_data_scanner` directory.

2.  **Run the application from your terminal.**
    Provide the path to the directory you want to scan as a command-line argument.

    ```bash
    python scanner_main.py /path/to/your/directory
    ```

### Example Usage

**To scan a directory named `my_project`:**
```bash
python scanner_main.py ./my_project
```

**Example Output:**
```
Scanning directory: ./my_project

--- Sensitive Data Found! ---

[+] File: ./my_project/config/prod.env
  - Found 1 instance(s) of 'AWS Access Key ID'
    Example: AKIAIOSFODNN7EXAMPLE
  - Found 1 instance(s) of 'AWS Secret Access Key'
    Example: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[+] File: ./my_project/src/dev/test_keys.txt
  - Found 1 instance(s) of 'RSA Private Key'
    Example: -----BEGIN RSA PRIVATE KEY-----
```

**If no data is found:**
```
Scanning directory: ./clean_project

--- No Sensitive Data Found ---
Scan complete. No files with matching sensitive data patterns were found.
```

## Disclaimer

*   **This tool is not foolproof.** It uses regular expressions to find patterns, which can result in both **false positives** (flagging data that is not sensitive) and **false negatives** (missing sensitive data that doesn't match a pattern).
*   The results should be manually reviewed to confirm if the flagged data is truly sensitive.
*   This tool is intended for educational and basic scanning purposes. For enterprise-grade data loss prevention (DLP), consider using more advanced, dedicated security solutions.
*   The tool reads all files as text. It may not be effective on binary files and will ignore files it cannot read due to permissions or encoding issues.

## File Structure
```
.
├── scanner_main.py                 # Main CLI application script
├── sensitive_data_scanner/
│   ├── __init__.py               # Makes sensitive_data_scanner a Python package
│   └── scanner.py                # Core logic for file scanning and regex matching
└── README_sensitive_data_scanner.md # This documentation file
```
