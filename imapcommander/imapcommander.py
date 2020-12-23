# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# Copyright 2020 - Ronald Portier.
"""This is the main module for the imapcommander package."""
import argparse
import imaplib


class ImapCommander:
    """This is the main class for the imapcommander package."""

    def run(self):
        """Main command for imap commander."""
        print("Hello world!")
        # Pass arguments. For now only password.
        parser = argparse.ArgumentParser()
        parser.add_argument("--password", dest="password")
        args = parser.parse_args()
        # Connect to inbox
        imapserver = imaplib.IMAP4_SSL(host="mail.therp.nl")
        imapserver.login("tuser@portier.eu", args.password)
        imapserver.select()  # Default is `INBOX`
        # Find all emails in inbox and print out the message subjects.
        _, message_numbers_raw = imapserver.search(None, "ALL")
        for message_number in message_numbers_raw[0].split():
            _, msg = imapserver.fetch(
                message_number, "(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT)])"
            )
            print(msg[0][1])
        imapserver.close()
        imapserver.logout()
