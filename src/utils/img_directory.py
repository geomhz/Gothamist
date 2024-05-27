import os
from src.configuration.config import IMG_DIRECTORY


def save_img_directory():
    save_directory = IMG_DIRECTORY
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    return save_directory
