#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os
import json

config_dir = os.path.expanduser("~/.musically")
config_file = os.path.join(config_dir, "config.json")

if not os.path.exists(config_dir):
    os.makedirs(config_dir)

if not os.path.exists(config_file):
    default_config = {
        "API_ID": "your_api_id",
        "API_HASH": "your_api_hash",
        "BOT_TOKEN": "your_bot_token",
        "CHAT_ID": "your_chat_id",
        "APP_NAME": "musical"
    }
    with open(config_file, "w") as f:
        json.dump(default_config, f, indent=4)

setup(
    name="musically",
    version="0.1.0",
    author="Ankit Chaubey",
    author_email="m.ankitchaubey@gmail.com",
    description="A package for automating music-related tasks via Telegram bot.",
    long_description="This package for Telegram client that automatically uploads music in high bitrate with high-quality thumbnails and captions in sequence, streamlining the process directly from the system.",
    long_description_content_type="text/plain",
    url="https://github.com/ankit-chaubey/musically",
    packages=["musically"],
    install_requires=[
        'pyrogram',
        'tqdm',
        'colorama',
        'mutagen',
        'requests',
        'TgCrypto',
    ],
    entry_points={
        "console_scripts": [
            "musical=musically.musical:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
