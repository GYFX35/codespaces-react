from . import fake_profile_detector
from . import scam_detector

def main():
    """Main function to run the social media analyzer."""
    print("--- Social Media Analyzer ---")
    print("This tool helps you analyze social media profiles and messages for potential scams.")

    platforms = ["facebook", "instagram", "whatsapp", "tiktok", "tinder", "snapchat", "wechat", "telegram", "twitter", "pinterest", "linkedin", "line", "discord", "teams", "zoom", "amazon", "alibaba", "youtube", "skype", "vk", "reddit", "email"]

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
        print("2. Analyze a message for phishing or scam attempts.")

        try:
            analysis_choice = int(input("Enter your choice (1-2): "))
            if analysis_choice == 1:
                profile_url = input(f"Enter the {platform.capitalize()} profile URL to analyze: ").strip()
                if profile_url:
                    fake_profile_detector.analyze_profile_based_on_user_input(profile_url, platform)
                else:
                    print("No profile URL entered.")
                break
            elif analysis_choice == 2:
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

if __name__ == '__main__':
    main()
