import argparse
import sys
from scam_detector.analyzer import analyze_text_for_scams


def main():
    parser = argparse.ArgumentParser(
        description="Text-based Scam Detection Tool. Analyzes input text for common scam indicators.",
        epilog='Example: python scam_main.py --text "Dear Customer, click http://suspicious.link/login to verify your account now!"',
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", help="Text content to analyze for scams.")
    group.add_argument(
        "-f", "--file", help="Path to a plain text file to read content from."
    )
    group.add_argument(
        "--stdin",
        action="store_true",
        help="Read text content from standard input (e.g., via pipe).",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (shows detailed URL analysis if URLs are found).",
    )

    # Add a threshold argument for a simple alert
    parser.add_argument(
        "--threshold",
        type=float,
        default=5.0,  # Default threshold, can be adjusted
        help="Score threshold above which a 'High Risk' warning is displayed (default: 5.0).",
    )

    args = parser.parse_args()

    input_text = ""
    if args.text:
        input_text = args.text
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {args.file}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            sys.exit(1)
    elif args.stdin:
        print(
            "Reading from stdin. Press Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows) to end input."
        )
        input_text = sys.stdin.read()

    if not input_text.strip():
        print("Error: No input text provided to analyze.")
        sys.exit(1)

    print("\nAnalyzing text...")
    results = analyze_text_for_scams(input_text)

    print("\n--- Scam Analysis Results ---")
    print(f"Overall Scam Likelihood Score: {results['score']}")

    if results["score"] == 0.0 and not results["indicators_found"]:
        print("No specific scam indicators found in the text.")
    elif results["score"] < args.threshold / 2:  # Example: low risk
        print("Assessment: Low risk of being a scam based on heuristics.")
    elif results["score"] < args.threshold:  # Example: medium risk
        print("Assessment: Medium risk. Some indicators suggest caution.")
    else:  # High risk
        print(f"WARNING: High risk! Score exceeds threshold of {args.threshold}.")
        print("This content has multiple indicators commonly found in scams.")

    if results["indicators_found"]:
        print("\nIndicators Found:")
        for indicator in results["indicators_found"]:
            print(f"  - {indicator}")

    if args.verbose and results["urls_analyzed"]:
        print("\nDetailed URL Analysis:")
        for url_info in results["urls_analyzed"]:
            print(f"  - URL: {url_info['url']}")
            print(f"    Suspicious: {url_info['is_suspicious']}")
            if url_info["reasons"]:
                print(f"    Reasons: {'; '.join(url_info['reasons'])}")
            else:
                print(f"    Reasons: None")
    elif results["urls_analyzed"] and not args.verbose:
        print("\n(Run with --verbose to see detailed URL analysis if URLs were found)")

    print(
        "\nDisclaimer: This tool uses heuristic-based detection and is not foolproof."
    )
    print(
        "Always exercise caution and use your best judgment. Do not rely solely on this tool for security decisions."
    )


if __name__ == "__main__":
    main()
