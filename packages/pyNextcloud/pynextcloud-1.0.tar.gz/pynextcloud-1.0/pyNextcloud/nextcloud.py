import requests
import os
from requests.auth import HTTPBasicAuth
from .config import NEXTCLOUD_URL, USERNAME, PASSWORD

def UploadFile(LOCAL_UPLOAD_PATH=None, FILE=None, REMOTE_UPLOAD_PATH=None):
    """
    Uploads files to a Nextcloud storage server after ensuring the target directory exists.

    :param LOCAL_UPLOAD_PATH: The local path of the file to be uploaded.
    :param REMOTE_UPLOAD_PATH: The remote path on the server where the file will be uploaded.
    :return: An error message if an error is encountered; otherwise, None.
    """
    try:
        # Extract directory path from the REMOTE_UPLOAD_PATH
        remote_dir = "/".join(REMOTE_UPLOAD_PATH.split("/")[:-1])

        # Check if the directory exists
        dir_check = DirectoryExists_Check(remote_dir)
        if "does not exist" in dir_check:
            CreateDirectory(remote_dir)

        # Proceed with file upload
        if FILE:
            response = requests.put(
                NEXTCLOUD_URL + REMOTE_UPLOAD_PATH,
                data=FILE,
                auth=HTTPBasicAuth(USERNAME, PASSWORD)
            )
        else:
            with open(LOCAL_UPLOAD_PATH, 'rb') as file:
                response = requests.put(
                    NEXTCLOUD_URL + REMOTE_UPLOAD_PATH,
                    data=file,
                    auth=HTTPBasicAuth(USERNAME, PASSWORD)
                )
        if response.status_code == 201:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload file: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")

