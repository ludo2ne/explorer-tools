import os
from tabulate import tabulate
from datetime import datetime


class Folder:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = self.total_size()
        self.creation_date = os.path.getctime(path)

    def exists(self):
        """Checks if the folder exists
        """
        return os.path.exists(self.path)

    def total_size(self):
        """Calculates the total size of the folder and its contents.
        """
        size = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for f in filenames:
                file_path = os.path.join(dirpath, f)
                size += os.path.getsize(file_path)
        return size

    def nb_files(self):
        """Counts the total number of files in the folder
        """
        count = 0
        for root, dirs, files in os.walk(self.path):
            count += len(files) + len(dirs)
        return count

    def list_files_and_folders(self):
        file_info = []
        for item in os.listdir(self.path):
            item_path = os.path.join(self.path, item)
            created_date = os.path.getctime(item_path)
            modified_date = os.path.getmtime(item_path)
            num_files = ""
            size = os.path.getsize(item_path)
            is_folder = os.path.isdir(item_path)

            if is_folder:
                subfolder = Folder(item_path)
                size = subfolder.total_size()
                num_files = subfolder.nb_files()

            file_info.append([
                item,
                size,
                num_files,
                is_folder,
                datetime.fromtimestamp(created_date).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(modified_date).strftime('%Y-%m-%d %H:%M:%S')])

        # Sort the file info by folder and size
        file_info.sort(key=lambda x: (x[3], x[1]))

        # Format size to pretty format
        for item in file_info:
            item[1] = self.format_size(item[1])

        # Print the file info in a tabular format
        headers = ['Name', 'Size', 'Num Files',
                   'Is Folder', 'Created Date', 'Modified Date']
        print(tabulate(file_info,
                       headers=headers,
                       tablefmt="psql",
                       colalign=("left", "right", "right", "left", "left", "left")))

    def compare(self, path2):
        """Compare content with another folder
        """
        # Get files attributes for both directories
        path1_attributes = self.get_files_attributes()
        dir2 = Folder(path2)
        path2_attributes = dir2.get_files_attributes()

        # Find common and different files
        common_files = set([f[0] for f in path1_attributes]) & set(
            [f[0] for f in path2_attributes])
        path1_only_files = [(f[0], f[1], f[2], f[3])
                            for f in path1_attributes if f[0] not in common_files]
        path2_only_files = [(f[0], f[1], f[2], f[3])
                            for f in path2_attributes if f[0] not in common_files]

        print(f"Number of common files: {len(common_files)} \n")

        if path1_only_files:
            print(
                f"Files in {self.path} but not in {path2}: {len(path1_only_files)}")
            print(tabulate(path1_only_files, headers=[
                  "Name", "IsFolder", "Size", "Created"], tablefmt="psql"))
            print("\n")
        else:
            print(f"No files in {self.path} but not in {path2}")
            print("\n")

        if path2_only_files:
            print(
                f"Files in {path2} but not in {self.path}: {len(path2_only_files)}")
            print(tabulate(path2_only_files, headers=[
                  "Name", "IsFolder", "Size", "Created"], tablefmt="psql"))
            print("\n")
        else:
            print(f"No files in {path2} but not in {self.path}")
            print("\n")

    def format_size(self, size_bytes):
        """
        Converts a size in bytes to a human-readable format
        """
        for unit in ['', 'KB', 'MB', 'GB', 'TB']:
            if abs(size_bytes) < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def get_files_attributes(self):
        """List files with some attributes
        """
        files = os.listdir(self.path)
        files_attributes = []
        for file in files:
            file_path = os.path.join(self.path, file)
            isfolder = os.path.isdir(file_path)
            size = os.path.getsize(file_path)
            created = os.path.getctime(file_path)
            created_date = datetime.fromtimestamp(
                created).strftime('%Y-%m-%d %H:%M:%S')
            files_attributes.append((file, isfolder, size, created_date))
        return files_attributes
