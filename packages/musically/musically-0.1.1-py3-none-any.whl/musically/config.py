#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import os
from colorama import Fore, init

# Initialize colorama for colored text output
init(autoreset=True)

# Define config path
config_path = os.path.expanduser("~/.musically/config.json")

# Function to load existing configuration or prompt setup if missing
def load_config():
    if not os.path.exists(config_path):
        print(f"{Fore.RED}⚠ Config file not found at {Fore.YELLOW}{config_path}{Fore.RED}.")
        return None
    with open(config_path, "r") as f:
        return json.load(f)

# Function to set up configuration interactively
def setup_config():
    print(f"{Fore.LIGHTCYAN_EX}🚀 Setting up configuration...\n")

    # Prompt user for required details
    api_id = input(f"{Fore.GREEN}Enter API_ID: {Fore.YELLOW}").strip()
    api_hash = input(f"{Fore.GREEN}Enter API_HASH: {Fore.YELLOW}").strip()
    bot_token = input(f"{Fore.GREEN}Enter BOT_TOKEN: {Fore.YELLOW}").strip()
    chat_id = input(f"{Fore.GREEN}Enter CHAT_ID: {Fore.YELLOW}").strip()
    app_name = input(f"{Fore.GREEN}Enter APP_NAME: {Fore.YELLOW}").strip()

    # Save configuration to JSON file
    config_data = {
        "API_ID": api_id,
        "API_HASH": api_hash,
        "BOT_TOKEN": bot_token,
        "CHAT_ID": chat_id,
        "APP_NAME": app_name
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)

    print(f"\n{Fore.GREEN}✔ Configuration saved successfully!")
    print(f"{Fore.LIGHTCYAN_EX}Now, you can use the following commands:")
    print(f"{Fore.YELLOW}  musical-make {Fore.LIGHTCYAN_EX}- Create zipped items for uploading")
    print(f"{Fore.YELLOW}  musical-gen  {Fore.LIGHTCYAN_EX}- Generate a .txt file for uploading")
    print(f"{Fore.YELLOW}  musical-config {Fore.LIGHTCYAN_EX}- Setup Configuration")
    print(f"{Fore.YELLOW}  musical-dev  {Fore.LIGHTCYAN_EX}- Advanced Configuration")
    print(f"{Fore.YELLOW}  musical  {Fore.LIGHTCYAN_EX}- To begin uploding!")
    print(f"\n{Fore.GREEN}✔ Setup complete! You can now proceed with your tasks.")

# Main function to show options and execute actions
def main():
    print(f"{Fore.CYAN}================= {Fore.LIGHTMAGENTA_EX}System Configuration {Fore.CYAN}=================")
    print(f"{Fore.GREEN}Press {Fore.YELLOW}b {Fore.GREEN}to begin upload information.")
    print(f"{Fore.GREEN}Press {Fore.YELLOW}c {Fore.GREEN}to set configuration.")
    print(f"{Fore.GREEN}Press {Fore.YELLOW}n {Fore.GREEN}or {Fore.YELLOW}Enter {Fore.GREEN}to skip setup and exit.")
    print(f"{Fore.CYAN}========================================================")

    choice = input(f"{Fore.LIGHTCYAN_EX}Enter your choice: {Fore.YELLOW}").strip().lower()

    if choice == "c":
        setup_config()
    elif choice == "b":
        print(f"{Fore.LIGHTCYAN_EX}🚀 Starting upload process... Type {Fore.YELLOW}musical {Fore.LIGHTCYAN_EX}to begin.\n")
    else:
        print(f"{Fore.RED}⚠ Skipping setup. Exiting...\n")

# Run main function if executed directly
if __name__ == "__main__":
    main()
