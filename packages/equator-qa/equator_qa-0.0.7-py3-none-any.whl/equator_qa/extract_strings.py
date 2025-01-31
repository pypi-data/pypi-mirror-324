import re 

def extract_score_from_string(response_string):
    """
    Extracts a numerical score from a response string using predefined patterns.
    
    This function searches the input `response_string` for various patterns that indicate a score.
    It uses regular expressions to match different formats and returns the first found score as an integer.
    If no score pattern is matched, it returns `None`.
    
    Args:
        response_string (str):
            The string containing the evaluator's response from which to extract the score.
    
    Returns:
        Optional[int]:
            The extracted score as an integer if a pattern is matched; otherwise, `None`.
    
    Example:
        ```python
        response = "The score assigned is 85%."
        score = extract_score_from_string(response)
        print(score)  # Output: 85
        ```
    
    Notes:
        - The function is case-insensitive and handles multiple score formats.
        - Ensure that the response strings follow one of the predefined patterns for accurate extraction.
    """
    # Regular expressions to match different patterns that indicate a score
    patterns = [
        r"\"score\"\s*:\s*(\d+)",  # JSON-like: "score": 0 or "score":0
        r"'score':\s*(\d+)",       # Python dict-like: {'score': 0}
        r"'grade':\s*(\d+)",       # Python dict-like: {'grade': 0}
        r"Grade:\s*(\d+)",          # Grade without ratio, e.g., Grade: 0
        r"Grade:\s*{'score':\s*(\d+)}",  # Grade followed by Python dict, e.g., Grade: {'score': 0}
        r"Score:\s*{'score':\s*(\d+)}",  # Score followed by Python dict, e.g., Score: {'score': 0}
        r"\*\*Score:\*\*\s*{'score':\s*(\d+)}",  # Markdown Score followed by Python dict, e.g., **Score:** {'score': 20}
        r"\*\*Grade:\*\*\s*{'score':\s*(\d+)}",  # Markdown Grade followed by Python dict, e.g., **Grade:** {'score': 0}
        r"score\s*is\s*(\d+)%",               # Plain text: score is 0%
        r"score\s*of\s*\*\*(\d+)%\*\*",       # Markdown: score of **0%**
        r"the\s*score\s*assigned\s*is\s*(\d+)%",  # Assigned score: the score assigned is 0%
        r"Grade:\s*A\s*\(\s*(\d+)%\)",        # Grade with percentage, e.g., Grade: A (100%)
        r"Grade:\s*[F]\s*\(\s*(\d+)/\d+\)",   # Grade F with ratio, e.g., Grade: F (0/10)
        r"Grade:\s*(\d+)/\d+",                # Ratio format, e.g., Grade: 0/10
        r"\*\*Grade:\*\*\s*(\d+)/\d+",        # Markdown style: **Grade:** 0/10
        r"\*\*Grade:\*\*\s*F\s*\(\s*(\d+)/\d+\)",  # Markdown style with grade F: **Grade:** F (0/100)
        r"Grade:\s*\*\*(\d+)/\d+\*\*",        # Markdown format, e.g., **Grade:** 0/10
        r"Grade:\s*F\s*\(\s*(\d+)\s*out\s*of\s*\d+\)",  # Grade F with "out of", e.g., Grade: F (0 out of 10)
        r"You\s*received\s*a\s*score\s*of\s*(\d+)\s*out\s*of\s*\d+",  # Plain text: You received a score of 0 out of 10
        r"\*\*(\d+)/100\s*score\*\*",        # Markdown style, e.g., **100/100 score**
        r"would\s*earn\s*a\s*score\s*of\s*(\d+)",  # Plain text: would earn a score of 100
        r"return\s*a\s*score\s*of\s*(\d+)",       # Plain text: return a score of 0
        r"\$\\boxed{([^}]+)}\$",  # LaTeX boxed notation: $\\boxed{1}$ (Handles any content inside)
        r"\"student_answer\"\s*:\s*\"([^\"]+)\"",  # JSON: Extracts full student answer
        r"'student_answer'\s*:\s*'([^']+)'",  # Python dictionary format: {'student_answer':'1'}
        r"```json\s*\{.*?\"student_answer\"\s*:\s*\"([^\"]+)\".*?\}\s*```",  # JSON inside Markdown: ```json { "student_answer": "12" } ```
    ]    # Iterate over each pattern to find a match
    for pattern in patterns:
        match = re.search(pattern, response_string, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # If no matching score pattern is found, return None
    return None


def sanitize_string(value):
    """
    Escapes curly braces in strings to prevent issues with format specifiers in logging.
    """
    if isinstance(value, str):
        return value.replace("{", "{{").replace("}", "}}")
    return value

