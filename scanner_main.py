import argparse
import os
from sensitive_data_scanner import scanner

def main():
    parser = argparse.ArgumentParser(description="Scan a directory for files containing sensitive data like API keys, private keys, and credit card numbers.")
    parser.add_argument("directory", help="The directory to scan recursively.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found at '{args.directory}'")
        return

    print(f"Scanning directory: {args.directory}\n")
    all_findings = scanner.scan_directory(args.directory)

    if not all_findings:
        print("--- No Sensitive Data Found ---")
        print("Scan complete. No files with matching sensitive data patterns were found.")
        return

    print("--- Sensitive Data Found! ---")
    for filepath, findings in all_findings.items():
        print(f"\n[+] File: {filepath}")
        for pattern_name, matches in findings.items():
            print(f"  - Found {len(matches)} instance(s) of '{pattern_name}'")
            # To avoid printing too much data, maybe just show the first match or a count
            # For now, let's print the first match to give an idea of what was found
            print(f"    Example: {matches[0]}")

if __name__ == "__main__":
    main()
