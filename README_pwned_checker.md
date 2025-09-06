# Account Pwned Checker CLI

This tool checks if an email account has been compromised in a known data breach by using the 'Have I Been Pwned?' (HIBP) API.

## Features

*   Checks a single email address against the HIBP database.
*   Lists the details of each breach found for the account.
*   Provides clear output for both compromised and non-compromised accounts.

## Prerequisites

*   Python 3.6+
*   `requests` library
*   A 'Have I Been Pwned?' API Key

## Installation & Setup

1.  **Get an API Key:**
    *   You must have an API key to use the HIBP API. You can get one for free from the [HIBP API Key Page](https://haveibeenpwned.com/API/Key).
    *   Once you have your key, open the `pwned_checker/checker.py` file.
    *   Replace the placeholder `"YOUR_API_KEY_HERE"` with your actual API key:
        ```python
        # In pwned_checker/checker.py
        headers = {
            "hibp-api-key": "YOUR_API_KEY_HERE"  # <-- PASTE YOUR KEY HERE
        }
        ```

2.  **Navigate to the project directory.**
    Make sure you have the `pwned_main.py` script and the `pwned_checker` directory.

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv_pwned
    source venv_pwned/bin/activate  # On Windows: venv_pwned\Scripts\activate
    ```

4.  **Install dependencies:**
    Navigate to the `pwned_checker` directory and run:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  Open your terminal or command prompt.
2.  Make sure your virtual environment is activated.
3.  Navigate to the root directory containing `pwned_main.py`.
4.  Run the application with the email you want to check:
    ```bash
    python pwned_main.py "some.email@example.com"
    ```

### Example Usage

**To check an email:**
```bash
python pwned_main.py "test@example.com"
```

**Example Output (If Breaches are Found):**
```
Checking account: test@example.com

--- Account Found in Breaches! ---
The account 'test@example.com' was found in the following breaches:

  - Breach: Adobe
    Domain: adobe.com
    Date: 2013-10-04
    Description: In October 2013, 153 million Adobe accounts were breached...

  - Breach: MyFitnessPal
    Domain: myfitnesspal.com
    Date: 2018-02-25
    Description: In February 2018, the health and fitness service MyFitnessPal suffered a data breach...
```

**Example Output (If No Breaches are Found):**
```
Checking account: a.secure.email@example.com

--- No Breaches Found ---
The account 'a.secure.email@example.com' was not found in any known breaches.
```

## Disclaimer

*   This tool relies on the 'Have I Been Pwned?' service. Its accuracy is dependent on the data maintained by HIBP.
*   A "not found" result does not guarantee an account is secure, only that it has not appeared in a breach known to HIBP.
*   Handle your API key securely. Do not commit it to public repositories. The method of placing it directly in the source code is for simplicity; for more secure applications, use environment variables or a secrets management system.

## File Structure
```
.
├── pwned_main.py                 # Main CLI application script
├── pwned_checker/
│   ├── __init__.py             # Makes pwned_checker a Python package
│   ├── checker.py              # Logic for interacting with the HIBP API
│   └── requirements.txt        # Python dependencies
└── README_pwned_checker.md       # This documentation file
```
