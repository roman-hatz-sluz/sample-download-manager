import os
import zipfile


def list_non_wav_files_in_zip(zip_path):
    """
    List all non-wav files in a given zip file, skipping folders.

    Args:
    - zip_path (str): Path to the zip file.

    Returns:
    - list: List of non-wav files in the zip file.
    """
    non_wav_files = []

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            # Check if it's a file (doesn't end with '/') and not a .wav file
            if not file_name.endswith("/") and not file_name.lower().endswith(".wav"):
                non_wav_files.append(file_name)

    return non_wav_files


def main(folder_path):
    """
    Check all zip files in a given folder and list non-wav files.

    Args:
    - folder_path (str): Path to the folder containing zip files.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".zip"):
                zip_path = os.path.join(root, file)
                non_wav_files = list_non_wav_files_in_zip(zip_path)

                if non_wav_files:
                    print(f"In {file}, non-wav files are:")
                    for non_wav_file in non_wav_files:
                        print(f"  - {non_wav_file}")


folder_path = "FOLDER_NAME"
main(folder_path)
