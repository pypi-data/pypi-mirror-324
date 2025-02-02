#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import zipfile
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def zip_folders_in_directory(base_directory):
    try:
        # Iterate through all folders in the given base directory
        for foldername, subfolders, filenames in os.walk(base_directory):
            # Skip if there are no files in the folder
            if not filenames:
                continue
            
            # Name of the zip file (same as folder name)
            zip_filename = os.path.join(foldername, os.path.basename(foldername) + ".zip")
            
            # Skip if the zip file already exists
            if os.path.exists(zip_filename):
                print(f"{Fore.YELLOW}⚠ Zip file already exists: {Fore.CYAN}{zip_filename}")
                continue
            
            # Create a zip file and add all files in the folder
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    # Add the file to the zip, keeping folder structure relative
                    zipf.write(filepath, os.path.relpath(filepath, foldername))
            
            print(f"{Fore.GREEN}✔ Zipped folder: {Fore.YELLOW}{foldername} {Fore.GREEN}into {Fore.CYAN}{zip_filename}")
    
    except Exception as e:
        print(f"{Fore.RED}✖ An error occurred: {e}")

def main():
    # Get directory input from the user
    base_directory = input(f'{Fore.BLUE}Enter the path to the base directory: {Style.RESET_ALL}').strip()

    # Check if the input path is valid
    if os.path.isdir(base_directory):
        zip_folders_in_directory(base_directory)
    else:
        print(f"{Fore.RED}✖ The specified path is not a directory!")

if __name__ == "__main__":
    main()
