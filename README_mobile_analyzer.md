# Mobile App Analyzer

This tool analyzes Android APK files for potential security issues, including high-risk permissions, hardcoded secrets, and indicators of phishing or scams.

## Features

*   **APK Decompilation:** Uses `apktool` to decompile the APK for source code analysis.
*   **Permission Analysis:** Extracts and identifies high-risk permissions from the `AndroidManifest.xml`.
*   **Secret Scanning:** Scans the decompiled code for hardcoded secrets like API keys and private keys.
*   **Scam Detection:** Analyzes text content in the app's files for suspicious URLs, phishing keywords, and other scam indicators.

## Prerequisites

*   Python 3.x
*   `apktool`: Must be installed and available in your system's PATH.
*   `aapt`: Must be installed and available in your system's PATH.

You can typically install these tools on a Debian-based system (like Ubuntu) with:
`sudo apt-get install apktool aapt`

## How to Run

1.  Navigate to the root directory of this repository.
2.  Run the analyzer from your terminal, passing the path to the APK file you want to analyze:

    ```bash
    python mobile_analyzer_main.py /path/to/your/app.apk
    ```

### Options

*   `--keep-files`: Use this flag to prevent the script from deleting the `decompiled_apk` directory after the analysis is complete. This is useful for debugging or manual inspection.

    ```bash
    python mobile_analyzer_main.py /path/to/your/app.apk --keep-files
    ```

## How to Interpret the Output

The tool will print a report to the console with the following sections:

*   **High-Risk Permissions Found:** A list of permissions that could potentially be abused to access sensitive user data or control the device.
*   **Potential Secrets Found:** A list of files that may contain hardcoded sensitive data. Review these files carefully.
*   **Scam Indicators Found:** A list of files containing suspicious URLs, keywords, or other patterns that might indicate phishing or other scams.

## Limitations

*   **Android Only:** This tool currently only supports Android APK files. iOS app analysis is not supported.
*   **Static Analysis Only:** The analysis is purely static (it only examines the code and files). It does not run the app or monitor its behavior at runtime.
*   **Not Foolproof:** This tool uses patterns and heuristics to find potential issues. It is not guaranteed to find all vulnerabilities, and it may produce false positives. Always use your judgment and, if possible, combine this with other security testing methods.

## Disclaimer

This tool is for educational and research purposes only. The user is responsible for any use of this tool. Do not use it to analyze apps for which you do not have permission.
