#!/usr/bin/env python
# -*- coding: utf-8 -*-
# musically/setup_config.py
import os
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def setup_config():
    config_dir = os.path.expanduser("~/.musically")
    config_main_file = os.path.join(config_dir, "config.json")
    config_dev_file = os.path.join(config_dir, "dev.json")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(Fore.GREEN + "[✔] Created config directory: " + Fore.YELLOW + config_dir)

    if not os.path.exists(config_main_file):
        default_config_main = {
            "API_ID": "your_api_id",
            "API_HASH": "your_api_hash",
            "BOT_TOKEN": "your_bot_token",
            "CHAT_ID": "your_chat_id",
            "APP_NAME": "musical",
        }
        with open(config_main_file, "w") as f:
            json.dump(default_config_main, f, indent=4)
        print(Fore.GREEN + "[✔] Created main config file: " + Fore.CYAN + config_main_file)
    else:
        print(Fore.YELLOW + "[!] Main config file already exists: " + Fore.CYAN + config_main_file)

    if not os.path.exists(config_dev_file):
        default_config_dev = {
            "APP_NAME": "musical",
            "API_URL": "https://api-cli.netlify.app/{auth}.json",
            "API_KEY": "qazwsxedcrfvtgby",
        }
        with open(config_dev_file, "w") as f:
            json.dump(default_config_dev, f, indent=4)
        print(Fore.GREEN + "[✔] Created dev config file: " + Fore.CYAN + config_dev_file)
    else:
        print(Fore.YELLOW + "[!] Dev config file already exists: " + Fore.CYAN + config_dev_file)

    print(Fore.MAGENTA + Style.BRIGHT + "[✓] Configuration setup complete.")

def main():
    setup_config()

if __name__ == "__main__":
    main()
