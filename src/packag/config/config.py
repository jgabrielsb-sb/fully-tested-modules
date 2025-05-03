from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

LOG_DIR = Path(os.getenv('LOG_DIR'))