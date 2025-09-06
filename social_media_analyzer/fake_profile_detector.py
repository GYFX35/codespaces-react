import webbrowser

# --- Platform-Specific Advice ---
PLATFORM_SPECIFIC_ADVICE = {
    "instagram": [
        "Check for a high follower count but very low engagement (likes/comments) on posts.",
        "Look for accounts that exclusively post promotional content or ads.",
        "Be wary of accounts that have a large number of followers but follow very few people."
    ],
    "tinder": [
        "Be cautious of profiles that seem 'too perfect' with professional-level photos.",
        "Watch out for profiles that immediately try to move the conversation to another platform (e.g., WhatsApp).",
        "Be wary of profiles with very sparse information or only a single photo."
    ],
    "tiktok": [
        "Check if the account has a large number of followers but the videos have very few views or likes.",
        "Look for accounts that spam comments with links or promotional messages.",
        "Be suspicious of accounts that use stolen or unoriginal content."
    ],
    "snapchat": [
        "Be careful with accounts that you don't know personally, especially if they ask for personal information.",
        "Scammers may use Snapchat to send disappearing messages with malicious links."
    ],
    "whatsapp": [
        "Be wary of messages from unknown numbers, especially if they contain links or ask for money.",
        "Check the profile picture and status of unknown contacts for anything suspicious.",
    ],
    "wechat": [
        "Be cautious of accounts that you don't know, especially if they ask for money or personal information.",
        "Scammers may use fake accounts to impersonate friends or family."
    ],
    "facebook": [
        "Check the 'About' section for inconsistencies or lack of information.",
        "Look at the age of the account and the history of posts.",
        "Be suspicious of friend requests from people you don't know, especially if you have no mutual friends."
    ]
}


# --- Generic Fake Profile Indicators ---
FAKE_PROFILE_INDICATORS = [
    {
        "id": "profile_picture_generic",
        "prompt": "Is the profile picture generic, a stock photo, an illustration, or of a celebrity?",
        "weight_if_yes": 2,
        "details_if_yes": "Generic or stolen profile pictures are common for fake accounts."
    },
    {
        "id": "profile_picture_reverse_search",
        "prompt": "Have you tried a reverse image search on the profile picture? Did it show the image is widely used or belongs to someone else?",
        "weight_if_yes": 3,
        "details_if_yes": "Reverse image search can quickly identify stolen or common stock photos."
    },
    {
        "id": "account_age_very_new",
        "prompt": "Does the profile seem very new with little history (e.g., recent join date, few old posts)?",
        "weight_if_yes": 1,
        "details_if_yes": "Many fake accounts are newly created."
    },
    {
        "id": "few_posts_or_activity",
        "prompt": "Does the profile have very few posts, photos, or other activity over its lifespan?",
        "weight_if_yes": 1,
        "details_if_yes": "Lack of genuine activity can be a sign."
    },
    {
        "id": "generic_or_copied_posts",
        "prompt": "Are the posts (if any) generic, nonsensical, repetitive, or copied from other sources?",
        "weight_if_yes": 2,
        "details_if_yes": "Content that isn't original or personal is suspicious."
    },
    {
        "id": "engagement_mismatch",
        "prompt": "Is there a mismatch between the number of friends/followers and the engagement (likes/comments) on posts?",
        "weight_if_yes": 1,
        "details_if_yes": "Unusual ratios can be an indicator (e.g., many followers, but almost no likes)."
    },
    {
        "id": "poor_grammar_spelling",
        "prompt": "Is the language in the profile's bio or posts consistently poor in grammar or spelling?",
        "weight_if_yes": 1,
        "details_if_yes": "Hastily created fake profiles often have noticeable language issues."
    },
    {
        "id": "about_section_sparse_or_inconsistent",
        "prompt": "Is the 'About' or 'Bio' section sparse, inconsistent, or overly glamorous/fake?",
        "weight_if_yes": 2,
        "details_if_yes": "Incomplete or suspicious 'About' information is a red flag."
    },
    {
        "id": "pressure_or_strange_requests",
        "prompt": "Has this profile sent messages pressuring you for information, money, or to click suspicious links?",
        "weight_if_yes": 3,
        "details_if_yes": "This is a strong indicator of a malicious account."
    }
]

