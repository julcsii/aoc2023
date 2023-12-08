import logging
import sys
from typing import Dict, List

from omegaconf import OmegaConf
import pandas as pd

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

    games = parse_games(input_list)
    logger.debug(games)

    games_df = pd.DataFrame(games).fillna(0)
    logger.debug(games_df.head(5))

    possible_games = get_possible_games(games_df, 12, 13, 14)
    logger.debug(possible_games.head())

    solution = possible_games.reset_index()["game_id"].astype("int").sum()
    logger.info(solution)


def parse_games(list_of_games: List[str]):
    parsed_games = []
    for game in list_of_games:
        logger.debug(game)
        game_data = parse_game(game)
        parsed_games =  parsed_games + game_data
    return parsed_games


def get_possible_games(games_df: pd.DataFrame, max_red, max_green, max_blue) -> pd.DataFrame:
    max_colors_per_game = games_df.groupby("game_id").agg("max")
    red_limit = max_colors_per_game["red"] <= max_red
    green_limit = max_colors_per_game["green"] <= max_green
    blue_limit = max_colors_per_game["blue"] <= max_blue
    possible_games = red_limit & green_limit & blue_limit
    return max_colors_per_game[possible_games]


def parse_game(game: str) -> List[Dict[str, int]]:
    # 'Game 1: 9 red, 5 blue, 6 green; 6 red, 13 blue; 2 blue, 7 green, 5 red'
    parsed_games = []
    game_title, sub_games = game.split(": ")
    for sub_game in sub_games.split("; "):
        # 9 red, 5 blue, 6 green
        sample = sub_game.split(", ")
        game_parsed = {
            "game_id": game_title.split(" ")[-1],
        }
        for result in sample:
            count, colour = result.split(" ")
            game_parsed[colour] = int(count)
        parsed_games.append(game_parsed)
    # [{'game_id': '1', 'red': '9', 'blue': '5', 'green': '6'}, {'game_id': '1', 'red': '6', 'blue': '13'}, {'game_id': '1', 'blue': '2', 'green': '7', 'red': '5'}]
    return parsed_games




if __name__ == "__main__":
    main(cfg)
