"""An application that sends logging messages to a designated MS Teams Channel."""
from teams_alert_link.notifier import TeamsNotifier
from teams_alert_link.screenshot import capture_desktop_state

__all__ = ["TeamsNotifier", "capture_desktop_state"]
__version__ = "0.0.a1"
