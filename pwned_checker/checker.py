import requests
import json

API_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/{account}"

def check_pwned(account):
    """
    Checks the 'Have I Been Pwned?' API for a given account.

    Args:
        account (str): The email address to check.

    Returns:
        A list of breach data if found, None otherwise.
    """
    headers = {
        "hibp-api-key": "YOUR_API_KEY_HERE"  # A free API key can be obtained from https://haveibeenpwned.com/API/Key
    }
    try:
        response = requests.get(API_URL.format(account=account), headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None  # Not found, so not pwned
        else:
            print(f"Error: Received status code {response.status_code} from the API.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
