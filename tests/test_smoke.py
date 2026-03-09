def test_smoke():
    assert True


def test_generate_text_returns_llm_response():
    """Test that generate_text wires the service to the LLM and returns the response."""
    from unittest.mock import patch

    from src.services.generate_text import generate_text

    with patch("src.services.generate_text.llm_complete") as mock_llm, patch(
        "src.services.generate_text.save_generation"
    ) as mock_save:
        mock_llm.return_value = "Mocked LLM response"
        result = generate_text("Hello, world")
        assert result == "Mocked LLM response"
        mock_llm.assert_called_once_with("Hello, world")
        mock_save.assert_called_once_with("Hello, world", "Mocked LLM response")
