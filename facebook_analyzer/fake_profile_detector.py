# facebook_analyzer/fake_profile_detector.py

import webbrowser

# Common indicators of fake profiles.
# Each indicator can have a 'weight' for a simple scoring system.
# 'prompt' is what the user will be asked.
# 'type' can be 'yes_no', 'numeric', 'text_analysis' (future), etc.
# 'details_if_yes' can provide more context or ask for more info if the user answers 'yes'.
FAKE_PROFILE_INDICATORS = [
    {
        "id": "profile_picture_generic",
        "prompt": "Is the profile picture generic, a stock photo, an illustration, or of a celebrity (i.e., not a clear photo of a unique, real person)?",
        "type": "yes_no",
        "weight_if_yes": 2,
        "details_if_yes": "Generic or stolen profile pictures are common for fake accounts."
    },
    {
        "id": "profile_picture_reverse_search",
        "prompt": "Have you tried a reverse image search (e.g., Google Images, TinEye) on the profile picture? If so, did it show the image is widely used, a stock photo, or belongs to someone else?",
        "type": "yes_no",
        "weight_if_yes": 3,
        "details_if_yes": "Reverse image search can often quickly identify stolen or common stock photos."
    },
    {
        "id": "account_age_very_new",
        "prompt": "Does the profile seem very new with little history (e.g., join date is recent, few old posts)? (Requires manual check on the profile)",
        "type": "yes_no",
        "weight_if_yes": 1,
        "details_if_yes": "While not definitive, many fake accounts are newly created."
    },
    {
        "id": "few_posts_or_activity",
        "prompt": "Does the profile have very few posts, photos, or other activity over its lifespan? (Requires manual check)",
        "type": "yes_no",
        "weight_if_yes": 1,
        "details_if_yes": "Lack of genuine activity can be a sign."
    },
    {
        "id": "generic_or_copied_posts",
        "prompt": "Are the posts (if any) generic, nonsensical, repetitive, or seem copied from other sources? (Requires manual check)",
        "type": "yes_no",
        "weight_if_yes": 2,
        "details_if_yes": "Content that isn't original or personal is suspicious."
    },
    {
        "id": "friend_count_mismatch",
        "prompt": "Does the profile have a very high number of friends but very little engagement (likes/comments) on their posts, or an unusually low number of friends for a long-standing account? (Requires manual check)",
        "type": "yes_no",
        "weight_if_yes": 1,
        "details_if_yes": "Unusual friend counts or activity ratios can be indicators."
    },
    {
        "id": "poor_grammar_spelling",
        "prompt": "Is the language used in the profile's 'About' section or posts consistently poor in grammar or spelling (beyond typical typos)? (Requires manual check)",
        "type": "yes_no",
        "weight_if_yes": 1,
        "details_if_yes": "Often, hastily created fake profiles have noticeable language issues."
    },
    {
        "id": "about_section_sparse_or_inconsistent",
        "prompt": "Is the 'About' section very sparse, missing key information (like education, work), or contains information that seems inconsistent or overly glamorous/fake? (Requires manual check)",
        "type": "yes_no",
        "weight_if_yes": 2,
        "details_if_yes": "Incomplete or suspicious 'About' information is a red flag."
    },
    {
        "id": "mutual_friends_suspicious",
        "prompt": "If you have mutual friends, do those mutual connections seem legitimate or are they also suspicious-looking profiles?",
        "type": "yes_no",
        "weight_if_yes": 1,
        "details_if_yes": "Fake accounts often connect with other fake accounts."
    },
    {
        "id": "pressure_or_strange_requests",
        "prompt": "Has this profile sent you messages that pressure you for information, money, or to click suspicious links shortly after connecting?",
        "type": "yes_no",
        "weight_if_yes": 3,
        "details_if_yes": "This is a strong indicator of a malicious fake account."
    }
]

def guide_reverse_image_search(image_url=None):
    """Opens browser tabs to guide the user through reverse image search."""
    print("\n--- Guiding Reverse Image Search ---")
    print("You can use services like Google Images or TinEye to check if a profile picture is used elsewhere.")
    if image_url:
        print(f"If you have a direct URL for the image: {image_url}")
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


def analyze_profile_based_on_user_input(profile_url):
    """
    Guides the user through a checklist to assess if a Facebook profile is fake.
    Does NOT scrape any data. Relies on user observation.
    """
    print(f"\n--- Analyzing Facebook Profile (Manual Check) ---")
    print(f"Please open the Facebook profile in your browser: {profile_url}")
    print("You will be asked a series of questions based on your observations.")
    print("This tool does NOT access Facebook directly or scrape any data.")
    webbrowser.open(profile_url) # Open for user convenience

    user_responses = {}
    total_score = 0
    positive_indicators = []

    # Ask about reverse image search first
    perform_ris = input("Do you want guidance to perform a reverse image search on the profile picture? (yes/no): ").strip().lower()
    if perform_ris == 'yes':
        img_url_known = input("Do you have a direct URL for the profile image? (yes/no): ").strip().lower()
        if img_url_known == 'yes':
            actual_img_url = input("Please paste the direct image URL: ").strip()
            guide_reverse_image_search(actual_img_url)
        else:
            guide_reverse_image_search()
            print("Now, let's answer the question about the reverse image search based on your findings.")


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
        print("However, always remain cautious.")
    else:
        print("The following indicators suggestive of a fake profile were noted based on your input:")
        for pi in positive_indicators:
            print(pi)

        print(f"\nOverall 'suspicion score': {total_score}")
        if total_score == 0:
             print("Assessment: No strong indicators noted from your input.")
        elif total_score <= 3:
            print("Assessment: Low likelihood of being fake based on your input, but remain cautious.")
        elif total_score <= 6:
            print("Assessment: Medium likelihood. Some indicators suggest this profile could be fake. Exercise caution.")
        elif total_score <= 9:
            print("Assessment: High likelihood. Several indicators suggest this profile may be fake. High caution advised.")
        else:
            print("Assessment: Very high likelihood. Many strong indicators suggest this profile is likely fake. Avoid interaction and consider reporting.")

    print("\nDisclaimer:")
    print("This analysis is based SOLELY on your manual observations and answers to the checklist.")
    print("It is not a definitive judgment. False positives and negatives are possible.")
    print("Always use your best judgment when interacting with profiles online.")
    print("If you suspect a profile is fake and malicious, consider reporting it to Facebook through their official channels.")

    return {
        "profile_url": profile_url,
        "score": total_score,
        "positive_indicators_details": positive_indicators,
        "user_responses": user_responses
    }

if __name__ == '__main__':
    print("Fake Profile Detector - Manual Checklist Tool")
    print("IMPORTANT: This tool does NOT access Facebook or scrape data.")
    print("It guides YOU to manually check a profile and answer questions.")
    print("------------------------------------------------------------")

    # Example of how it would be called:
    # First, ensure the user is aware of the process for reverse image search, as it's a common first step.
    # For the test, we'll simulate this.

    test_profile_url = input("Enter a Facebook profile URL to simulate analyzing (e.g., https://www.facebook.com/some.profile): ").strip()
    if not test_profile_url:
        print("No URL entered, exiting.")
    else:
        # In a real CLI, you might ask about reverse image search separately first, or integrate it.
        # For this direct test, the function itself will ask.
        analysis = analyze_profile_based_on_user_input(test_profile_url)
        # print("\nFull analysis object (for debugging):")
        # import json
        # print(json.dumps(analysis, indent=2))
