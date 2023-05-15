import os
from datetime import datetime
from tabulate import tabulate


def get_files_attributes(path):
    files = os.listdir(path)
    files_attributes = []
    for file in files:
        file_path = os.path.join(path, file)
        isfolder = os.path.isdir(file_path)
        size = os.path.getsize(file_path)
        created = os.path.getctime(file_path)
        created_date = datetime.fromtimestamp(
            created).strftime('%Y-%m-%d %H:%M:%S')
        files_attributes.append((file, isfolder, size, created_date))
    return files_attributes


def compare_directories(path1, path2):
    # Get files attributes for both directories
    path1_attributes = get_files_attributes(path1)
    path2_attributes = get_files_attributes(path2)

    # Find common and different files
    common_files = set([f[0] for f in path1_attributes]) & set(
        [f[0] for f in path2_attributes])
    path1_only_files = [(f[0], f[1], f[2], f[3])
                        for f in path1_attributes if f[0] not in common_files]
    path2_only_files = [(f[0], f[1], f[2], f[3])
                        for f in path2_attributes if f[0] not in common_files]

    # Print results
    print("Compare :")
    print("  " + path1)
    print("  " + path2)
    print("\n")
    print(f"Number of common files: {len(common_files)}")
    print("\n")
    if path1_only_files:
        print(f"Files in {path1} but not in {path2}: {len(path1_only_files)}")
        print(tabulate(path1_only_files, headers=[
              "Name", "IsFolder", "Size", "Created"], tablefmt="psql"))
        print("\n")
    else:
        print(f"No files in {path1} but not in {path2}")
        print("\n")
    if path2_only_files:
        print(f"Files in {path2} but not in {path1}: {len(path2_only_files)}")
        print(tabulate(path2_only_files, headers=[
              "Name", "IsFolder", "Size", "Created"], tablefmt="psql"))
        print("\n")
    else:
        print(f"No files in {path2} but not in {path1}")
        print("\n")


compare_directories("data/folder1", "data/folder2")
