import os
import logging
import re
import time
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup
from discordwebhook import Discord
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from a .env file
load_dotenv() 

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get configuration from environment variables
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
COMMIT_URL = "https://commits.facepunch.com/r/rust_reboot"
POLL_INTERVAL_SECONDS = 50

# --- Validation ---
if not WEBHOOK_URL:
    logging.error("FATAL: DISCORD_WEBHOOK_URL environment variable not set.")
    exit()

discord = Discord(url=WEBHOOK_URL)

def fetch_latest_commit() -> Optional[Dict]:
    """
    Fetches the latest commit details from the Facepunch website.

    Returns:
        A dictionary containing the commit details if successful, otherwise None.
    """
    try:
        response = requests.get(COMMIT_URL)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        commit_div = soup.find('div', class_='commit columns')
        if not commit_div:
            logging.warning("Could not find commit information on the page.")
            return None

        # --- Parsing Details ---
        commit_id = int(commit_div['like-id'])
        author = commit_div.find('div', class_='author').text.strip()
        repo = commit_div.find('span', class_='repo').text.strip()
        branch = commit_div.find('span', class_='branch').text.strip()
        changeset = commit_div.find('span', class_='changeset').text.strip()
        message = commit_div.find('div', class_='commits-message').text.strip()
        
        # More robust avatar URL parsing
        avatar_div = commit_div.find('div', class_='avatar')
        avatar_url = ""
        if avatar_div and 'style' in avatar_div.attrs:
            match = re.search(r"url\('?([^'\)]+)'?\)", avatar_div['style'])
            if match:
                avatar_url = match.group(1)

        return {
            "id": commit_id,
            "author": author,
            "repo": repo,
            "branch": branch,
            "changeset": changeset,
            "message": message,
            "avatar_url": avatar_url
        }

    except requests.RequestException as e:
        logging.error(f"Error fetching commit page: {e}")
        return None
    except (AttributeError, TypeError, KeyError) as e:
        logging.error(f"Error parsing commit details: {e}")
        return None


def send_discord_notification(commit: Dict):
    """Sends a formatted commit notification to Discord."""
    logging.info(f"Sending notification for new commit: {commit['id']}")
    discord.post(
        embeds=[
            {
                "author": {"name": commit["author"], "url": COMMIT_URL},
                "title": f"{commit['repo']}{commit['branch']}{commit['changeset']}",
                "description": commit["message"],
                "thumbnail": {"url": commit["avatar_url"]}
            }
        ]
    )


def main():
    """Main loop to check for and report new commits."""
    logging.info("Starting Rust commit checker...")
    
    # Initialize with the latest commit ID without sending a notification first
    latest_commit = fetch_latest_commit()
    last_commit_id = latest_commit['id'] if latest_commit else 0
    logging.info(f"Initialized with latest commit ID: {last_commit_id}")

    while True:
        commit = fetch_latest_commit()
        if commit and commit['id'] > last_commit_id:
            logging.info(f"New commit found: {commit['id']} (previously {last_commit_id})")
            last_commit_id = commit['id']
            send_discord_notification(commit)
        
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()