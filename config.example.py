# Configuration settings for Email Cleaner

# --- SERVER SETTINGS ---
IMAP_SERVER = "imap.gmail.com"  # Outlook: "outlook.office365.com", Yahoo: "imap.mail.yahoo.com"
TARGET_YEAR = 2026  # Target year to delete emails from
BATCH_LIMIT = None  # Set to an integer (e.g. 5) for testing, or None for all

# --- ACCOUNT CREDENTIALS ---
EMAIL_ADDRESS = "yourname@gmail.com"

# Enter your 16-character App Password here (e.g., "abcd efgh ijkl mnop")
# Note: For Gmail, generate an App Password in your Google Account settings 
# under Security > 2-Step Verification > App Passwords. Do NOT use your regular login password.
APP_PASSWORD = "abcd efgh ijkl mnop"


# --- SAFEGUARD FLAGS ---
# Emails matching ANY item in this list will NEVER be deleted or moved to Trash.
IGNORED_SENDERS = [
    # 1. Your own email address
    EMAIL_ADDRESS.lower(),
    
    # 2. Specific email addresses
    #"xyz@gmail.com",
    #"xu@yahoo.com",
    # "xrc@gmail.com",
    
    # 3. Top-Level Domains / Extensions (.gov, .ca, .in)
    # ".gov",
    # ".ca",
    # ".in",
    
    # 4. Entire Domains (e.g. "paypal.com", "bankofamerica.com")
    # "domain.com",
]