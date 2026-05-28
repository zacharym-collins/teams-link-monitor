import os
from unittest.mock import patch

import pytest

from teams_notifier.payload import AdaptiveCardPayload

@pytest.fixture
def base_payload():
    """Fixture to provide a cleanly initialized payload builder for each test."""
    return AdaptiveCardPayload(
        script_name="SAP_Test_Script",
        error_message="Connection lost to session 0",
        timestamp="2026-05-28 12:00:00"
    )

@pytest.fixture
def clean_env(tmp_path):
    """Fixture to mock the environment variable path to a safe, temporary directory."""
    temp_dir = str(tmp_path)
    with patch.dict(os.environ, {"TEAMS_MONITOR_OUTPUT_DIR": temp_dir}):
        yield temp_dir
