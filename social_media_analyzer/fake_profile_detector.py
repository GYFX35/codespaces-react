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
    ],
    "telegram": [
        "Be wary of unsolicited messages from users or bots, especially those promoting investments or crypto.",
        "Check the username for slight misspellings of official channels or known contacts.",
        "Never share personal codes or login information with anyone on Telegram."
    ],
    "twitter": [
        "Look for newly created accounts with very few tweets but high follower counts (often bots).",
        "Be suspicious of accounts that primarily tweet suspicious links or participate in crypto scams.",
        "Check the bio and tweets for poor grammar or generic content."
    ],
    "pinterest": [
        "Be cautious of pins that lead to suspicious websites unrelated to the pin's content.",
        "Look for profiles with very few boards or pins but a high number of followers.",
        "Be wary of accounts that leave spammy comments with links."
    ],
    "linkedin": [
        "Be suspicious of profiles with generic job titles and descriptions.",
        "Check for inconsistencies in work history or education.",
        "Be wary of connection requests from individuals with no mutual connections or a sparse profile."
    ],
    "line": [
        "Be cautious of messages from unknown accounts, especially those with links or QR codes.",
        "Scammers may impersonate official accounts; check for the green shield icon for verified accounts.",
    ],
    "discord": [
        "Be wary of direct messages from users you don't share a server with.",
        "Never click on suspicious links or download files from unknown users.",
        "Be cautious of friend requests from users with no mutual friends or servers in common."
    ],
    "teams": [
        "Be wary of messages from external accounts you don't recognize.",
        "Do not share sensitive company information with unverified contacts.",
        "Report any suspicious activity to your IT department."
    ],
    "zoom": [
        "Be cautious of unexpected meeting invitations or links.",
        "Ensure the meeting host is someone you know and trust.",
        "Do not share personal information in public chat during a meeting."
    ],
    "amazon": [
        "Be wary of seller profiles with little to no feedback or very new accounts.",
        "Check product reviews for signs of being fake or paid.",
        "Be suspicious of sellers who ask you to complete a transaction outside of Amazon's official platform."
    ],
    "alibaba": [
        "Verify the seller's credentials, such as their 'Gold Supplier' status and business license.",
        "Be cautious of prices that are significantly lower than the market average.",
        "Use Alibaba's Trade Assurance for secure payments and to protect against fraud."
    ],
    "youtube": [
        "Be wary of comments with suspicious links, especially on popular videos.",
        "Check the 'About' page of a channel for contact information and creation date.",
        "Look for channels with high subscriber counts but low video views or engagement."
    ],
    "skype": [
        "Be cautious of contact requests from people you don't know.",
        "Never send money or share personal information with unknown contacts.",
        "Scammers may impersonate Microsoft or Skype support to gain access to your account."
    ],
    "vk": [
        "Be suspicious of profiles with very little personal information or photos.",
        "Check for a large number of 'friends' but low engagement on posts.",
        "Be wary of messages with links to third-party sites, especially for games or prizes."
    ],
    "reddit": [
        "Check a user's post and comment history for signs of spam or bot-like activity.",
        "Be cautious of unsolicited private messages with investment opportunities or suspicious links.",
        "Look at the age of the Reddit account (cake day) and their karma score."
    ],
    "email": [
        "Carefully examine the sender's email address for any misspellings or unusual domains.",
        "Be suspicious of emails that create a sense of urgency or pressure.",
        "Never click on links or download attachments from unsolicited or unexpected emails.",
        "Check for generic greetings like 'Dear Customer' instead of your name.",
        "In Gmail, look for the 'verified sender' checkmark for well-known brands."
    ],
    "viber": [
        "Be wary of messages from unknown numbers, especially those containing links or asking for money.",
        "Check the profile of unknown contacts for any suspicious information.",
        "Viber will never ask for your personal information or login details in a message."
    ],
    "signal": [
        "Be cautious of message requests from people you don't know.",
        "Signal is end-to-end encrypted, but that doesn't protect you from scams if you interact with a scammer.",
        "Do not share your PIN or personal information with anyone."
    ],
    "badoo": [
        "Be wary of users who immediately ask to move the conversation to another platform.",
        "Look for the 'verified user' badge on profiles.",
        "Be cautious of profiles that seem too good to be true or have professional-level photos."
    ],
    "binance": [
        "Be suspicious of anyone asking for your API keys, passwords, or 2FA codes.",
        "Double-check the domain name of the Binance website before logging in (binance.com).",
        "Binance support will never ask you to send them cryptocurrency."
    ],
    "sharechat": [
        "Be wary of profiles that post a large amount of spam or promotional content.",
        "Check for the 'verified' badge on profiles of public figures.",
        "Do not engage with users who ask for personal information or money in private chat."
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

# --- Identity Usurpation Indicators ---
IDENTITY_USURPATION_INDICATORS = [
    {
        "id": "is_new_or_backup_account",
        "prompt": "Is the profile claiming to be a 'new' or 'backup' account for someone you already know?",
        "weight_if_yes": 3,
        "details_if_yes": "Scammers often create fake accounts claiming to have lost access to their old one."
    },
    {
        "id": "exact_match_of_known_profile",
        "prompt": "Does the profile use the exact same name and profile picture as an existing profile of someone you know?",
        "weight_if_yes": 3,
        "details_if_yes": "Directly cloning a profile is a major red flag for impersonation."
    },
    {
        "id": "unverified_new_account_claim",
        "prompt": "Have you verified with the person through a different, trusted communication method that this new profile is actually theirs?",
        "weight_if_no": 2, # Note: Weight is applied if the answer is 'no'
        "details_if_no": "If you haven't verified the new account, it's highly suspicious."
    },
    {
        "id": "inconsistent_behavior",
        "prompt": "Are there inconsistencies in writing style, language, or behavior compared to the person you know?",
        "weight_if_yes": 2,
        "details_if_yes": "A change in communication style can indicate a different person is behind the account."
    },
    {
        "id": "suspicious_friend_list",
        "prompt": "Does the friend list seem unusually small, or does it lack mutual friends you'd expect?",
        "weight_if_yes": 1,
        "details_if_yes": "Impersonation accounts often have hastily assembled or illogical friend lists."
    },
    {
        "id": "urgent_requests_for_money_or_info",
        "prompt": "Is the account making urgent requests for money, gift cards, or personal information, often citing an emergency?",
        "weight_if_yes": 3,
        "details_if_yes": "This is a classic scam tactic used by impersonators to exploit the trust of friends and family."
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


def analyze_identity_usurpation(profile_url, platform):
    """
    Guides the user through a checklist to assess if a profile is impersonating someone.
    """
    print(f"\n--- Analyzing {platform.capitalize()} Profile for Identity Usurpation (Manual Check) ---")
    print("This check is designed to help you determine if a profile is impersonating someone you know.")
    print(f"Please open the profile in your browser or app: {profile_url}")
    webbrowser.open(profile_url)

    user_responses = {}
    total_score = 0
    positive_indicators = []

    print("\nYou will now be asked a series of questions about the profile.")
    for indicator in IDENTITY_USURPATION_INDICATORS:
        while True:
            answer = input(f"{indicator['prompt']} (yes/no): ").strip().lower()
            if answer in ['yes', 'no']:
                user_responses[indicator['id']] = answer
                if answer == 'yes' and 'weight_if_yes' in indicator:
                    total_score += indicator['weight_if_yes']
                    positive_indicators.append(f"- {indicator['prompt']} ({indicator['details_if_yes']})")
                elif answer == 'no' and 'weight_if_no' in indicator:
                    total_score += indicator['weight_if_no']
                    positive_indicators.append(f"- (Unverified) {indicator['prompt']} ({indicator['details_if_no']})")
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")

    print("\n--- Identity Usurpation Analysis Results ---")
    print(f"Profile URL: {profile_url}")

    if not positive_indicators:
        print("Based on your answers, no strong indicators of identity usurpation were identified.")
    else:
        print("The following indicators suggestive of identity usurpation were noted:")
        for pi in positive_indicators:
            print(pi)

        print(f"\nOverall 'impersonation suspicion score': {total_score}")
        if total_score <= 3:
            print("Assessment: Low likelihood of impersonation.")
        elif total_score <= 6:
            print("Assessment: Medium likelihood. Exercise extreme caution and verify independently.")
        else:
            print("Assessment: High likelihood. Avoid interaction and report the profile.")

    print("\nDisclaimer: This analysis is based SOLELY on your manual observations.")
    print("Always use your best judgment. If you suspect impersonation, contact the person being impersonated through a trusted channel and report the fake profile to the platform.")

    return {
        "profile_url": profile_url,
        "platform": platform,
        "score": total_score,
        "positive_indicators": positive_indicators,
    }


if __name__ == '__main__':
    print("Fake Profile Detector - Manual Checklist Tool")

    while True:
        print("\nSelect the type of analysis to perform:")
        print("1. General Fake Profile Analysis")
        print("2. Identity Usurpation Analysis")

        try:
            choice = int(input("Enter your choice (1-2): "))
            if choice in [1, 2]:
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    test_platform = input("\nEnter the social media platform to simulate analyzing (e.g., instagram): ").strip().lower()
    test_profile_url = input(f"Enter a {test_platform.capitalize()} profile URL to simulate analyzing: ").strip()

    if test_profile_url and test_platform:
        if choice == 1:
            analyze_profile_based_on_user_input(test_profile_url, test_platform)
        elif choice == 2:
            analyze_identity_usurpation(test_profile_url, test_platform)
