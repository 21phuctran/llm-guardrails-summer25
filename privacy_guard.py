from better_profanity import profanity
import re

def check_profanity_pii(text: str):
    """
    Check if the text contains profanity or PII.
    Returns a tuple (bool, str).
    """
    if profanity.contains_profanity(text):
        return True, "Profanity"
    
    # The current regex conservatively blocks unformatted 9-digit sequences to 
    # prevent trivial dash-stripping bypasses, accepting a higher false 
    # positive rate for better privacy protection.
    pii_regex = {
        "ssn": re.compile(r"\b(?!000|666|9\d{2})([0-8]\d{2}|7([0-6]\d|7[012]))([-]?)\d{2}\3\d{4}\b"),
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
        "us_phone": re.compile(r"\b(?:\+1[-.\s]?)?(?:\(?[2-9]\d{2}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b"),
    }

    for pattern, regex in pii_regex.items():
        if regex.search(text):
            return True, pattern
    
    return False, None
