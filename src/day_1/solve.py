
import logging
import sys
from typing import List, Optional

from omegaconf import OmegaConf
import regex as re

from src.utils.io import read_txt


cfg = OmegaConf.load("config.yaml") 


logging.basicConfig(
    stream=sys.stdout,
    format=cfg.logging.format,
    datefmt=cfg.logging.date_format,
    level=cfg.logging.level
)
logger = logging.getLogger(__name__)

def extract_calibration_codes(inputs: List[str]) -> List[int]:
    calibration_codes = []
    for i in inputs:
        code = extract_calibration_code(i)
        if code:
            calibration_codes.append(code)
    return calibration_codes    


def extract_calibration_code(i: str) -> Optional[int]:
    "Returns the first and last digit from a list of strings"
    digits_extracted = []
    text_chars = ""
    for ch in i:
        if not ch.isalnum():
            text_chars = ""
        if ch.isnumeric():
            digits = extract_text_digits(text_chars)
            digits_extracted += digits
            digits_extracted.append(ch)
            text_chars = ""
        if ch.isalpha():
            text_chars += ch
    digits = extract_text_digits(text_chars)
    digits_extracted += digits
    if digits_extracted and len(digits_extracted) > 0:
        return int(f"{digits_extracted[0]}{digits_extracted[-1]}")
    return None


def extract_text_digits(input_string: str) -> List[int]:
    # Define a dictionary to map text representations to their numeric equivalents
    text_to_digit_mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "zero": "0",
        "null": "0"
    }

    # Create a regex pattern to match any of the text representations
    pattern = re.compile('|'.join(map(re.escape, text_to_digit_mapping.keys())), re.IGNORECASE)

    # Find all matches in the input string
    matches = re.findall(pattern, input_string, overlapped=True)

    # Convert text representations to numeric values
    result = [int(text_to_digit_mapping[match.lower()]) for match in matches]

    return result

rows_to_print = 10

input_list = read_txt(cfg.data.input)
logger.debug(input_list[:rows_to_print])

calibration_codes = extract_calibration_codes(input_list)
logger.debug(calibration_codes[:rows_to_print])

sum = sum(calibration_codes)

logger.info(sum)