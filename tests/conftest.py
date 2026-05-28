import pytest

from app.payload import AdaptiveCardPayload

@pytest.fixture
def base_payload():
    """Fixture to provide a cleanly initialized payload builder for each test."""
    return AdaptiveCardPayload(
        script_name="SAP_Test_Script",
        error_message="Connection lost to session 0",
        timestamp="2026-05-28 12:00:00"
    )
