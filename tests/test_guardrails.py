import pytest
from unittest.mock import patch
from app import generate
from privacy_guard import check_profanity_pii

# Mocked check_profanity_pii function for unit tests
def mock_check_profanity_pii(content):
    if "shit" in content:
        return True, "profanity"
    if "123-45-6789" in content:
        return True, "SSN"
    return False, None

# Test for query blocking due to profanity
@patch("privacy_guard.check_profanity_pii", side_effect=mock_check_profanity_pii)
def test_query_blocking(mock_check):
    state = {
        "question": "Can you say shit?",
        "context": [],
        "answer": ""
    }
    result = generate(state)
    assert result == {"answer": "[Blocked: Query]"}
    mock_check.assert_called_once_with(state["question"])

# Test for context blocking due to PII
@patch("privacy_guard.check_profanity_pii", side_effect=mock_check_profanity_pii)
def test_context_blocking(mock_check):
    state = {
        "question": "Tell me a joke",
        "context": [{"page_content": "My SSN is 123-45-6789."}],
        "answer": ""
    }
    result = generate(state)
    assert result == {"answer": "[Blocked: Context]"}
    mock_check.assert_any_call("My SSN is 123-45-6789.")

# Test for response blocking due to profanity
@patch("privacy_guard.check_profanity_pii", side_effect=mock_check_profanity_pii)
@patch("app.log_to_csv")
def test_response_blocking(mock_log, mock_check):
    state = {
        "question": "Tell me a joke",
        "context": [{"page_content": "Some context."}],
        "answer": ""
    }
    with patch("app.llm.invoke", return_value=type("obj", (object,), {"content": "That's shit!"})):
        result = generate(state)
    assert result == {"answer": "[Blocked: Response]"}
    mock_check.assert_any_call("That's shit!")
    mock_log.assert_called_once()

# Test for successful response (No Blockage)
@patch("privacy_guard.check_profanity_pii", side_effect=mock_check_profanity_pii)
@patch("app.log_to_csv")
def test_successful_response(mock_log, mock_check):
    state = {
        "question": "Tell me a joke",
        "context": [{"page_content": "Some context."}],
        "answer": ""
    }
    with patch("app.llm.invoke", return_value=type("obj", (object,), {"content": "That's a good joke!"})):
        result = generate(state)
    assert result == {"answer": "That's a good joke!"}
    mock_check.assert_any_call(state["question"])
    mock_log.assert_called_once()