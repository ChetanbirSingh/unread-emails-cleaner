import email
from email.header import decode_header
import imaplib
import sys
from config import EMAIL_ADDRESS, APP_PASSWORD, IMAP_SERVER, IGNORED_SENDERS, TARGET_YEAR, BATCH_LIMIT

# Force UTF-8 output to prevent Windows 'charmap' encoding errors with emojis/characters
sys.stdout.reconfigure(encoding="utf-8")


def decode_str(header_value):
    """Utility to safely decode email headers like Subject and From."""
    if not header_value:
        return ""
    decoded_fragments = decode_header(header_value)
    text = ""
    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            text += fragment.decode(encoding or "utf-8", errors="ignore")
        else:
            text += str(fragment)
    return text


def check_protected(sender_header):
    """Parses sender header and checks against IGNORED_SENDERS safely."""
    if not sender_header:
        return False

    _, email_addr = email.utils.parseaddr(sender_header)
    email_clean = email_addr.lower().strip()

    if not email_clean:
        return False

    domain = email_clean.split("@")[-1] if "@" in email_clean else ""

    for item in IGNORED_SENDERS:
        item = item.lower().strip()

        if item.startswith("."):
            if domain.endswith(item):
                return True
        elif item == email_clean or item == domain:
            return True

    return False


def clean_unread_by_year(year, limit=None):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, APP_PASSWORD)
        mail.select("INBOX")

        since_date = f"01-Jan-{year}"
        before_date = f"01-Jan-{year + 1}"

        print(f"Searching for strictly UNREAD emails from year {year}...")
        
        # Explicit IMAP search for UNSEEN (Unread) emails
        status, response = mail.uid("search", None, "UNSEEN", "SINCE", since_date, "BEFORE", before_date)

        if status != "OK" or not response[0]:
            print("No matching emails found.")
            mail.logout()
            return

        email_uids = response[0].split()
        total_found = len(email_uids)
        print(f"Total unread candidate UIDs found from {year}: {total_found}\n")

        safe_email_uids = []
        skipped_count = 0

        print("--- CHECKING & FILTERING EMAILS ---")
        for e_uid in email_uids:
            # Fetch FLAGS and Header in one PEEK call to verify UNSEEN status
            _, msg_data = mail.uid("fetch", e_uid, "(FLAGS BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])")
            
            is_unread = True
            sender = "Unknown Sender"
            subject = "No Subject"

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = decode_str(msg.get("From", sender))
                    subject = decode_str(msg.get("Subject", subject))
                elif isinstance(response_part, bytes):
                    # Direct check: double-verify the email doesn't have the \Seen flag
                    if b"\\Seen" in response_part:
                        is_unread = False

            # Skip if Python flag check reveals it was already marked as SEEN
            if not is_unread:
                print(f"👁️ SKIPPED (Already Read): From: {sender} | Subject: {subject}")
                continue

            # Check protection rules
            if check_protected(sender):
                print(f"🛡️ SKIPPED (Protected): From: {sender} | Subject: {subject}")
                skipped_count += 1
            else:
                safe_email_uids.append(e_uid)

            if limit and len(safe_email_uids) >= limit:
                print(f"\n👉 BATCH LIMIT REACHED: Processing max {limit} items.")
                break

        print("------------------------------------\n")

        if not safe_email_uids:
            print("No unread emails left to process after safety checks!")
            mail.logout()
            return

        # Move to Gmail Trash using Native Gmail IMAP Labels
        trash_folder = "[Gmail]/Trash" if "gmail" in IMAP_SERVER.lower() else "Trash"

        for e_uid in safe_email_uids:
            # Copy UID to trash and mark for deletion
            mail.uid("copy", e_uid, trash_folder)
            mail.uid("store", e_uid, "+FLAGS", "(\\Deleted)")

        mail.expunge()
        print(f"\n✅ Done! Moved {len(safe_email_uids)} unread email(s) to Trash. Skipped {skipped_count} protected email(s).")

        mail.logout()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    clean_unread_by_year(TARGET_YEAR, limit=BATCH_LIMIT)