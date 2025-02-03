import json
import logging
import re

logger = logging.getLogger(__name__)

def plaintext_load_command(output: str) -> None|str:
    """Extracts the command from an unstructured LLM output.

    Prompts compatible with this extraction must
    - have exactly one command
    - define the command to start with "Command:"
    """
    if len(re.findall(r'^Command:(.*)$', output, re.MULTILINE)) > 1:
        return None

    output = output.replace('```', '').strip()

    result = re.search(r'^Command:(.*)$', output, re.MULTILINE)
    if not result:
        return None
    result = result.group(1)

    command = result.strip(' `#')
    if command == "":
        return None

    return command

def json_load_list(json_str: str) -> list:
    """Parses a JSON list from a string."""
    # most common JSON parsing errors are invalid text before and after list or escaping errors
    # remove all text outside the first occurrence of [ and after the last occorrence of ].
    try: 
        json_str = '[' + json_str.split('[', 1)[1].rsplit(']', 1)[0] + ']'
        json_str = __cleanup_json(json_str)
        return json.loads(json_str)
    except:
        logger.debug("Could not parse this list: " + json_str)
        return []

def json_load_object(json_str: str) -> dict:
    """Parses a JSON object from a string."""
    # most common JSON parsing errors are invalid text before and after object or escaping errors
    # remove all text outside the first occurrence of { and after the last occorrence of }.
    try:
        json_str = '{' + json_str.split('{', 1)[1].rsplit('}', 1)[0] + '}'
        json_str = __cleanup_json(json_str)
        return json.loads(json_str)
    except:
        logger.debug("Could not parse this object: " + json_str)
        return {}

def __cleanup_json(json_str: str) -> str:
    # replace all valid occurrences of \ with random string
    json_str = re.sub(r'\\\\', 'a7cfe105473ff3ac588d5ab0ed6f1247', json_str)
    json_str = re.sub(r'\\"', 'd4a0fbadf8fd20714ebd8316ce5c5c03', json_str)
    # remove all other \
    json_str = re.sub(r'\\', '', json_str)
    # return all valid occurrences back
    json_str = re.sub(r'a7cfe105473ff3ac588d5ab0ed6f1247', '\\\\', json_str)
    json_str = re.sub(r'd4a0fbadf8fd20714ebd8316ce5c5c03', '\\"', json_str)
    return json_str

