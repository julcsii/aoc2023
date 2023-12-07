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


def main(cfg):
    rows_to_print = 10
    input_list = read_txt(cfg.data.input)
    logger.debug(input_list[:rows_to_print])

    calibration_codes = extract_calibration_codes(input_list)
    logger.debug(calibration_codes[:rows_to_print])

    total_sum = sum(calibration_codes)
    logger.info(total_sum)


def extract_calibration_codes(inputs: List[str]) -> List[int]:
    return [code for i in inputs if (code := extract_calibration_code(i)) is not None]

def extract_calibration_code(input_str: str) -> Optional[int]:
    digits_extracted = []
    text_chars = ""

    for ch in input_str:
        if not ch.isalnum():
            text_chars = ""
        if ch.isnumeric():
            digits_extracted.extend(extract_text_digits(text_chars))
            digits_extracted.append(ch)
            text_chars = ""
        if ch.isalpha():
            text_chars += ch

    digits_extracted.extend(extract_text_digits(text_chars))

    if digits_extracted:
        return int(f"{digits_extracted[0]}{digits_extracted[-1]}")
    return None

def extract_text_digits(input_string: str) -> List[int]:
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

    pattern = re.compile('|'.join(map(re.escape, text_to_digit_mapping.keys())), re.IGNORECASE)
    matches = re.findall(pattern, input_string, overlapped=True)

    return [int(text_to_digit_mapping[match.lower()]) for match in matches]

if __name__=="__main__":
    main(cfg)
