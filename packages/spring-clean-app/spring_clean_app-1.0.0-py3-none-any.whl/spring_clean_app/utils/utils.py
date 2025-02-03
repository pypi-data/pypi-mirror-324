import os


def create_file(file_path, content):
    """Create a file with the specified content."""
    with open(file_path, "w") as file:
        file.write(content)


def create_folder(folder, exist_ok):
    os.makedirs(folder, exist_ok=exist_ok)


def create_folder(base_path, folder, exist_ok=True):
    # Create the full path
    full_path = os.path.join(base_path, folder)
    # Use os.makedirs to create the nested folder structure
    os.makedirs(full_path, exist_ok=exist_ok)


def create_folders(base_path, folder_structure, exist_ok=True):
    for val in folder_structure.values():
        create_folder(base_path, val)
