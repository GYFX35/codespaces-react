# Text-Based Scam Detection Tool

This Python CLI tool analyzes text content to identify common indicators associated with scams, such as phishing, prize scams, tech support scams, and more. It provides a likelihood score and a list of specific heuristics triggered.

## Features

*   **Heuristic-Based Analysis:** Checks text against predefined lists of keywords and regular expression patterns related to:
    *   Urgency and pressure tactics.
    *   Requests for sensitive information (credentials, financial details).
    *   Too-good-to-be-true offers and prizes.
    *   Generic greetings.
    *   Tech support scam language.
    *   Payment requests and mentions of cryptocurrencies/gift cards.
*   **URL Analysis (String-Based):**
    *   Detects URLs within the text.
    *   Checks for suspicious Top-Level Domains (TLDs).
    *   Looks for suspicious keywords (e.g., "login", "verify") in URL paths or domains (with a basic check to avoid flagging known major domains).
*   **Detection of Potential Identifiers:**
    *   Cryptocurrency addresses (BTC, ETH).
    *   Phone numbers (basic detection).
*   **Scam Likelihood Score:** Calculates a score based on the number and severity (weights) of indicators found.
*   **Configurable Input:** Accepts text via direct command-line argument, from a file, or from standard input (stdin).
*   **Verbose Output:** Option to display detailed analysis of URLs found.
*   **Adjustable Threshold:** Set a score threshold for a "High Risk" warning.

## Prerequisites

*   Python 3.6+
*   No external Python libraries are required for the core functionality (uses only standard libraries like `re`, `argparse`, `urllib.parse`).

## Installation

1.  **Download the Code:**
    *   Ensure you have `scam_main.py` and the `scam_detector` directory (containing `analyzer.py`, `heuristics.py`, `__init__.py`).

2.  **No `pip install` needed for external libraries for the core tool.**

## Usage

The tool is run from the command line using `python3 scam_main.py`. You must provide one input method.

### Command-Line Arguments

*   **Input (Required - choose one):**
    *   `-t TEXT, --text TEXT`: Text content to analyze directly.
    *   `-f FILE, --file FILE`: Path to a plain text file to read content from.
    *   `--stdin`: Read text content from standard input (e.g., via a pipe).
*   **Options:**
    *   `-v, --verbose`: Enable verbose output (shows detailed URL analysis if URLs are found).
    *   `--threshold THRESHOLD`: Score threshold above which a 'High Risk' warning is displayed (default: 5.0).
    *   `-h, --help`: Show help message and exit.

### Examples

1.  **Analyze text directly:**
    ```bash
    python3 scam_main.py --text "Dear Customer, your account is suspended. Please login at http://yourbank.suspicious-site.xyz/update to avoid closure."
    ```

2.  **Analyze text from a file:**
    ```bash
    python3 scam_main.py --file path/to/suspicious_email.txt
    ```

3.  **Analyze text from a file with verbose output and a custom threshold:**
    ```bash
    python3 scam_main.py --file message.txt --verbose --threshold 3.0
    ```

4.  **Analyze text piped from another command (Linux/macOS):**
    ```bash
    cat email_body.txt | python3 scam_main.py --stdin
    ```
    *(On Windows, you might type input then Ctrl+Z, Enter for stdin)*

## Interpreting the Output

*   **Overall Scam Likelihood Score:** A numerical score. Higher scores indicate a higher likelihood of the text being a scam based on the tool's heuristics.
*   **Assessment:** A qualitative assessment (e.g., "Low risk," "Medium risk," "WARNING: High risk!") based on the score and the threshold.
*   **Indicators Found:** A list of specific reasons why the text was flagged (e.g., presence of urgency keywords, suspicious URL TLDs).
*   **Detailed URL Analysis (with `--verbose`):** For each URL found:
    *   The URL string.
    *   Whether it was deemed suspicious.
    *   Specific reasons for suspicion (e.g., "Uses a potentially suspicious TLD," "URL contains suspicious keyword").

## Disclaimer

*   **Heuristic-Based, Not Foolproof:** This tool uses a set of predefined rules, keywords, and patterns. It is **not a definitive judgment** on whether a piece of text is a scam. Scammers constantly evolve their tactics.
*   **False Positives/Negatives:** The tool may incorrectly flag legitimate text as suspicious (false positive) or fail to detect a real scam (false negative).
*   **Context is Key:** The tool does not understand the full context of the communication, the sender, or your relationship with them, all of which are crucial for accurately identifying scams.
*   **Use Your Judgment:** **Always exercise extreme caution and use your best judgment** when dealing with unsolicited communications, requests for personal information, or offers that seem too good to be true.
*   **Do Not Rely Solely on This Tool:** This tool is an aid and should be one of many factors in your decision-making process. If you are unsure about a message, consult trusted sources or individuals.

## File Structure
```
.
├── scam_detector/
│   ├── __init__.py     # Makes 'scam_detector' a Python package
│   ├── analyzer.py     # Core scam analysis logic
│   └── heuristics.py   # Keyword lists, regex patterns, and weights
└── scam_main.py          # CLI entry point
└── README_scam_detector.md # This documentation file
```
```
