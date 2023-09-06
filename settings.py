import os

from dotenv import load_dotenv

load_dotenv()

# Constants
USER_AGENT = "archive-content-pusher"

# Archive
ARCHIVE_BACKEND_URL = os.getenv("ARCHIVE_BACKEND_URL", "https://kabbalahmedia.info/backend")
CDN_URL = os.getenv("CDN_URL", "https://cdn.kabbalahmedia.info")

# laitman.ru
LAITMAN_RU_URL = os.getenv("LAITMAN_RU_URL", "https://test.laitman-ru.kab.sh")
LAITMAN_RU_USERNAME = os.getenv("LAITMAN_RU_USERNAME", 'Som28')
LAITMAN_RU_PASSWORD = os.getenv("LAITMAN_RU_PASSWORD", 'X1(VkbFhex1tSVJykx02L2eB')
