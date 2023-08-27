import requests
import zipfile
import os


def is_valid_zip(zip_path):
    """Check if the given path is a valid zip file."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.testzip()
        return True
    except Exception as e:
        print(f"Error with file {zip_path}: {e}")
        return False


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = [
        value.strip()
        for part in cd.split(";")
        if "filename=" in part
        for value in part.split("=")[1:]
    ]
    return fname[0].strip('"') if fname else None


def check_and_download_zip(url):
    # Send a HEAD request to get the content type without downloading the whole file
    response = requests.head(url)

    # Check if the content type is for a zip file
    if "content-type" in response.headers and (
        response.headers["content-type"] == "application/zip"
        or response.headers["content-type"] == "application/octet-stream"
    ):
        print("Zip file found! Downloading...")

        # Download the zip file
        response = requests.get(url)

        # Extract filename from Content-Disposition header
        filename = get_filename_from_cd(response.headers.get("content-disposition"))
        if not filename:
            filename = "downloaded_file.zip"

        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Download complete! Saved as {filename}")

        # Check if the downloaded file is a valid zip
        if not is_valid_zip(filename):
            print(f"Invalid zip file: {filename}. Deleting...")
            os.remove(filename)  # Delete the invalid zip file
            return 0  # Return 0 as no valid data was downloaded

        # Return the size of the downloaded content
        return len(response.content)
    else:
        print("No zip file found at the provided link.")
        return 0


# Initialize total_downloaded to 0
total_downloaded = 0

# Loop through numbers 1 to 10,000
for number in range(13093, 100000):
    print(f"Check number {number}")
    url = f"FOLDER_NAME/download/{number}/"

    # Add the size of the downloaded file to total_downloaded
    total_downloaded += check_and_download_zip(url)

    # Print the total amount of data downloaded so far
    print(f"Total data downloaded so far: {total_downloaded / (1024 * 1024):.2f} MB")
