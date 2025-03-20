#!/bin/bash

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip git

# Clone the repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# Install Python dependencies
pip3 install -r requirements.txt

# Ask for bot token and admin ID
read -p "Enter your Telegram bot token: " BOT_TOKEN
read -p "Enter your admin ID: " ADMIN_ID

# Create a configuration file
echo "BOT_TOKEN = '$BOT_TOKEN'" > config.py
echo "ADMIN_ID = $ADMIN_ID" >> config.py

# Run the bot
python3 bot.py
