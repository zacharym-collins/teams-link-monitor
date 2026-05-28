import os
from pathlib import Path
from unittest.mock import patch

from teams_notifier.screenshot import capture_desktop_state

def test_capture_desktop_state_creates_file(clean_env):
    """Verify that a physical screenshot file is generated and matches naming rules."""
    script_name = "SAMPLE_Test_Run"
    filename, filepath = capture_desktop_state(script_name)

    assert filename is not None
    assert filepath is not None
    assert filename.startswith(script_name)
    assert filename.endswith(".png")
    assert Path(filepath).exists()
    assert Path(filepath).stat().st_size > 0

def test_capture_desktop_state_creates_missing_directory(tmp_path):
    """
    Ensure the function safely creates a directory tree if the configured path
    doesn't exist yet.
    """
    nested_missing_dir = tmp_path / "nested" / "logs" / "folder"
    script_name = "SAMPLE_Missing_Dir_Test"
    with patch.dict(os.environ, {"TEAMS_MONITOR_OUTPUT_DIR": nested_missing_dir.as_posix()}):
        assert not nested_missing_dir.exists()
        _, filepath = capture_desktop_state(script_name)
        assert nested_missing_dir.exists()
        assert Path(filepath).exists()

def test_capture_desktop_state_fallback_on_permission_error(clean_env):
    """Verify that if the environment path is completely broken or locked down, it falls back to os.getcwd()."""
    invalid_dir = Path("I:/An/Invalid/Drive/Path/That/Doesnt/Exist/*?/")
    script_name = "SAMPLE_Fallback_Test"
    
    with patch.dict(os.environ, {"TEAMS_MONITOR_OUTPUT_DIR": invalid_dir.as_posix()}):
        filename, filepath = capture_desktop_state(script_name)
        
        expected_fallback_path = Path.cwd() / filename
        actual_filepath = Path(filepath)
        
        assert filename is not None
        assert actual_filepath == expected_fallback_path
        assert actual_filepath.exists()
        
        if actual_filepath.exists():
            actual_filepath.unlink()
