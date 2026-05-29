"""
This class handles building the Adaptive Card JSON layout.
"""

from datetime import datetime

class AdaptiveCardPayload:
    def __init__(self, script_name, error_message, timestamp=None):
        self.script_name = script_name
        self.error_message = error_message
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def build(self, screenshot_path=None, color="Attention", title="CRITICAL ERROR DETECTED"):
        """Dynamically constructs the JSON payload based on arguments provided."""
        body = [
            {
                "type": "TextBlock",
                "text": title,
                "weight": "Bolder",
                "size": "Medium",
                "color": color
            },
            {
                "type": "FactSet",
                "facts": [
                    {"title": "Script:", "value": self.script_name},
                    {"title": "Time:", "value": self.timestamp}
                ]
            },
            {
                "type": "TextBlock",
                "text": f"**Error Details:**\n```\n{self.error_message}\n```",
                "wrap": True
            }
        ]

        if screenshot_path:
            clean_path = str(screenshot_path).replace("\\", "/")
            body.append({
                "type": "TextBlock",
                "text": f"**Visual Proof Saved To:**\n`{clean_path}`",
                "wrap": True,
                "isSubtle": True
            })

        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.4",
                        "body": body
                    }
                }
            ]
        }