def guide_reverse_image_search(image_url=None):
    """Opens browser tabs to guide the user through reverse image search."""
    print("\n--- Guiding Reverse Image Search ---")
    print("You can use services like Google Images or TinEye to check if a profile picture is used elsewhere.")
    if image_url:
        google_url = f"https://images.google.com/searchbyimage?image_url={image_url}"
        tineye_url = f"https://tineye.com/search?url={image_url}"
        print(f"Attempting to open Google Images: {google_url}")
        webbrowser.open(google_url)
        print(f"Attempting to open TinEye: {tineye_url}")
        webbrowser.open(tineye_url)
    else:
        print("If you have the image saved, you can upload it to these sites:")
        print("Google Images: https://images.google.com/ (click the camera icon)")
        webbrowser.open("https://images.google.com/")
        print("TinEye: https://tineye.com/")
        webbrowser.open("https://tineye.com/")
    print("Look for whether the image is a common stock photo, belongs to a different person, or appears on many unrelated profiles.")
    input("Press Enter to continue after performing your search...")

def print_platform_specific_advice(platform):
    """Prints platform-specific advice to the user."""
    if platform in PLATFORM_SPECIFIC_ADVICE:
        print(f"\n--- Platform-Specific Advice for {platform.capitalize()} ---")
        for advice in PLATFORM_SPECIFIC_ADVICE[platform]:
            print(f"- {advice}")

def analyze_profile_based_on_user_input(profile_url, platform):
    """
    Guides the user through a checklist to assess if a social media profile is fake.
    """
    print(f"\n--- Analyzing {platform.capitalize()} Profile (Manual Check) ---")
    print(f"Please open the profile in your browser or app: {profile_url}")
    print("You will be asked a series of questions based on your observations.")
    webbrowser.open(profile_url)

    print_platform_specific_advice(platform)

    user_responses = {}
    total_score = 0
    positive_indicators = []

    perform_ris = input("\nDo you want guidance to perform a reverse image search on the profile picture? (yes/no): ").strip().lower()
    if perform_ris == 'yes':
        img_url_known = input("Do you have a direct URL for the profile image? (yes/no): ").strip().lower()
        if img_url_known == 'yes':
            actual_img_url = input("Please paste the direct image URL: ").strip()
            guide_reverse_image_search(actual_img_url)
        else:
            guide_reverse_image_search()

    for indicator in FAKE_PROFILE_INDICATORS:
        while True:
            answer = input(f"{indicator['prompt']} (yes/no): ").strip().lower()
            if answer in ['yes', 'no']:
                user_responses[indicator['id']] = answer
                if answer == 'yes':
                    total_score += indicator['weight_if_yes']
                    positive_indicators.append(f"- {indicator['prompt']} ({indicator['details_if_yes']})")
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")

    print("\n--- Fake Profile Analysis Results ---")
    print(f"Profile URL: {profile_url}")

    if not positive_indicators:
        print("Based on your answers, no common fake profile indicators were strongly identified.")
    else:
        print("The following indicators suggestive of a fake profile were noted:")
        for pi in positive_indicators:
            print(pi)

        print(f"\nOverall 'suspicion score': {total_score}")
        if total_score <= 3:
            print("Assessment: Low likelihood of being fake.")
        elif total_score <= 6:
            print("Assessment: Medium likelihood. Exercise caution.")
        else:
            print("Assessment: High likelihood. High caution advised.")

    print("\nDisclaimer: This analysis is based SOLELY on your manual observations.")
    print("Always use your best judgment and consider reporting suspicious profiles to the platform.")

    return {
        "profile_url": profile_url,
        "platform": platform,
        "score": total_score,
        "positive_indicators": positive_indicators,
    }

if __name__ == '__main__':
    print("Fake Profile Detector - Manual Checklist Tool")
    test_platform = input("Enter the social media platform to simulate analyzing (e.g., instagram): ").strip().lower()
    test_profile_url = input(f"Enter a {test_platform.capitalize()} profile URL to simulate analyzing: ").strip()
    if test_profile_url and test_platform:
        analyze_profile_based_on_user_input(test_profile_url, test_platform)
