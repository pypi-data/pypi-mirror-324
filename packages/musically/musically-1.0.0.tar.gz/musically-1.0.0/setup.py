#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

# Run the configuration script after installation
os.system("python3 -m musically.setup_config")

setup(
    name="musically",
    version="1.0.0",
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
            "musical-config=musically.config:main",
            "musical-gen=musically.gen:main",
            "musical-make=musically.make:main",
            "musical-dev=musically.dev:main",
            "musical-reset=musically.setup_config:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
