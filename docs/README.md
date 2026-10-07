# Gmail Unread Cleaner

A safe, automated Python utility designed to clean up unread emails by year in Gmail using IMAP with `UID` commands. It includes safeguards to protect important senders, specific domains, and top-level domain extensions (`.gov`, `.ca`, etc.) from accidental deletion.

## Key Features

- **UID Operations:** Uses IMAP `UID` commands (`uid_search`, `uid_fetch`, `uid_copy`) instead of volatile sequence IDs to avoid index-shifting errors during batch operations.
- **Safe Inspection (`BODY.PEEK`):** Fetches headers and checks `\Seen` flags without accidentally marking unread emails as read during analysis.
- **Safeguard Filtering:** Prevents deletion of VIP senders using exact email addresses, entire domains, or top-level domain matching (e.g., `.gov`, `.ca`).
- **Year-Based Cleanup:** Easily target emails from specific calendar years.
- **Credential Protection:** Keeps account credentials isolated inside a local `config.py` file that is excluded from Git tracking.

## Setup Instructions
Clone the Repository
```

git clone [https://github.com/your-username/gmail-unread-cleaner.git](https://github.com/your-username/gmail-unread-cleaner.git)

```

## Configure Credentials

1. Copy the example configuration template:
```
cp config.example.py config.py
```

2. Open config.py in your text editor.

3. Add your Gmail address and a 16-character App Password:

```
EMAIL_ADDRESS = "yourname@gmail.com"
APP_PASSWORD = "abcd efgh ijkl mnop"
```

## Customize Safeguards & Settings
In config.py, customize your target year and protection rules:

```
TARGET_YEAR = 2026
BATCH_LIMIT = None  # Set to a number (e.g., 5) for testing, or None for full run

IGNORED_SENDERS = [
    EMAIL_ADDRESS.lower(),  # Protects self-sent emails
    "vip@gmail.com",
    ".gov",                  # Protects all .gov addresses
    ".ca",                   # Protects all .ca addresses
]
```

## Running the Tool
Execute the script from the root directory using Python:
```
python main.py
```