def DownloadFile(LOCAL_DOWNLOAD_PATH, REMOTE_DOWNLOAD_PATH):
    """
    Downloads files from a Nextcloud storage server.

    :param LOCAL_DOWNLOAD_PATH: The local directory path where the file will be saved.
    :param REMOTE_DOWNLOAD_PATH: The path on the remote server from where the file will be downloaded.
    :return: An error message if an error is encountered; otherwise, None.
    """
    try:
        # Send a request to GET a file from REMOTE_DOWNLOAD_PATH.
        response = requests.get(
            NEXTCLOUD_URL + REMOTE_DOWNLOAD_PATH,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        if response.status_code == 200:
            with open(LOCAL_DOWNLOAD_PATH, 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully.")
        else:
            print(f"Failed to download file: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred during download: {e}")

def DownloadFile_URL(REMOTE_DOWNLOAD_PATH):
    """
    Downloads file link of Nextcloud storage server.

    :param REMOTE_DOWNLOAD_PATH: The path on the remote server from where the file will be downloaded.
    :return: URL from which File can be downloded.
    """
    URL = NEXTCLOUD_URL + REMOTE_DOWNLOAD_PATH
    return print(URL)

def DirectoryExists_Check(DIRECTORY_PATH):
    """
    Checks if a directory exists in Nextcloud storage.

    :param DIRECTORY_PATH: The path of the directory to check.
    :return: A message indicating whether the directory exists or not.
    """
    try:
        # Send a PROPFIND request to check if the directory exists
        response = requests.request(
            "PROPFIND",  # PROPFIND is the WebDAV method for retrieving resources
            NEXTCLOUD_URL + DIRECTORY_PATH,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers={"Depth": "1"}  # Depth 1 means we just check if the folder exists, not its contents
        )
        if response.status_code == 207:  # 207 means directory exists (WebDAV specific)
            return f"Directory exists"
        elif response.status_code == 404:
            return f"Directory '{DIRECTORY_PATH}' does not exist."
        else:
            return f"Unexpected response: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred while checking the directory: {e}"

def CreateDirectory(NEW_FOLDER_PATH):
    """
    Creates a folder (or multiple nested folders) in Nextcloud.

    :param NEW_FOLDER_PATH: The path or paths where new folders will be created.
    :return: A message indicating the result of the folder creation.
    """
    try:
        # Ensure the path is in list format
        if isinstance(NEW_FOLDER_PATH, str):
            paths = NEW_FOLDER_PATH.split("/")  # Split into components for nested creation
        elif isinstance(NEW_FOLDER_PATH, list):
            paths = NEW_FOLDER_PATH
        else:
            return "Invalid folder path format. Must be a string or list."

        current_path = ""
        for path in paths:
            if path.strip():  # Skip empty components
                current_path = f"{current_path}/{path}" if current_path else path

                # Send a MKCOL request to create the directory
                response = requests.request(
                    "MKCOL", 
                    NEXTCLOUD_URL + current_path,
                    auth=HTTPBasicAuth(USERNAME, PASSWORD)
                )

                if response.status_code == 201:
                    print(f"Folder '{current_path}' created successfully.")
                elif response.status_code == 405:
                    print(f"Folder '{current_path}' already exists.")
                else:
                    print(f"Failed to create folder '{current_path}': {response.status_code} - {response.text}")

        return "All specified directories processed."
    except Exception as e:
        return f"An error occurred while creating the folders: {e}"
    
def RenamePath(CURRENT_PATH, NEW_PATH):
    """
    Renames or moves a file or directory in Nextcloud. If the new path requires non-existent folders, they will be created.

    :param CURRENT_PATH: The current path of the file or folder.
    :param NEW_PATH: The new path for the file or folder.
    :return: A message indicating the result of the operation.
    """
    try:
        # Ensure the paths are valid strings
        if not isinstance(CURRENT_PATH, str) or not isinstance(NEW_PATH, str):
            return "Both CURRENT_PATH and NEW_PATH must be strings."

        # Extract the directory part of the new path
        new_dir = "/".join(NEW_PATH.split("/")[:-1])

        # Create the new directories if they do not exist
        if new_dir:
            create_result = CreateDirectory(new_dir)
            print(create_result)
        
        # Construct the full URLs for the old and new paths
        old_url = f"{NEXTCLOUD_URL}{CURRENT_PATH}"
        new_url = f"{NEXTCLOUD_URL}{NEW_PATH}"

        # Send the MOVE request to rename/move the resource
        response = requests.request(
            "MOVE",
            old_url,
            headers={"Destination": new_url},
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )

        # Handle the response
        if response.status_code == 201 or response.status_code == 204:
            return f"Successfully renamed/moved from '{CURRENT_PATH}' to '{NEW_PATH}'."
        elif response.status_code == 404:
            return f"The resource at '{CURRENT_PATH}' does not exist."
        elif response.status_code == 403:
            return f"Permission denied to rename/move '{CURRENT_PATH}'."
        else:
            return f"Failed to rename/move '{CURRENT_PATH}': {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred while renaming/moving the resource: {e}"
    
def DeletePath(TRAGET_PATH):
    """
    Deletes a file or directory in Nextcloud. If the target is a directory, it will be deleted recursively.

    :param TRAGET_PATH: The path of the file or folder to delete.
    :return: A message indicating the result of the operation.
    """
    try:
        # Ensure the path is valid
        if not isinstance(TRAGET_PATH, str):
            return "The target_path must be a string."

        # Construct the full URL for the target path
        target_url = f"{NEXTCLOUD_URL}{TRAGET_PATH}"

        # Send the DELETE request
        response = requests.request(
            "DELETE",
            target_url,
            auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )

        # Handle the response
        if response.status_code == 204:
            return f"Successfully deleted '{TRAGET_PATH}'."
        elif response.status_code == 404:
            return f"The resource at '{TRAGET_PATH}' does not exist."
        elif response.status_code == 403:
            return f"Permission denied to delete '{TRAGET_PATH}'."
        else:
            return f"Failed to delete '{TRAGET_PATH}': {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred while deleting the resource: {e}"

def UploadFolder(LOCAL_FOLDER_PATH, REMOTE_FOLDER_PATH):
    """
    Uploads a folder and its contents to Nextcloud, overwriting any existing files.

    :param LOCAL_FOLDER_PATH: The local folder path to be uploaded.
    :param REMOTE_FOLDER_PATH: The remote folder path on Nextcloud.
    """
    try:
        for root, dirs, files in os.walk(LOCAL_FOLDER_PATH):
            relative_path = os.path.relpath(root, LOCAL_FOLDER_PATH)
            remote_path = os.path.join(REMOTE_FOLDER_PATH, relative_path).replace("\\", "/")
            
            if not DirectoryExists_Check(remote_path):
                CreateDirectory(remote_path)

            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(remote_path, file).replace("\\", "/")
                
                with open(local_file_path, 'rb') as f:
                    response = requests.put(
                        NEXTCLOUD_URL + remote_file_path,
                        data=f,
                        auth=HTTPBasicAuth(USERNAME, PASSWORD)
                    )
                    if response.status_code == 201:
                        print(f"Uploaded {local_file_path} to {remote_file_path}")
                    elif response.status_code == 409:
                        print(f"Conflict: {local_file_path} already exists at {remote_file_path}. Overwriting...")
                        response = requests.put(
                            NEXTCLOUD_URL + remote_file_path,
                            data=f,
                            auth=HTTPBasicAuth(USERNAME, PASSWORD)
                        )
                        if response.status_code == 201:
                            print(f"Successfully overwrote {local_file_path} to {remote_file_path}")
                        else:
                            print(f"Failed to overwrite {local_file_path}: {response.status_code} - {response.text}")
                    else:
                        print(f"Failed to upload {local_file_path}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred during folder upload: {e}")

def UploadFolder(LOCAL_FOLDER_PATH, REMOTE_FOLDER_PATH):
    """
    Uploads a folder and its contents to Nextcloud, ensuring all directories exist.
    """
    try:
        for root, dirs, files in os.walk(LOCAL_FOLDER_PATH):
            dirs[:] = [d for d in dirs if d not in ('.venv', '__pycache__')]
            relative_path = os.path.relpath(root, LOCAL_FOLDER_PATH)
            remote_path = os.path.join(REMOTE_FOLDER_PATH, relative_path).replace("\\", "/")
            
            CreateDirectory(remote_path)

            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(remote_path, file).replace("\\", "/")
                
                with open(local_file_path, 'rb') as f:
                    response = requests.put(
                        NEXTCLOUD_URL + remote_file_path,
                        data=f,
                        auth=HTTPBasicAuth(USERNAME, PASSWORD)
                    )
                    if response.status_code == 201:
                        print(f"Uploaded {local_file_path} to {remote_file_path}")
                    elif response.status_code == 409:
                        print(f"Conflict: {local_file_path} already exists at {remote_file_path}. Overwriting...")
                        response = requests.put(
                            NEXTCLOUD_URL + remote_file_path,
                            data=f,
                            auth=HTTPBasicAuth(USERNAME, PASSWORD)
                        )
                        if response.status_code == 201:
                            print(f"Successfully overwrote {local_file_path}")
                        else:
                            print(f"Failed to overwrite {local_file_path}: {response.status_code} - {response.text}")
                    else:
                        print(f"Failed to upload {local_file_path}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred during folder upload: {e}")
