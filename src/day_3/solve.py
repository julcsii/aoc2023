import logging
import sys
from typing import List

from omegaconf import OmegaConf
from shapely import LineString

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
    """
    to get the coords and the numbers use regex?
    or iterate?
    
    for each row we take the numbers as a shapely line:
        (number, LineString([start index], [end index]))
    	and
        (char, Polygon())
    Put these into two geopandas df and do overlay
    """

    solution = get_parts_shape(input_list)
   
    logger.info(solution[0][1])


def get_special_character_shape(input_row: str) -> List[int]:
    pass

def get_parts_shape(inputs: List[str]):
    shapes = []
    for row_num, row in enumerate(inputs):
        logger.info(row)
        number_start_idx = None
        number = ""
        for number_end_idx, char in enumerate(row):
            logger.info(char)
            if char.isnumeric():
                # logger.info(char)
                if number_start_idx is None:
                    # if we have not yet any numbers
                    number_start_idx = number_end_idx
                number = number + char
            # if there is a . or a special character
            # or we are at the end of the row with a non-empty number
            if ((not char.isnumeric()) and (len(number) > 0)) or ((len(number) > 0) and (number_end_idx == len(row)-1)):
                line = LineString([[row_num, number_start_idx], [row_num, number_end_idx-1]])
                shape = (number, line)
                logger.info(shape)
                shapes.append(shape)
                number = ""
                number_start_idx = None
        break
    return shapes



if __name__ == "__main__":
    main(cfg)
