# RustCommitsToDiscord

A reliable Python bot that monitors the official [Facepunch Rust Commits page](https://commits.facepunch.com/r/rust_reboot) and sends detailed notifications for new commits directly to your Discord server using webhooks.

This script runs continuously, checking for updates at a set interval, and provides styled, embedded messages for new commits, making it easy to keep track of Rust development in real-time.

## Features

  * **Real-time Commit Monitoring**: Checks for new Rust commits every 50 seconds.
  * **Detailed Discord Notifications**: Sends rich, embedded messages to a Discord webhook.
  * **Secure Configuration**: Keeps your Discord webhook URL safe by loading it from a `.env` file instead of hardcoding it.
  * **Robust Logging**: Implements logging for easier troubleshooting and monitoring of the bot's status.
  * **Clean and Structured Code**: The script is refactored into functions for better readability and maintenance.
  * **Parses Rich Information**: Extracts and displays the author, repository, branch, changeset, commit message, and author's avatar for each commit.

## Example Output

When a new commit is detected, a message similar to the following will be posted in your configured Discord channel:

The embed includes:

  * The author's name, linked to the commit page.
  * The repository, branch, and changeset information.
  * The full commit message.
  * The author's avatar as a thumbnail.

## Prerequisites

  * Python 3.7+
  * A Discord server where you have permissions to create and manage webhooks.

## Installation & Configuration

Follow these steps to get the bot up and running.

**1. Clone the Repository**

```bash
git clone https://github.com/GloftOfficial/RustCommitsToDiscord
cd RustCommitsToDiscord
```

**2. Create a Discord Webhook**

a. In your Discord server, go to **Server Settings \> Integrations**.
b. Click on **Webhooks \> New Webhook**.
c. Give the webhook a name (e.g., "Rust Commits"), choose the desired channel, and copy the **Webhook URL**.

**3. Install Dependencies**

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**4. Configure the Webhook URL**

a. Create a new file in the project directory named `.env`.

b. Open the `.env` file and add your webhook URL in the following format:
`DISCORD_WEBHOOK_URL="YOUR_WEBHOOK_URL_HERE"`
Replace `YOUR_WEBHOOK_URL_HERE` with the URL you copied from Discord.

## Usage

Once the configuration is complete, you can start the bot by running the `bot.py` script.

```bash
python bot.py
```

The script will start running in your terminal, logging its status and sending a notification to your Discord server whenever a new Rust commit is published.