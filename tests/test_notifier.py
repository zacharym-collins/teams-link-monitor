import os
from unittest.mock import patch

import pytest

from teams_link_monitor.notifier import TeamsNotifier

# A dummy webhook URL that matches the pattern expected by the class
FAKE_WEBHOOK = "https://mock.webhook.office.com/webhookb2/test-token"


def test_notifier_initialization_with_explicit_url():
    """Ensure the notifier cleanly accepts an explicitly passed URL string."""
    notifier = TeamsNotifier(webhook_url=FAKE_WEBHOOK)
    assert notifier.webhook_url == FAKE_WEBHOOK


def test_notifier_initialization_from_env():
    """Ensure the notifier falls back to loading from environment variables if no URL is passed."""
    with patch.dict(os.environ, {"TEAMS_WEBHOOK_URL": FAKE_WEBHOOK}):
        notifier = TeamsNotifier()
        assert notifier.webhook_url == FAKE_WEBHOOK


def test_notifier_initialization_missing_url_raises_error():
    """Verify that a ValueError is raised immediately if no URL is found anywhere."""
    with patch("teams_link_monitor.notifier.load_dotenv") as mock_load:
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Teams Webhook URL missing"):
                TeamsNotifier()


def test_send_error_success(requests_mock):
    """Test that a standard 200 OK response from Teams results in a True return."""
    # requests_mock intercepts requests sent to our fake URL and stubs a success status
    requests_mock.post(FAKE_WEBHOOK, status_code=200, text="1")
    
    notifier = TeamsNotifier(webhook_url=FAKE_WEBHOOK)
    success = notifier.send_error("SAMPLE_Test", "An error occurred")
    
    assert success is True
    assert requests_mock.called
    # Confirm the payload sent was valid json data
    assert requests_mock.last_request.json()["type"] == "message"


def test_send_error_server_rejection(requests_mock):
    """Verify that if Teams rejects the payload (e.g., status 400), the method returns False."""
    requests_mock.post(FAKE_WEBHOOK, status_code=400, text="Summary text is required.")
    notifier = TeamsNotifier(webhook_url=FAKE_WEBHOOK)
    success = notifier.send_error("SAMPLE_Test", "Bad layout error")
    
    assert success is False


def test_send_error_network_timeout(requests_mock):
    """Ensure that if a network failure or timeout occurs, it is caught and returns False instead of crashing."""
    import requests
    # Simulate a dead socket connection exception
    requests_mock.post(FAKE_WEBHOOK, exc=requests.exceptions.ConnectTimeout)
    notifier = TeamsNotifier(webhook_url=FAKE_WEBHOOK)
    success = notifier.send_error("SAMPLE_Test", "Timeout test")
    
    assert success is False
