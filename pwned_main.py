import argparse
from pwned_checker import checker

def main():
    parser = argparse.ArgumentParser(description="Check if an email account has been compromised in a data breach using the 'Have I Been Pwned?' service.")
    parser.add_argument("email", help="The email address to check.")
    args = parser.parse_args()

    print(f"Checking account: {args.email}")
    breaches = checker.check_pwned(args.email)

    if breaches:
        print("\n--- Account Found in Breaches! ---")
        print(f"The account '{args.email}' was found in the following breaches:")
        for breach in breaches:
            print(f"\n  - Breach: {breach['Name']}")
            print(f"    Domain: {breach.get('Domain', 'N/A')}")
            print(f"    Date: {breach.get('BreachDate', 'N/A')}")
            print(f"    Description: {breach.get('Description', 'N/A')}")
    elif breaches is None:
        print("\n--- No Breaches Found ---")
        print(f"The account '{args.email}' was not found in any known breaches.")
    else:
        print("\n--- An Error Occurred ---")
        print("Could not retrieve data. Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
