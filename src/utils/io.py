from typing import List


def read_txt(file_path: str) -> List[str]:
    # removing the new line characters
    with open(file_path) as f:
        lines = [line.rstrip() for line in f]
    return lines