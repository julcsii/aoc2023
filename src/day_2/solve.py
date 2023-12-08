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

    max_colors_per_game = games_df.groupby("game_id").agg("max")
    logger.debug(max_colors_per_game.head())

    max_colors_per_game["game_power"] = max_colors_per_game.apply(lambda x: x["red"]*x["green"]*x["blue"], axis=1)
    logger.debug(max_colors_per_game.head())

    solution = max_colors_per_game["game_power"].sum()
    logger.info(solution)


def parse_games(list_of_games: List[str]):
    parsed_games = []
    for game in list_of_games:
        logger.debug(game)
        game_data = parse_game(game)
        parsed_games =  parsed_games + game_data
    return parsed_games


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
