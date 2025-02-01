from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from a .env file

NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
