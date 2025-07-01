# Facebook Security Analyzer CLI

This command-line tool provides utilities to help users analyze Facebook messages for potential phishing attempts and assess Facebook profiles for indicators of fakeness.

## Features

1.  **Phishing Message Analysis:**
    *   Accepts user-provided message text.
    *   Scans for common phishing keywords (e.g., "verify your account," "urgent security alert").
    *   Extracts URLs and checks them against patterns of suspicious URLs (e.g., impersonation of legitimate domains, use of URL shorteners, IP address links).
    *   Provides a "suspicion score" and a summary of findings.

2.  **Fake Profile Analysis (Manual Check):**
    *   Accepts a Facebook profile URL from the user.
    *   **Important:** This tool *does not* scrape Facebook or automatically access profile data, in compliance with Facebook's policies.
    *   It guides the user through a manual checklist of common fake profile indicators (e.g., generic profile picture, recent account age, low activity, poor grammar, suspicious requests).
    *   Includes an interactive helper to guide the user in performing a reverse image search on the profile picture using external services like Google Images or TinEye.
    *   Calculates a "suspicion score" based on the user's answers and provides an assessment of how likely the profile is to be fake.

## Prerequisites

*   Python 3.x

## Installation & Setup

1.  **Clone the repository or download the files.**
    If you have the files (`main.py` and the `facebook_analyzer` directory) in a single project folder, no complex installation is typically needed.

2.  **No external Python libraries are required** for the core functionality as it currently stands (uses only standard libraries like `re` and `webbrowser`). If future enhancements (like direct API calls for URL checking) are added, this section will need updates.

## How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you saved the `main.py` file and the `facebook_analyzer` folder.
3.  Run the application using the Python interpreter:
    ```bash
    python main.py
    ```

4.  The tool will display a menu:

    ```
    --- Facebook Security Analyzer ---
    Choose an option:
    1. Analyze a message for phishing
    2. Analyze a Facebook profile for fakeness (manual check)
    3. Exit
    ------------------------------------
    Enter your choice (1-3):
    ```

## Usage

### 1. Analyze a message for phishing

*   Select option `1`.
*   When prompted, paste the full text of the suspicious message and press Enter.
*   The tool will output:
    *   A phishing likelihood score (higher is more suspicious).
    *   Any suspicious keywords found.
    *   Any suspicious URLs found, along with the reason they were flagged.
    *   An overall summary.

### 2. Analyze a Facebook profile for fakeness (manual check)

*   Select option `2`.
*   When prompted, enter the full Facebook profile URL (e.g., `https://www.facebook.com/some.profile`).
*   The tool will open the profile URL in your default web browser for your manual inspection.
*   You will then be guided through a series of yes/no questions based on your observations of the profile.
    *   This includes an optional guided step to perform a reverse image search on the profile's picture.
*   After you answer all questions, the tool will provide:
    *   A list of fake profile indicators you noted.
    *   An overall "suspicion score."
    *   An assessment category (e.g., Low, Medium, High likelihood of being fake).

## Disclaimer

*   This tool provides heuristic-based analysis and guidance. It is **not foolproof** and should not be considered a definitive judgment on whether a message is phishing or a profile is fake.
*   **Phishing Detection:** The tool uses a predefined list of keywords and URL patterns. Sophisticated phishing attempts may evade these checks. Always exercise extreme caution with suspicious messages, especially those asking for login credentials or personal information. Do not rely solely on this tool.
*   **Fake Profile Detection:** The analysis is based *entirely* on your manual observations and answers. False positives and negatives are possible. Always use your best judgment when interacting with profiles online.
*   **Facebook's Terms of Service:** This tool is designed to operate without violating Facebook's Terms of Service by not scraping or automatically collecting data from its platform. The fake profile analysis relies on user-driven manual checks.
*   **Reporting:** If you encounter a phishing attempt or a malicious fake profile, report it directly to Facebook through their official reporting channels.

## File Structure
```
.
├── main.py                     # Main CLI application script
├── facebook_analyzer/
│   ├── __init__.py             # Makes facebook_analyzer a Python package
│   ├── phishing_detector.py    # Logic for phishing message analysis
│   └── fake_profile_detector.py # Logic for fake profile interactive checklist
└── README.md                   # This documentation file
```

## Future Enhancements (Potential)

*   Integration with external URL checking services/APIs (e.g., Google Safe Browsing) for more robust phishing detection.
*   More sophisticated text analysis for phishing detection (e.g., NLP techniques).
*   Allowing users to customize keyword lists.
*   A graphical user interface (GUI) instead of a CLI.
```
