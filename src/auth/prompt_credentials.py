import getpass
import re

DEFAULT_EMAIL = "sudeep_patwardhan@yahoo.com"


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def prompt_for_credentials() -> dict:
    """
    Prompt user for Yahoo OAuth credentials and email.
    Credentials are returned but never stored to disk.
    """
    print("Please enter your Yahoo account details and API credentials.")
    print("You can obtain API credentials from: https://developer.yahoo.com/apps/\n")
    
    # Prompt for email with default
    while True:
        email = input(f"Enter your Yahoo email address [{DEFAULT_EMAIL}]: ").strip()
        if not email:
            email = DEFAULT_EMAIL
            print(f"   Using default: {email}")
        if not validate_email(email):
            print("❌ Invalid email format. Please enter a valid email address.")
            continue
        break
    
    # Prompt for Client ID
    while True:
        client_id = input("Enter your Client ID (Consumer Key): ").strip()
        if not client_id:
            print("❌ Client ID is required. Please try again.")
            continue
        break
    
    # Use getpass to hide the secret input
    while True:
        client_secret = getpass.getpass("Enter your Client Secret (Consumer Secret): ").strip()
        if not client_secret:
            print("❌ Client Secret is required. Please try again.")
            continue
        break
    
    return {
        'email': email,
        'client_id': client_id,
        'client_secret': client_secret
    }