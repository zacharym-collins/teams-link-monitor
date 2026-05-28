import os
import requests

from dotenv import load_dotenv
from teams_notifier.payload import AdaptiveCardPayload

class TeamsNotifier:
    def __init__(self, webhook_url=None):
        if not webhook_url:
            load_dotenv()
            self.webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
        else:
            self.webhook_url = webhook_url

        if not self.webhook_url:
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
                return True
            else:
                print(f"Teams rejected the alert: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Failed to dispatch network alert to Teams: {e}")
            return False
