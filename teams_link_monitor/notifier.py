import os
import requests

from dotenv import load_dotenv
from loguru import logger

from teams_link_monitor.payload import AdaptiveCardPayload

class TeamsNotifier:
    def __init__(self, webhook_url=None):
        if not webhook_url:
            load_dotenv()
            self.webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
        else:
            self.webhook_url = webhook_url

        if not self.webhook_url:
            logger.critical("Teams Webhook URL missing. Pass a url directly to " \
            "TeamsNotifier() or set TEAMS_WEBHOOK_URL in your .env.")
            raise ValueError(
                "Teams Webhook URL missing. Set TEAMS_WEBHOOK_URL in your .env "
                "file or pass it explicitly to TeamsNotifier()."
            )
        
    def send_error(self, script_name, error_message, screenshot_path=None):
        """Builds and dispatches the error notification payload."""
        builder = AdaptiveCardPayload(script_name, error_message)
        payload = builder.build(screenshot_path=screenshot_path)

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            if response.ok:
                logger.info("Response successfully received.")
                return True
            else:
                logger.warning(f"Teams rejected the alert: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.critical(f"Failed to dispatch network alert to Teams: {e}")
            return False
