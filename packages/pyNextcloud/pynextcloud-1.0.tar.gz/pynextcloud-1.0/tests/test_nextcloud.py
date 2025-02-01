import unittest
from dotenv import load_dotenv
import os
from pyNextcloud.nextcloud import (
    UploadFile,
    DownloadFile,
    DownloadFile_URL,
    DirectoryExists_Check,
    CreateDirectory,
    RenamePath,
    DeletePath,
    UploadFolder
)

# Load environment variables from .env file
load_dotenv()

# Print environment variables for debugging
print("NEXTCLOUD_URL:", os.getenv('NEXTCLOUD_URL'))
print("USERNAME:", os.getenv('USERNAME'))
print("PASSWORD:", os.getenv('PASSWORD'))

# Ensure environment variables are set
assert os.getenv('NEXTCLOUD_URL'), "NEXTCLOUD_URL is not set"
assert os.getenv('USERNAME'), "USERNAME is not set"
assert os.getenv('PASSWORD'), "PASSWORD is not set"

class TestNextcloudFunctions(unittest.TestCase):

    def test_upload_file(self):
        # Add test cases for UploadFile function
        result = UploadFile('test_folder/example.html', 'HTML/example.html')
        self.assertIsNone(result)

    def test_download_file(self):
        # Add test cases for DownloadFile function
        result = DownloadFile('HTML/example.html', 'test_folder/example.html')
        self.assertIsNone(result)

    def test_download_file_url(self):
        # Add test cases for DownloadFile_URL function
        url = DownloadFile_URL('HTML/example.html')
        self.assertIsNotNone(url)

    def test_directory_exists_check(self):
        # Add test cases for DirectoryExists_Check function
        result = DirectoryExists_Check('HTML')
        self.assertIn(result, ["Directory exists", "Directory 'remote_directory' does not exist."])

    def test_create_directory(self):
        # Add test cases for CreateDirectory function
        result = CreateDirectory('new_directory')
        self.assertIn(result, ["All specified directories processed.", "An error occurred while creating the folders: ..."])

    def test_rename_path(self):
        # Add test cases for RenamePath function
        result = RenamePath('HTML/example.html', 'HTML/example2.html')
        self.assertIn(result, ["Successfully renamed/moved from 'current_path.txt' to 'new_path.txt'.", "An error occurred while renaming/moving the resource: ..."])

    def test_delete_path(self):
        # Add test cases for DeletePath function
        result = DeletePath('HTML')
        self.assertIn(result, ["Successfully deleted 'target_path.txt'.", "An error occurred while deleting the resource: ..."])

    def test_upload_folder(self):
        # Add test cases for UploadFolder function
        result = UploadFolder('test_folder', 'HTML')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()