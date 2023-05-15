import os
from tabulate import tabulate
import datetime


def list_files_and_folders(path):
    """
    Prints a table of all files and folders in the given directory and their properties, including:
    - Name
    - Size (formatted for readability)
    - Number of files (for folders only)
    - Is Folder (Yes/No)

    Additionally, two columns have been added to display the creation date and last modified date of each file or folder.

    Args:
        path (str): The path to the directory to search for files and folders.

    Returns:
        None. The function prints the results in a tabular format.
    """
    # Create an empty list to store file info
    file_info = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        is_folder = os.path.isdir(item_path)
        if is_folder:
            size = get_folder_size(item_path)
            num_files = count_files_in_folder(item_path)
            created_date = os.path.getctime(item_path)
            modified_date = os.path.getmtime(item_path)
            file_info.append([item, format_size(size), num_files, "Yes", datetime.datetime.fromtimestamp(created_date).strftime(
                '%Y-%m-%d %H:%M:%S'), datetime.datetime.fromtimestamp(modified_date).strftime('%Y-%m-%d %H:%M:%S')])
        else:
            size = os.path.getsize(item_path)
            created_date = os.path.getctime(item_path)
            modified_date = os.path.getmtime(item_path)
            file_info.append([item, format_size(size), "", "No", datetime.datetime.fromtimestamp(created_date).strftime(
                '%Y-%m-%d %H:%M:%S'), datetime.datetime.fromtimestamp(modified_date).strftime('%Y-%m-%d %H:%M:%S')])

    # Sort the file info by folder and size
    file_info.sort(key=lambda x: (x[3], x[1]))

    # Print the file info in a tabular format
    headers = ['Name', 'Size', 'Num Files',
               'Is Folder', 'Created Date', 'Modified Date']
    print(tabulate(file_info, headers=headers, tablefmt="psql"))


def get_folder_size(folder_path):
    """
    Returns the total size of a folder and all its subfolders in bytes.

    Args:
        folder_path (str): The path to the folder to calculate the size of.

    Returns:
        total_size (int): The size of the folder and all its subfolders in bytes.
    """
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size


def count_files_in_folder(folder_path):
    """
    Counts the total number of files in a folder and all its subfolders.

    Args:
        folder_path (str): The path to the folder to count the files of.

    Returns:
        count (int): The total number of files in the folder and all its subfolders.
    """
    count = 0
    for root, dirs, files in os.walk(folder_path):
        count += len(files)
    return count


def format_size(size_bytes):
    """
    Converts a size in bytes to a human-readable format (e.g. 1.23 MB).

    Args:
        size_bytes (int): The size in bytes to convert.

    Returns:
        size_str (str): The human-readable size string.
    """
    for unit in ['', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


list_files_and_folders("/home/ensai/cloud computing")
