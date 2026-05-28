from datetime import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from PIL import ImageGrab

def capture_desktop_state(script_name):
    load_dotenv()
    output_env = os.getenv("TEAMS_MONITOR_OUTPUT_DIR")
    output_dir = Path(output_env) if output_env else Path.cwd()
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        output_dir = Path.cwd()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{script_name}_FAIL_{timestamp}.png"
    filepath = output_dir / filename

    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)
        return filename, str(filepath)
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")
        return None, None
