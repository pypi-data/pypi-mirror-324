#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def write_direct_subfolder_paths(parent_folder):
    try:
        # Remove surrounding quotes if present
        parent_folder = parent_folder.strip('"')

        # Extract the folder name to use for the output file name
        folder_name = os.path.basename(parent_folder.rstrip("\\/"))
        output_file = os.path.join(parent_folder, f"{folder_name}.txt")

        # Get only the direct subfolders within the parent folder
        subfolders = [
            os.path.join(parent_folder, folder) 
            for folder in os.listdir(parent_folder) 
            if os.path.isdir(os.path.join(parent_folder, folder))
        ]

        # Sort the subfolders alphabetically
        subfolders.sort()

        # Write the paths in the specified format to the output file
        with open(output_file, 'w') as file:
            for folder in subfolders:
                file.write(f'"{folder}" | False\n')

        print(f'{Fore.GREEN}✔ Formatted folder paths from "{Fore.YELLOW}{parent_folder}{Fore.GREEN}" have been written to "{Fore.CYAN}{output_file}{Fore.GREEN}".')
    except Exception as e:
        print(f"{Fore.RED}✖ An error occurred: {e}")

def main():
    # Take user input for the folder path
    parent_folder = input(f'{Fore.BLUE}Enter the folder path (e.g., "D:\\imp"): {Style.RESET_ALL}').strip()
    
    # Call the function
    write_direct_subfolder_paths(parent_folder)

if __name__ == "__main__":
    main()
