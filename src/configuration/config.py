import os
from dotenv import load_dotenv

load_dotenv()

URL = 'https://gothamist.com/'
IMG_DIRECTORY = './downloaded_images'
WORKER_THREAD = 10

ROBOCLOUD_URL = os.getenv("CLOUD_URL")
ROBOCLOUD_TOKEN = os.getenv("CLOUD_TOKEN")