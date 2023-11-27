import os
from archiver_packages.utilities.utilities import clear



def remove_output_folder(output_directory:str):
    """
    Remove output folder to remove previously downloaded videos and 
    avoid link and downloaded video mismatch in parse_to_html() zip func.
    """
    from shutil import rmtree

    if os.path.exists(output_directory):
        rmtree(output_directory)


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