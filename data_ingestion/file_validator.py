import os


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".json"}


def validate_file(file_path):

    # Check whether the file exists
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return False

    # Check whether the path points to a file
    if not os.path.isfile(file_path):
        print("Error: The given path is not a file.")
        return False

    # Check whether the file is empty
    if os.path.getsize(file_path) == 0:
        print("Error: File is empty.")
        return False

    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Check whether the file type is supported
    if file_extension not in SUPPORTED_EXTENSIONS:
        print(f"Error: Unsupported file format: {file_extension}")
        return False

    print("File validation successful!")
    return True
