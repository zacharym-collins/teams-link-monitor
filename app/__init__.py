"""An application that sends logging messages to a designated MS Teams Channel."""
from app.notifier import TeamsNotifier
from app.screenshot import capture_desktop_state

__all__ = ["TeamsNotifier", "capture_desktop_state"]
__version__ = "0.0.a1"
