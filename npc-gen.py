
#!/usr/bin/env python3

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from Generator import NpcGenerator


def validate_api_token():
    token = os.getenv("APITOKEN")
    if not token:
        sys.exit("❌ Error: API token is missing. Make sure APITOKEN=<token> is set in your .env file.")
    token = token.strip('"').strip("'")
    os.environ["APITOKEN"] = token
    return token


def select_campaign(generator):
    campaigns = generator.get_campaigns().get("data", [])
    if not campaigns:
        sys.exit("❌ No campaigns found.")

    print("\nAvailable campaigns:")
    for idx, campaign in enumerate(campaigns):
        print(f"  [{idx}] {campaign['name']} (ID: {campaign['id']})")
    print("  [x] Exit")

    while True:
        choice = input("\nEnter the number of the campaign to use (or 'x' to cancel): ").strip().lower()
        if choice == 'x':
            print("Exiting.")
            sys.exit(0)
        try:
            index = int(choice)
            if 0 <= index < len(campaigns):
                return campaigns[index]['name']
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def main():
    parser = argparse.ArgumentParser(description="Generate random NPCs in a Kanka campaign.")
    parser.add_argument("--host", help="Set API base DOMAINNAME (e.g., kanka.example.com)")
    parser.add_argument("--campaign", help="Specify campaign name directly")
    parser.add_argument("--count", type=int, help="Number of NPCs to generate", default=None)

    args = parser.parse_args()

    # Normalize host input if provided
    if args.host:
        host = args.host.strip()
        if not host.startswith("http://") and not host.startswith("https://"):
            host = "https://" + host
        if not host.endswith("/api/1.0/"):
            host = host.rstrip("/") + "/api/1.0/"
        os.environ["API_URL"] = host

    validate_api_token()
    generator = NpcGenerator()

    campaign_name = args.campaign or select_campaign(generator)

    count = args.count
    if count is None:
        try:
            count = int(input("Enter number of NPCs to generate: "))
        except ValueError:
            sys.exit("❌ Invalid number entered.")

    generator.create_npcs(campaign_name, count)


if __name__ == "__main__":
    main()
