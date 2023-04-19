import email.header
import json
import logging
import os
import re
from email.policy import default as default_policy
from getpass import getpass
from pathlib import Path

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import CommandError
from imapclient import IMAPClient
from imapclient.exceptions import LoginError


class IMAPScraper(object):
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)

    def command_scrape(self):
        imap_username = (
            input(f"Enter username for {settings.SCRAPER_IMAP_SERVER}: ")
            if not settings.SCRAPER_IMAP_USERNAME
            else settings.SCRAPER_IMAP_USERNAME
        )
        imap_password = (
            getpass(
                f"Enter password for {imap_username} at"
                f" {settings.SCRAPER_IMAP_SERVER}: "
            )
            if not settings.SCRAPER_IMAP_PASSWORD
            else settings.SCRAPER_IMAP_PASSWORD
        )

        self.log.debug(
            "IMAPClient for %s:%s",
            settings.SCRAPER_IMAP_SERVER,
            settings.SCRAPER_IMAP_PORT,
        )
        imap_client = IMAPClient(
            host=settings.SCRAPER_IMAP_SERVER, port=settings.SCRAPER_IMAP_PORT
        )
        try:
            imap_client.login(imap_username, imap_password)
        except LoginError as login_error:
            raise CommandError("Invalid credentials") from login_error
        mailboxes = []
        if settings.SCRAPER_IMAP_FLAGS:
            self.log.debug(
                "Using SCRAPER_IMAP_FLAG (%s), ignoring SCRAPER_IMAP_FOLDER",
                settings.SCRAPER_IMAP_FLAGS,
            )

            for mailbox in imap_client.list_folders():
                if any(
                    [
                        flag
                        for flag in mailbox[0]
                        if any(
                            f
                            for f in settings.SCRAPER_IMAP_FLAGS
                            if flag.decode("utf-8") == f
                        )
                    ]
                ):
                    self.log.debug(
                        "Folder '%s' has one of flags '%s'",
                        mailbox[2],
                        ", ".join(settings.SCRAPER_IMAP_FLAGS),
                    )
                    mailboxes.append(mailbox[2])

        elif settings.SCRAPER_IMAP_FOLDERS:
            self.log.debug("Using SCRAPER_IMAP_FOLDER")
            mailboxes = settings.SCRAPER_IMAP_FOLDERS
        else:
            self.log.debug("Looking in AAAAAALLLL mailboxes")
            for mailbox in imap_client.list_folders():
                mailboxes.append(mailbox[2])

        search_list = ["FROM", "ebay@ebay.com"]
        for ebay_email in [
            f"ebay@ebay.{tld}"
            for tld in ["co.uk", "de", "fr", "ch", "nl", "com.au"]
        ]:
            search_list.insert(0, "OR")
            search_list.append("FROM")
            search_list.append(ebay_email)

        messages = []
        for mailbox in mailboxes:
            self.log.debug("Selecting folder %s", mailbox)
            imap_client.select_folder(mailbox)
            mailbox_msgs = imap_client.search(search_list)
            self.log.debug("Found %s messages from eBay", len(mailbox_msgs))
            messages.append((mailbox, mailbox_msgs))

        def find_in_html(content):
            soup = BeautifulSoup(content, features="lxml")
            urls = re.findall(
                r".*\.ebay\.(?:com|co\.uk|de|fr|ch|nl|com\.au).*",
                soup.prettify(),
                re.IGNORECASE,
            )
            res = set()
            for url in urls:
                if "transid" in url.lower():
                    # just get transid + itemid
                    transid_match = re.match(
                        r".*transid(?:%3D|=)([0-9-]+)[^0-9]",
                        url,
                        re.IGNORECASE,
                    )
                    itemid_match = re.match(
                        r".*itemid(?:%3D|=)([0-9-]+)[^0-9].*",
                        url,
                        re.IGNORECASE,
                    )
                    if transid_match and itemid_match:
                        res.add((transid_match.group(1), itemid_match.group(1)))
            if res:
                return res
            return None

        def process_not_multipart(part):
            content = part.get_content()
            if part.get_content_type() == "text/html":
                matches = find_in_html(content)
                if matches:
                    return matches
            else:
                # Images, PDFs, icals, etc. Ignore
                return None

        orders = set()
        for message in messages:
            imap_client.select_folder(message[0])

            for uid, message_data in imap_client.fetch(
                set(message[1]), "RFC822"
            ).items():
                email_message: email.message.EmailMessage = (
                    email.message_from_bytes(
                        message_data[b"RFC822"], policy=default_policy
                    )
                )
                matches = None
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if not part.is_multipart():
                            matches = process_not_multipart(part)
                else:
                    matches = process_not_multipart(email_message)

                if matches:
                    for match in matches:
                        orders.add(match)

                else:
                    self.log.debug(
                        '%s Nothin found in "%s"',
                        uid,
                        email.header.decode_header(
                            email_message.get("Subject")
                        )[0][0],
                    )

        self.log.debug("%s", imap_client.logout().decode("utf-8"))
        # (transid, itemid)
        self.log.debug("Orders: %s", len(orders))
        imap_folder = Path(settings.SCRAPER_CACHE_BASE, "imap")
        try:
            os.makedirs(imap_folder)
        except FileExistsError:
            pass
        with open(
            imap_folder / "imap-ebay.json", "w", encoding="utf-8"
        ) as file:
            file.write(json.dumps(list(orders), indent=4))
