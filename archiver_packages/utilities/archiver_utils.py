import os, re
from archiver_packages.utilities.utilities import clear
from datetime import datetime


def rename_directory_with_timestamp(directory_path):
    if os.path.exists(directory_path):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_directory_name = f"{directory_path} (Up to {current_time})"
        os.rename(directory_path, new_directory_name)
        print(f"Directory '{directory_path}' renamed to '{new_directory_name}' with timestamp.")

    # Create the directory
    os.makedirs(directory_path)

    # Set full permissions (read, write, execute) for owner, group, and others
    os.chmod(directory_path, 0o777)


def chrome_version_exception(exception:str):

    # Find Chromedriver version
    chromedriver_version_index = exception.find("Chrome version ")
    chromedriver_version = exception[chromedriver_version_index + len("Chrome version "):].split()[0]

    # Find current browser version 
    browser_version_index = exception.find("Current browser version is ")
    browser_version = exception[browser_version_index + len("Current browser version is "):].split()[0]

    title = "Chrome Version Mismatch"
    text = f"Your current Google Chrome version is {browser_version}. For compatibility, please uninstall the current version and install Chrome version {chromedriver_version}."

    clear()

    print(f"\n{title}\n{text}")

    input("\nPress enter to exit")
    exit()


def rename_filename_to_id(filename_without_extension,html_dir,file_output_dir) -> str:
    id = re.search(r'\[([a-zA-Z0-9_-]+)\]', filename_without_extension).group(1)

    new_filename = f"{html_dir}/{id}.mp4"
    os.rename(file_output_dir, new_filename)

    return new_filename