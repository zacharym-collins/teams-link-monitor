def test_base_payload_wrapper_structure(base_payload):
    """Ensure the core Teams wraper and schema versions are accurate."""
    result = base_payload.build()
    assert result["type"] == "message"
    assert len(result["attachments"]) == 1
    card_content = result["attachments"][0]["content"]
    assert card_content["type"] == "AdaptiveCard"
    assert card_content["version"] == "1.4"
