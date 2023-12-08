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


def main(cfg: OmegaConf) -> None:
    """
    Main function to execute the program.

    Args:
        cfg (OmegaConf): The configuration.

    Returns:
        None
    """
    rows_to_print = 10
    input_list = read_txt(cfg.data.input)
    logger.debug(input_list[:rows_to_print])

    solution = ...
    logger.info(solution)


if __name__ == "__main__":
    main(cfg)
