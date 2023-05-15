import os
import random
import string


def create_files(directory_path):
    extensions = ['.txt', '.py', '.md']
    for i in range(20):
        # Generate random filename and extension
        filename = ''.join(random.choice(string.ascii_lowercase))
        extension = random.choice(extensions)
        file_path = os.path.join(directory_path, filename + extension)

        # Create the file
        with open(file_path, 'w') as f:
            f.write('This is a test file.')


create_files("data/folder1")
