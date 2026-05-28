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
