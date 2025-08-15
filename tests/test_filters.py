import pytest
from privacy_guard import check_profanity_pii

# Profanity test cases
def test_check_profanity():
    assert check_profanity_pii("You are nice.") == (False, None)
    assert check_profanity_pii("shit happens.") == (True, "Profanity")
    assert check_profanity_pii("Don't be a bitch!") == (True, "Profanity")
    # Obfuscated → NOT caught by better_profanity
    assert check_profanity_pii("He said fu** off.") == (False, None)  
    assert check_profanity_pii("This is damn good!") == (True, "Profanity")
    assert check_profanity_pii("I had a cocktail") == (False, None)  # Should NOT be flagged

# PII test cases
def test_check_pii_email():
    assert check_profanity_pii("My email is test@example.com.") == (True, "email")
    assert check_profanity_pii("Reach me at fake.name123@domain.co.uk") == (True, "email")
    assert check_profanity_pii("No email here.") == (False, None)

def test_check_pii_ssn():
    assert check_profanity_pii("My SSN is 123-45-6789") == (True, "ssn")
    # Even with no dashes, we want to make sure it still matches
    assert check_profanity_pii("123456789") == (True, "ssn")
    assert check_profanity_pii("No SSN here") == (False, None)

def test_check_pii_phone():
    assert check_profanity_pii("Call me at 555-123-4567") == (True, "us_phone")
    assert check_profanity_pii("My number is (555) 123-4567") == (True, "us_phone")
    assert check_profanity_pii("Phone: 555.123.4567") == (True, "us_phone")
    assert check_profanity_pii("This is just a number: 1234") == (False, None)

def test_check_pii_mixed():
    text = "My SSN is 123-45-6789 and email is john@doe.com"
    ssn_pattern = r"\b(?!000|666|9\d{2})([0-8]\d{2}|7([0-6]\d|7[012]))([-]?)\d{2}\3\d{4}\b"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    assert check_profanity_pii(text) == (True, "ssn")  # Here, we expect SSN pattern to match

def test_check_pii_clean_text():
    assert check_profanity_pii("This is a clean sentence with no PII.") == (False, None)