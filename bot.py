import os
import logging
import re
import time
from typing import Dict, Optional
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discordwebhook import Discord

# --- Configuration ---
# Load the webhook from an environment variable for security
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

COMMIT_URL = "https://commits.facepunch.com/r/rust_reboot"
POLL_INTERVAL_SECONDS = 50

# --- Keyword Filter ---
# The bot will only post commits containing at least one of these keywords.
# The search is case-insensitive.
KEYWORDS = {
    "and switch", "audio alarm", "auto turret", "autoturret", "automated",
    "battery", "blocker", "boom box", "boomer", "button", "cable tunnel", "cctv",
    "cctv camera", "ceiling light", "champagne boomer", "computer station",
    "connected speaker", "conveyor", "counter", "deluxe christmas lights",
    "disco ball", "disco floor", "door controller", "drone", "electric",
    "electric furnace", "electric heater", "electrical branch", "elevator",
    "flasher light", "fluid", "fluid combiner", "fluid splitter",
    "fluid switch & pump", "fogger-3000", "fuel tank vehicle module",
    "generator", "green industrial light", "hammer", "hbhf", "hbhf sensor",
    "horizontal weapon rack", "hose tool", "igniter", "industrial",
    "industrial combiner", "industrial conveyor", "industrial crafter",
    "industrial splitter", "industrial wall light", "large animated neon sign",
    "large battery", "large neon sign", "large solar panel",
    "large water catcher", "laser detector", "laser light", "memory cell",
    "medium animated neon sign", "medium neon sign",
    "medium rechargeable battery", "microphone stand", "modular car lift",
    "or switch", "pattern boomer", "pipe tool", "pipes", "powered",
    "powered water purifier", "pressure pad", "ptz cctv camera", "rand switch",
    "reactive target", "red industrial light", "rf broadcaster", "rf pager",
    "rf receiver", "rf transmitter", "roman candle", "root combiner", "rust+",
    "sam site", "search light", "seismic", "simple light", "siren light",
    "small generator", "small neon sign", "small rechargeable battery",
    "small water catcher", "smart alarm", "smart switch", "snow machine",
    "sound light", "spooky speaker", "splitter", "sprinkler",
    "storage adapter", "storage monitor", "strobe light", "switch",
    "tall weapon rack", "telephone", "tesla coil", "test generator",
    "timed explosive charge", "timer", "turbine", "turret", "volcano firework",
    "water barrel", "water pump", "wide weapon rack", "wind turbine", "wire",
    "wire tool", "xor switch"
}


# --- Validation ---
if not WEBHOOK_URL:
    logging.error("FATAL: DISCORD_WEBHOOK_URL environment variable not found in the container.")
    exit()

discord = Discord(url=WEBHOOK_URL)

def fetch_latest_commit() -> Optional[Dict]:
    """ Fetches the latest commit details from the Facepunch website. """
    try:
        response = requests.get(COMMIT_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        commit_div = soup.find('div', class_='commit columns')
        if not commit_div:
            logging.warning("Could not find commit information on the page.")
            return None
        commit_id = int(commit_div['like-id'])
        author = commit_div.find('div', class_='author').text.strip()
        repo = commit_div.find('span', class_='repo').text.strip()
        branch = commit_div.find('span', class_='branch').text.strip()
        changeset = commit_div.find('span', class_='changeset').text.strip()
        message = commit_div.find('div', class_='commits-message').text.strip()
        
        return {"id": commit_id, "author": author, "repo": repo, "branch": branch, "changeset": changeset, "message": message}
    except requests.RequestException as e:
        logging.error(f"Error fetching commit page: {e}")
        return None
    except (AttributeError, TypeError, KeyError) as e:
        logging.error(f"Error parsing commit details: {e}")
        return None

def send_discord_notification(commit: Dict):
    """Sends a stylish, text-based commit notification to Discord."""
    logging.info(f"Sending notification for commit {commit['id']}...")

    unix_timestamp = int(datetime.now().timestamp())
    message_content = f"""New commit by *{commit['author']}* <t:{unix_timestamp}:R>:
```{commit['repo']}:
{commit['message']}
```"""
    discord.post(content=message_content)

def main():
    """ Main loop to check for and report new commits. """
    logging.info("Starting Rust commit checker with keyword filtering enabled.")
    time.sleep(5)
    
    latest_commit = fetch_latest_commit()
    last_commit_id = latest_commit['id'] if latest_commit else 0
    logging.info(f"Initialized with latest commit ID: {last_commit_id}")

    while True:
        commit = fetch_latest_commit()
        if commit and commit['id'] > last_commit_id:
            logging.info(f"New commit found: {commit['id']} (previously {last_commit_id})")
            
            # --- Filtering Logic ---
            commit_message_lower = commit['message'].lower()
            if any(keyword in commit_message_lower for keyword in KEYWORDS):
                logging.info(f"Commit {commit['id']} contains a keyword. Sending notification.")
                send_discord_notification(commit)
            else:
                logging.info(f"Commit {commit['id']} does not contain any keywords. Skipping.")
            
            # Always update the last commit ID to avoid re-checking old commits
            last_commit_id = commit['id']
        
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()