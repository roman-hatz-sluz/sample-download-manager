import os
import zipfile


def bytes_to_gb(byte_size):
    """Convert bytes to gigabytes."""
    return byte_size / (2**30)


def is_valid_zip(zip_path):
    """Check if the given path is a valid zip file."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.testzip()
        return True
    except Exception as e:
        print(f"Error with file {zip_path}: {e}")
        return False


def check_zip_files_in_folder(folder_path):
    """Check all zip files in the given folder."""
    invalid_files = []
    total_invalid_size = 0
    total_zip_size = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".zip"):
                full_path = os.path.join(root, file)
                file_size = os.path.getsize(full_path)
                total_zip_size += file_size

                if not is_valid_zip(full_path):
                    print(f"Invalid zip file: {full_path}")
                    invalid_files.append(full_path)
                    total_invalid_size += file_size

    print(f"\nTotal size of invalid files: {bytes_to_gb(total_invalid_size):.2f} GB")
    print(
        f"\nTotal size of zip files that are not deleted: {bytes_to_gb(total_zip_size):.2f} GB"
    )

    # Prompt to delete invalid files
    if invalid_files:
        choice = (
            input("Do you want to delete all invalid files? (yes/no): ").strip().lower()
        )
        if choice == "yes":
            for file_path in invalid_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    total_zip_size -= os.path.getsize(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


folder_to_check = "FOLDER_NAME"
check_zip_files_in_folder(folder_to_check)
