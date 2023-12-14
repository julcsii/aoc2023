import logging
import sys
from typing import List

import geopandas as gpd
from omegaconf import OmegaConf
import pandas as pd
from shapely import LineString, Polygon, geometry

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

    lines = get_parts_shape(input_list)
    lines_gdf = gpd.GeoDataFrame(lines, columns=["number", "geometry"])
    logger.info(lines_gdf.head())

    rectangles = get_special_character_shape(input_list)
    rectangles_gdf = gpd.GeoDataFrame(rectangles, columns=["char_id", "geometry"])
    logger.info(rectangles_gdf.head())

    intersection_gdf = gpd.overlay(lines_gdf, rectangles_gdf, how="intersection", keep_geom_type=False)
    logger.info(intersection_gdf.head())
    intersection_grouped_gdf = intersection_gdf.groupby("char_id").count()
    gears_gdf = intersection_grouped_gdf[intersection_grouped_gdf["number"]==2].reset_index()
    logger.info(gears_gdf.head())
    two_matches = intersection_gdf[intersection_gdf["char_id"].isin(gears_gdf["char_id"].values.tolist())].astype({"number":int})
    solution = two_matches.groupby("char_id", as_index=False)["number"].prod().sum()
    logger.info(solution)


def get_special_character_shape(inputs: List[str]) -> List[int]:
    shapes = []
    for row_num, row in enumerate(inputs):
        for col_num, char in enumerate(row):
            if (not char.isalnum()) and (char != "."):
                # create a rectangle polygon around the special character from a bounding box
                xmin, ymin = (row_num-1, col_num-1)
                xmax, ymax = (row_num+1, col_num+1)
                bbox = xmin, ymin, xmax, ymax
                rectangle = geometry.box(*bbox, ccw=True)
                shape = (f"{char}_{row_num}_{col_num}", rectangle)
                shapes.append(shape)
    return shapes


def get_parts_shape(inputs: List[str]):
    shapes = []
    for row_num, row in enumerate(inputs):
        number_start_idx = None
        number = ""
        for number_end_idx, char in enumerate(row):
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
                shapes.append(shape)
                number = ""
                number_start_idx = None
    return shapes



if __name__ == "__main__":
    main(cfg)
