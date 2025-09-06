import argparse
import os
import shutil
import sys
from mobile_analyzer import analyzer

def main():
    parser = argparse.ArgumentParser(description="Analyze an Android APK for security vulnerabilities.")
    parser.add_argument("apk_path", help="The path to the APK file to analyze.")
    parser.add_argument("--keep-files", action="store_true", help="Keep the decompiled files after analysis.")
    args = parser.parse_args()

    apk_path = args.apk_path
    if not os.path.exists(apk_path):
        print(f"Error: APK file not found at {apk_path}")
        sys.exit(1)

    # Create a directory for the decompiled code
    output_dir = "decompiled_apk"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    print(f"--- Starting analysis for {os.path.basename(apk_path)} ---")

    # 1. Decompile the APK
    if not analyzer.decompile_apk(apk_path, output_dir):
        print("Failed to decompile APK. Aborting analysis.")
        sys.exit(1)

    # 2. Analyze permissions
    print("\n--- Analyzing Permissions ---")
    all_permissions = analyzer.get_permissions(apk_path)
    if all_permissions:
        high_risk_permissions = analyzer.check_high_risk_permissions(all_permissions)
        if high_risk_permissions:
            print("\n[!] High-Risk Permissions Found:")
            for perm in high_risk_permissions:
                print(f"  - {perm}")
        else:
            print("\nNo high-risk permissions found.")
    else:
        print("\nCould not extract permissions.")

    # 3. Scan for sensitive data
    print("\n--- Scanning for Hardcoded Secrets ---")
    sensitive_data = analyzer.scan_for_sensitive_data(output_dir)
    if sensitive_data:
        print("\n[!] Potential Secrets Found:")
        for file, findings in sensitive_data.items():
            print(f"  - In file: {file}")
            for finding_type, matches in findings.items():
                print(f"    - {finding_type}: {len(matches)} found")
    else:
        print("\nNo hardcoded secrets found.")

    # 4. Scan for scam indicators
    print("\n--- Scanning for Phishing and Scam Indicators ---")
    scam_indicators = analyzer.scan_for_scam_indicators(output_dir)
    if scam_indicators:
        print("\n[!] Scam Indicators Found:")
        for file, result in scam_indicators.items():
            print(f"  - In file: {file}")
            for indicator in result["indicators_found"]:
                print(f"    - {indicator}")
    else:
        print("\nNo scam indicators found.")

    # Clean up the decompiled files
    if not args.keep_files:
        print("\nCleaning up temporary files...")
        shutil.rmtree(output_dir)

    print("\n--- Analysis Complete ---")

if __name__ == "__main__":
    main()
