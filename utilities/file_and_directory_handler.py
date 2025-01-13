import os

from config import DOWNLOAD_DIRECTORY


def create_download_directory():
    if not os.path.exists(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)


def get_all_files_from_download_directory():
    try:
        all_items = os.listdir(DOWNLOAD_DIRECTORY)
        files = [
            item
            for item in all_items
            if os.path.isfile(os.path.join(DOWNLOAD_DIRECTORY, item))
        ]
        return files
    except FileNotFoundError:
        return []