
import logging
import sys
from typing import List, Optional, Tuple

from omegaconf import OmegaConf
from src.utils.io import read_txt


cfg = OmegaConf.load("config.yaml") 

DIGITS = "0123456789"

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
        calibration_codes.append(code)
    return calibration_codes    


def extract_calibration_code(i: str) -> Optional[int]:
    "Returns the first and last digit from a list of strings"
    digits_extracted = []
    for ch in i:
        if ch in DIGITS:
            digits_extracted.append(ch)
    if digits_extracted and len(digits_extracted) > 0:
        return int(f"{digits_extracted[0]}{digits_extracted[-1]}")
    return None

input_list = read_txt(cfg.data.input)
logger.debug(input_list[:3])

logger.debug(DIGITS)
calibration_codes = extract_calibration_codes(input_list)
logger.debug(calibration_codes[:3])

sum = sum(calibration_codes)

logger.info(sum)