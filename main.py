import sys
from facebook_analyzer import phishing_detector
from facebook_analyzer import fake_profile_detector


def display_menu():
    """Displays the main menu to the user."""
    print("\n--- Facebook Security Analyzer ---")
    print("Choose an option:")
    print("1. Analyze a message for phishing")
    print("2. Analyze a Facebook profile for fakeness (manual check)")
    print("3. Exit")
    print("------------------------------------")


def main():
    """Main function to run the CLI application."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print("\n--- Phishing Message Analyzer ---")
            message_text = input("Paste the full message text you want to analyze:\n")
            if not message_text:
                print("No message text provided. Returning to menu.")
                continue

            print("\nAnalyzing message...")
            analysis_result = phishing_detector.analyze_message_for_phishing(
                message_text
            )

            print("\n--- Phishing Analysis Results ---")
            print(f"Score: {analysis_result['score']} (Higher is more suspicious)")
            if analysis_result["keywords_found"]:
                print(
                    f"Suspicious Keywords Found: {', '.join(analysis_result['keywords_found'])}"
                )
            if analysis_result["suspicious_urls_found"]:
                print("Suspicious URLs Found:")
                for sus_url in analysis_result["suspicious_urls_found"]:
                    print(f"  - URL: {sus_url['url']}")
                    print(f"    Reason: {sus_url['reason']}")
            if (
                not analysis_result["keywords_found"]
                and not analysis_result["suspicious_urls_found"]
            ):
                print(
                    "No specific phishing keywords or suspicious URLs detected by basic checks."
                )

            print(f"\nOverall Summary: {analysis_result['summary']}")
            print("---------------------------------")

        elif choice == "2":
            print("\n--- Fake Profile Analyzer (Manual Check) ---")
            profile_url = input(
                "Enter the full Facebook profile URL you want to analyze (e.g., https://www.facebook.com/username):\n"
            ).strip()
            if not profile_url.startswith("http://") and not profile_url.startswith(
                "https://"
            ):
                print(
                    "Invalid URL format. Please include http:// or https://. Returning to menu."
                )
                continue
            if not profile_url:
                print("No profile URL provided. Returning to menu.")
                continue

            fake_profile_detector.analyze_profile_based_on_user_input(profile_url)
            print("------------------------------------------")

        elif choice == "3":
            print("Exiting Facebook Security Analyzer. Stay safe!")
            sys.exit()

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()
