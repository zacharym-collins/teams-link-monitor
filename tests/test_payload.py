def test_base_payload_wrapper_structure(base_payload):
    """Ensure the core Teams wraper and schema versions are accurate."""
    result = base_payload.build()
    assert result["type"] == "message"
    assert len(result["attachments"]) == 1
    card_content = result["attachments"][0]["content"]
    assert card_content["type"] == "AdaptiveCard"
    assert card_content["version"] == "1.4"

def test_payload_body_without_screenshot(base_payload):
    """Verify body contains exactly 3 blocks when no screenshot path is provided."""
    result = base_payload.build(screenshot_path=None)
    body = result["attachments"][0]["content"]["body"]
    assert len(body) == 3 # Title, FactSet, Error Details
    assert body[0]["text"] == "CRITICAL ERROR DETECTED"
    assert body[0]["color"] == "Attention"

def test_payload_body_with_screenshot(base_payload):
    """Verify the body expands to 4 blocks when a screenshot path is appended."""
    dummy_path = "C\\Logs\\fail.png"
    result = base_payload.build(screenshot_path=dummy_path)
    body = result["attachments"][0]["content"]["body"]
    assert len(body) == 4
    assert "Visual Proof Saved To:" in body[3]["text"]

def test_windows_path_backslash_sanitization(base_payload):
    """Ensures Windows backslashes are normalized to forward slashes for the JSON payload."""
    windows_path = "C:\\Users\\myusername\\OneDrive\\fail.png"
    expected_clean_path = "C:/Users/myusername/OneDrive/fail.png"
    result = base_payload.build(screenshot_path=windows_path)
    body = result["attachments"][0]["content"]["body"]
    last_block_text = body[3]["text"]
    assert expected_clean_path in last_block_text
    assert windows_path not in last_block_text
