import os
import shutil
import requests



def move_file(source_path:str, destination_path:str):
    try:
        # Check if source file exists
        if not os.path.exists(source_path):
            print(f"Source file '{source_path}' does not exist.")
            return

        # Move the file
        shutil.move(source_path, destination_path)
        print(f"File '{source_path}' moved to '{destination_path}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_directory(directory_name:str):
    try:
        # Check if the directory already exists
        if not os.path.exists(directory_name):
            # Create the directory
            os.makedirs(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        else:
            print(f"Directory '{directory_name}' already exists.")
    except OSError as error:
        print(f"Error creating directory '{directory_name}': {error}")


def copy_file_or_directory(source_path:str, destination_path:str):
    try:
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"File copied successfully from {source_path} to {destination_path}")
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
            print(f"Directory copied successfully from {source_path} to {destination_path}")
        else:
            print("Invalid source path. Neither a file nor a directory.")
    except FileNotFoundError:
        print("Source path not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")


def del_special_chars(filename:str) -> str:
    """ Removes special characters from a filename to ensure compatibility with Windows file naming rules. """

    special_chars = ["/","\\",":","*","?",'"',"<",">","|"]

    for char in special_chars:
        if char in filename:
            filename = filename.replace(char, "")

    return filename


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


def extract_filename_without_extension(file_path):
    filename_with_extension = os.path.basename(file_path)
    filename_without_extension, _ = os.path.splitext(filename_with_extension)
    return filename_without_extension


def download_file(thumbnail_url, save_path):
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Thumbnail saved to {save_path}")
        else:
            print(f"Error downloading thumbnail. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")