from datetime import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from PIL import ImageGrab

def capture_desktop_state(script_name):
    load_dotenv()
    output_env = os.getenv("TEAMS_MONITOR_OUTPUT_DIR")
    output_dir = Path(output_env) if output_env else Path.cwd()
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        logger.warning("Failed to create MONITOR_OUTPUT_DIR. Falling back to current working directory.")
        output_dir = Path.cwd()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{script_name}_FAIL_{timestamp}.png"
    filepath = output_dir / filename

    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)
        return filename, str(filepath)
    except Exception as e:
        logger.exception("Failed to capture desktop screenshot state.")
        return None, None
