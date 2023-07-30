import os
from datetime import datetime



def del_special_chars(filename:str) -> str:
    """Removes special characters from a filename to ensure compatibility with Windows file naming rules."""

    special_chars = ["/","\\",":","*","?",'"',"<",">","|"]

    for char in special_chars:
        if char in filename:
            filename = filename.replace(char, "")

    return filename


def convert_date_format(input_date:str) -> str:

    print(f"\nDate format conversion: {input_date}\n")

    # Parse the input date in the format "YYYYMMDD"
    parsed_date = datetime.strptime(input_date, "%Y%m%d")

    # Format the parsed date to "day Month Year" (e.g., "5 May 2022")
    formatted_date = parsed_date.strftime("%d %B %Y")
    
    return formatted_date


def list_files_by_creation_date(folder_path:str,except_extensions:list=None) -> list[str]:
    # Initialize an empty list to store file paths
    file_paths = []

    # Get the absolute path of the folder
    folder_path = os.path.abspath(folder_path)

    # Iterate through all the files in the folder
    for filename in os.listdir(folder_path):

        if except_extensions is not None:
            if any([x in filename.lower() for x in except_extensions]):
                continue

        file_path = os.path.join(folder_path, filename)

        # Check if the current item is a file and not a directory
        if os.path.isfile(file_path):
            # Append the file path to the list
            file_paths.append(file_path)

    # Sort the list of file paths based on the creation date (oldest to newest)
    file_paths.sort(key=lambda x: os.path.getctime(x))

    return file_paths

