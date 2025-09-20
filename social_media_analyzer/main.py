from . import fake_profile_detector
from . import scam_detector

def analyze_website_url():
    """Analyzes a website URL for potential scams."""
    url_to_check = input("Please enter the full URL you want to analyze: ").strip()
    if not url_to_check:
        print("No URL entered.")
        return

    # Ensure the URL has a scheme
    if not url_to_check.startswith(('http://', 'https://')):
        url_to_check = 'http://' + url_to_check

    print("\n--- Analyzing URL ---")
    is_susp, reason = scam_detector.is_url_suspicious(url_to_check, platform="general_web")
    if is_susp:
        print(f"\n[!] The URL '{url_to_check}' is flagged as IMMEDIATELY SUSPICIOUS.")
        print(f"Reason: {reason}")
        # We can stop here as the URL itself is a major red flag
        return
    else:
        print(f"\n[+] The URL '{url_to_check}' does not match common suspicious patterns.")
        print("Now analyzing the website's content...")

    # Analyze the content of the website
    content_result = scam_detector.analyze_url_content(url_to_check)

    print("\n--- Website Content Analysis Results ---")
    if "error" in content_result:
        print(f"Could not analyze website content: {content_result['error']}")
    elif not content_result.get("indicators_found"):
        print("No specific scam indicators were found in the website content.")
    else:
        print(f"Score: {content_result['score']} (Higher is more suspicious)")
        print("Indicators Found:")
        for indicator in content_result['indicators_found']:
            print(f"- {indicator}")

def analyze_social_media():
    """Handles the analysis of social media platforms."""
    platforms = sorted([
        "facebook", "instagram", "whatsapp", "tiktok", "tinder", "snapchat",
        "wechat", "telegram", "twitter", "pinterest", "linkedin", "line",
        "discord", "teams", "zoom", "amazon", "alibaba", "youtube", "skype",
        "vk", "reddit", "email", "viber", "signal", "badoo", "binance",
        "sharechat", "messenger", "qzone", "qq", "vimeo", "musical.ly", "kuaishou", "douyin"
    ])

    while True:
        print("\nSelect the social media platform you want to analyze:")
        for i, p in enumerate(platforms, 1):
            print(f"{i}. {p.capitalize()}")

        try:
            choice = int(input(f"Enter your choice (1-{len(platforms)}): "))
            if 1 <= choice <= len(platforms):
                platform = platforms[choice - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        print(f"\nWhat do you want to do for {platform.capitalize()}?")
        print("1. Analyze a profile for signs of being fake.")
        print("2. Analyze a profile for identity usurpation.")
        print("3. Analyze a message for phishing or scam attempts.")

        try:
            analysis_choice = int(input("Enter your choice (1-3): "))
            if analysis_choice == 1:
                profile_url = input(f"Enter the {platform.capitalize()} profile URL to analyze: ").strip()
                if profile_url:
                    fake_profile_detector.analyze_profile_based_on_user_input(profile_url, platform)
                else:
                    print("No profile URL entered.")
                break
            elif analysis_choice == 2:
                profile_url = input(f"Enter the {platform.capitalize()} profile URL to analyze for impersonation: ").strip()
                if profile_url:
                    fake_profile_detector.analyze_identity_usurpation(profile_url, platform)
                else:
                    print("No profile URL entered.")
                break
            elif analysis_choice == 3:
                message = input("Paste the message you want to analyze: ").strip()
                if message:
                    result = scam_detector.analyze_text_for_scams(message, platform)
                    print("\n--- Scam Analysis Results ---")
                    print(f"Score: {result['score']} (Higher is more suspicious)")
                    print("Indicators Found:")
                    if result['indicators_found']:
                        for indicator in result['indicators_found']:
                            print(f"- {indicator}")
                    else:
                        print("No specific scam indicators were found.")
                else:
                    print("No message entered.")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main function to run the security analyzer."""
    print("--- Universal Security Analyzer ---")
    print("This tool helps you analyze social media, messages, and websites for potential scams.")

    while True:
        print("\n--- Main Menu ---")
        print("1. Analyze a Social Media Platform")
        print("2. Analyze a Website URL")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice (1-3): "))
            if choice == 1:
                analyze_social_media()
            elif choice == 2:
                analyze_website_url()
            elif choice == 3:
                print("Exiting. Stay safe!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    main()
