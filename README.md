
# RustCommitsToDiscord

A reliable, containerized Python bot that monitors the official [Facepunch Rust Commits page](https://commits.facepunch.com/r/rust_reboot) and sends detailed notifications for new commits directly to your Discord server using webhooks.

This project is a heavily modified fork of the original script by GloftOfficial, rebuilt with modern practices for security, robustness, and ease of deployment using Docker and GitHub Actions.

## Key Improvements from the Original

This fork includes several significant enhancements over the original script:

  * **Containerized with Docker:** The entire application is containerized, ensuring a consistent and isolated environment.
  * **Automated Builds:** A GitHub Actions workflow automatically builds the Docker image and pushes it to the GitHub Container Registry (GHCR) on every update.
  * **Secure Configuration:** The hardcoded Discord webhook URL has been removed. The bot now securely loads the webhook from an environment variable, which is ideal for Docker deployments.
  * **Robust Logging:** Implements proper logging with timestamps and severity levels, making it much easier to monitor the bot's status and troubleshoot issues.
  * **Improved Error Handling:** More specific exception handling prevents the bot from crashing silently and provides better insight into potential problems.
  * **Refactored Code:** The codebase has been structured into functions for better readability, maintainability, and scalability.
  * **Modernized Parsing:** HTML parsing logic has been made more resilient to potential changes on the source website.

## Features

  * **Real-time Commit Monitoring**: Checks for new Rust commits every 50 seconds.
  * **Detailed Discord Notifications**: Sends rich, embedded messages to a Discord webhook.
  * **Parses Rich Information**: Extracts and displays the author, repository, branch, changeset, commit message, and author's avatar for each commit.

## Installation on Unraid

This bot is designed to be deployed easily on Unraid using its Docker image from the GitHub Container Registry (GHCR).

**1. Clone This Repository (Optional)**

You only need to clone this repository if you want to make your own modifications. The deployment process uses the pre-built image from the "Packages" section of this GitHub repository.

```bash
git clone https://github.com/Zuescho/rustcommitstodiscord
```

**2. Configure Unraid for GHCR**

If you haven't already, you need to configure Unraid to be able to pull images from the GitHub Container Registry. See the instructions in [this guide's "Step 2"](https://www.google.com/search?q=https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry%23authenticating-with-a-personal-access-token-classic) for creating a Personal Access Token (PAT) and adding it to Unraid's Docker registries.

**3. Deploy the Container on Unraid**

  * Go to the **Docker** tab in your Unraid dashboard and click **Add Container**.
  * In the **Repository** field, enter the path to the image from this repository:
    `ghcr.io/zuescho/rustcommitstodiscord:latest`
  * Click **Add another Path, Port, Variable, Label or Device** and add the following environment variable:
      * **Config Type:** `Variable`
      * **Key:** `DISCORD_WEBHOOK_URL`
      * **Value:** Paste your actual Discord webhook URL here.
  * **Optional:** To add the logo, paste the following URL into the **Icon URL** field:
    `https://raw.githubusercontent.com/Zuescho/rustcommitstodiscord/main/logo.png`
  * Click **Apply** to start the container. The bot will now be running and monitoring for new commits.