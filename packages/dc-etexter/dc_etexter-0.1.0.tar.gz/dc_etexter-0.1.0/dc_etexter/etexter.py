"""
Send an SMS text with Python and Gmail.

Author: Denise Case
Date: 2022-12-27
Updated: 2025-02-02

"""

import logging
import smtplib
import tomllib
from email.message import EmailMessage
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(config_file: str = None):
    """Load SMS gateway settings from a TOML config file."""
    config_path = Path(config_file or ".env.toml").resolve()

    if not config_path.exists():
        logging.error(f"Config file {config_path} not found.")
        raise RuntimeError(f"Missing configuration file: {config_path}")

    try:
        with config_path.open("rb") as file:
            return tomllib.load(file)
    except Exception as e:
        logging.error(f"Error loading config file {config_path}: {e}")
        raise RuntimeError("Failed to load configuration file.")


def send_text(body: str, recipient: str = None, config_file: str = None) -> None:
    """Send a text message via an email-to-SMS gateway.

    Args:
        body (str): The text message content. Only required argument.
        Optional recipient (str): The recipient's phone number. Defaults to sms_address_for_texts in the config file.
        Optional config_file (str, optional): Path to the TOML config file. Defaults to `.env.toml`.
    """
    config = load_config(config_file)

    try:
        # Load SMS settings from config
        host = config["outgoing_email_host"]
        port = int(config["outgoing_email_port"])
        sender_email = config["outgoing_email_address"]
        sender_password = config["outgoing_email_password"]
        recipient = config["sms_address_for_texts"]

        # Create SMS message
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg.set_content(body)

        # Determine SMTP client based on port
        if port == 465:
            smtp_class = smtplib.SMTP_SSL
        elif port == 587:
            smtp_class = smtplib.SMTP
        else:
            logging.warning("Uncommon SMTP port detected. Verify your settings.")
            smtp_class = smtplib.SMTP

        # Send the text message using SMTP
        with smtp_class(host, port) as server:
            logging.info(f"Connecting to SMTP server: {host}:{port}")

            if port == 587:  # TLS required for 587
                server.starttls()
                logging.info("TLS started.")

            server.login(sender_email, sender_password)
            logging.info(f"Logged in as {sender_email}. Sending text message...")

            server.send_message(msg)
            logging.info("Text message sent successfully.")

    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP authentication failed: Invalid username/password.")
        raise RuntimeError("Authentication error: Invalid credentials.")
    except smtplib.SMTPConnectError as e:
        logging.error(f"SMTP connection error: {e}")
        raise RuntimeError(f"SMTP connection error: {e}")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        raise RuntimeError(f"SMTP error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError(f"Unexpected error: {e}")


if __name__ == "__main__":
    logging.info("Starting emailer.py")
    smileyface = "\U0001F600"
    try:
        message = "You can send notifications from Python programs." + smileyface
        send_text(message)
        logging.info(f"SUCCESS. Text sent: {message}")
    except RuntimeError as e:
        logging.error(f"ERROR:  Sending failed: {e}")
