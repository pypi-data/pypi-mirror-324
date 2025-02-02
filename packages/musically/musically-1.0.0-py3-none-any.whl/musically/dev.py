#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import json
import requests
from colorama import Fore, init
init(autoreset=True)
config_path = os.path.expanduser("~/.musically/dev.json")

def mask_value(value):
    return f"{value[:4]}{'*' * (len(value) - 4)}" if value and len(value) > 4 else value

def setup_config(existing_config):
    print(f"{Fore.LIGHTCYAN_EX}🚀 Setting up configuration... (Press Enter to keep existing values)\n")

    app_name = input(f"{Fore.GREEN}Enter APP_NAME [{existing_config.get('APP_NAME', 'Not Set')}]: {Fore.YELLOW}").strip() or existing_config.get("APP_NAME")
    api_url = input(f"{Fore.GREEN}Enter API_URL [{mask_value(existing_config.get('API_URL', 'Not Set'))}]: {Fore.YELLOW}").strip() or existing_config.get("API_URL")
    api_key = input(f"{Fore.GREEN}Enter API_KEY [{mask_value(existing_config.get('API_KEY', '******'))}]: {Fore.YELLOW}").strip() or existing_config.get("API_KEY")

    config_data = {
        "APP_NAME": app_name,
        "API_URL": api_url,
        "API_KEY": api_key
    }

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)

    print(f"\n{Fore.GREEN}✔ Configuration saved successfully!")
    print(f"{Fore.LIGHTCYAN_EX}Now, you can proceed with your tasks.")

def load_or_setup_config():
    if not os.path.exists(config_path):
        print(f"{Fore.RED}⚠ Config file not found at {Fore.YELLOW}{config_path}{Fore.RED}.")
        existing_config = {}
    else:
        with open(config_path, "r") as f:
            existing_config = json.load(f)

    setup_config(existing_config)
    return existing_config

ASCII_ART = f"""
{Fore.GREEN}\
____   _________    _____________ ___
\\   \\ /   /  _  \\  /   _____/    |   \\
 \\   Y   /  /_\\  \\ \\_____  \\|    |   /
  \\     /    |    \\/        \\    |  /
   \\___/\\____|__  /_______  /______/
                \\/        \\/
"""

def main():
    config = load_or_setup_config()
    name = config.get("APP_NAME", "Unknown")
    api_url = mask_value(config.get("API_URL", "Not Set"))
    api_key = mask_value(config.get("API_KEY", "Not Set"))

    print(ASCII_ART)

    print(f"{Fore.LIGHTGREEN_EX}✓ Successfully started!")
    print(f"{Fore.CYAN}================= {Fore.LIGHTMAGENTA_EX}Your Welcome! {Fore.CYAN}=================")
    print(f"{Fore.GREEN}APP_NAME  : {Fore.YELLOW}{name}")
    print(f"{Fore.GREEN}API_URL   : {Fore.CYAN}{api_url}")
    print(f"{Fore.GREEN}API_KEY   : {Fore.LIGHTMAGENTA_EX}{api_key}")
    print(f"{Fore.CYAN}========================================================")


    print(f"{Fore.LIGHTCYAN_EX}To begin the upload process, type {Fore.YELLOW}musical{Fore.LIGHTCYAN_EX}.\n")

    print(f"{Fore.LIGHTMAGENTA_EX}📌 Developed by Ankit Chaubey")
    print(f"{Fore.LIGHTWHITE_EX}Release Date: {Fore.LIGHTWHITE_EX}3 December 2024")
    print(f"{Fore.LIGHTWHITE_EX}PYPI Version: (V1.0.0) {Fore.LIGHTWHITE_EX}2 February 2025")
    print(f"{Fore.LIGHTWHITE_EX}API Version: (V2.4) {Fore.LIGHTWHITE_EX}1 February 2025\n")

    print(f"{Fore.LIGHTYELLOW_EX}⚠️ This bot is provided strictly for private use.")
    print(f"{Fore.LIGHTRED_EX}❗ Redistribution, publication, or commercial sale is strictly prohibited.")
    print(f"{Fore.LIGHTCYAN_EX}Before using, ensure you have the necessary rights to use this bot.\n")

    print(f"{Fore.LIGHTWHITE_EX}🔗 Licensed under the Private Use License.")
    print(f"{Fore.LIGHTCYAN_EX}For more details, visit: {Fore.LIGHTBLUE_EX}https://github.com/ankit-chaubey/uploader-bot\n")

    print(f"{Fore.LIGHTGREEN_EX}Thank You, Have a nice day!")

if __name__ == "__main__":
    main()
