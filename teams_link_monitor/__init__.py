"""An application that sends logging messages to a designated MS Teams Channel."""
from loguru import logger

from teams_link_monitor.notifier import TeamsNotifier
from teams_link_monitor.screenshot import capture_desktop_state

logger.disable("teams_link_monitor")

__all__ = ["TeamsNotifier", "capture_desktop_state"]
__version__ = "0.0.a1"
