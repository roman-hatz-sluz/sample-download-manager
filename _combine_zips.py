import os
import zipfile


def combine_zip_files(folder_path):
    # List all files in the directory
    files = [f for f in os.listdir(folder_path) if f.endswith(".zip")]

    # Dictionary to store files that need to be combined
    to_combine = {}

    for file in files:
        tokens = file.split(" - ")
        if len(tokens) >= 3:
            key = tokens[0] + " - " + tokens[1]
            if key not in to_combine:
                to_combine[key] = []
            to_combine[key].append(file)

    for key, zip_files in to_combine.items():
        # If there's only one file for this key, no need to combine
        if len(zip_files) == 1:
            continue

        # Create a new zip file
        print(f"creating new ZIP for {key}")
        with zipfile.ZipFile(os.path.join(folder_path, key + ".zip"), "w") as new_zip:
            for zip_file in zip_files:
                with zipfile.ZipFile(
                    os.path.join(folder_path, zip_file), "r"
                ) as old_zip:
                    for name in old_zip.namelist():
                        data = old_zip.read(name)

                        # If the file doesn't already have a directory structure, add one
                        if "/" not in name and "\\" not in name:
                            # Extract the third token for the subfolder name
                            subfolder_name = zip_file.split(" - ")[2].rsplit(".", 1)[
                                0
                            ]  # Remove .zip extension
                            new_name = os.path.join(subfolder_name, name)
                        else:
                            new_name = name

                        new_zip.writestr(new_name, data)
                # Delete the old zip file
                # os.remove(os.path.join(folder_path, zip_file))


folder_to_check = "FOLDER_NAME"
combine_zip_files(folder_to_check)
print("Combination process completed!")
