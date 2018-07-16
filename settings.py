import os

from dotenv import load_dotenv

load_dotenv()

# Archive
ARCHIVE_BACKEND_URL = os.getenv("ARCHIVE_BACKEND_URL", "https://kabbalamedia.info/backend")
CDN_URL = os.getenv("CDN_URL", "https://cdn.kabbalahmedia.info")

# laitman.ru
LAITMAN_RU_URL = os.getenv("LAITMAN_RU_URL", "http://blogd2.kbb1.com")
LAITMAN_RU_USERNAME = os.getenv("LAITMAN_RU_USERNAME")
LAITMAN_RU_PASSWORD = os.getenv("LAITMAN_RU_PASSWORD")
