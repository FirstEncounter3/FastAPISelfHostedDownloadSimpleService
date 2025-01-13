import os

from config import DOWNLOAD_DIRECTORY, UPLOAD_DIRECTORY


def create_download_and_upload_directory() -> None:
    os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def get_all_files_from_download_directory() -> list[str]:
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
