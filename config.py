from datetime import timedelta
from pathlib import Path

# Cache Settings
CACHE_DIR = Path(".github_cache")
CACHE_DURATION = timedelta(hours=2)
 
# API Settings
DEFAULT_PER_PAGE = 100
API_TIMEOUT = 10

# Display Settings
COMMIT_PREVIEW_COUNT = 3
MESSAGE_PREVIEW_LENGTH = 70
DEFAULT_WEEKS = 52

# Graph Settings
INTENSITY_CHARS = [' ', '░', '▒', '▓', '█']
INTENSITY_LEVELS = [0, 1, 3, 6, 10]
DAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
