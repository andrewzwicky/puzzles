import requests
from bs4 import BeautifulSoup
from session import SESSION
from pprint import pprint
import numpy as np
from functools import cache

PROBLEM_URL = "https://adventofcode.com/2022/day/{}"
INPUT_URL = PROBLEM_URL + "/input"
ANSWER_URL = PROBLEM_URL + "/answer"
ANSWER_PAYLOAD = {"level": "1", "answer": None}
HEADERS = {
    "User-Agent": "github.com/andrewzwicky/puzzles"
}


def print_problem(day):
    problem_response = requests.get(
        PROBLEM_URL.format(day), headers=HEADERS, cookies={"session": SESSION}
    )
    problem_soup = BeautifulSoup(problem_response.content, "html.parser")

    problem_soup.header.decompose()

    for _tag in problem_soup.select(".share"):
        _tag.decompose()

    for _tag in problem_soup.select("#sponsor"):
        _tag.decompose()

    return str(problem_soup)

@cache
def get_problem_input(day):
    input_response = requests.get(INPUT_URL.format(day), cookies={"session": SESSION})

    raw_text = input_response.text
    cleaned_data = input_response.text.rstrip().split("\n")

    print("Raw Data:")
    print(repr(raw_text[: min(80, len(raw_text))]))

    print("Split Data:")
    if len(cleaned_data) != 0:
        pprint(cleaned_data[: min(10, len(cleaned_data))])

    else:
        cleaned_data = cleaned_data[0]
        pprint(cleaned_data[: min(80, len(cleaned_data))])

    return raw_text, cleaned_data

@cache
def submit_answer(day, level, answer):
    if answer is None:
        return False
    pprint(answer)
    answer_response = requests.post(
        url=ANSWER_URL.format(day),
        cookies={"session": SESSION},
        data={"level": level, "answer": answer},
    )

    answer_soup = BeautifulSoup(answer_response.text, "html.parser")

    message = answer_soup.article.text
    pprint(message)
    if "That's the right answer" in message:
        return True
    else:
        return False


def neighbors(arr: np.array, index, center=True, diagonals=True, UL=True, BR=True):
    shape = arr.shape
    if len(shape) == 2:
        # 2D
        row_min = col_min = 0
        row_max, col_max = shape
        row, col = index
        including = np.indices(shape)[
            :,
            max(row_min, row - 1) : min(row_max, row + 2),
            max(col_min, col - 1) : min(col_max, col + 2),
        ].reshape(2, -1)

        mask = np.ones(including.shape, dtype=bool)

        if UL is False:
            where = np.where((including[0, :] <= row) & (including[1, :] <= col))
            mask[
                :,
                np.squeeze(where),
            ] = False

        if BR is False:
            where = np.where((including[0, :] >= row) & (including[1, :] >= col))
            mask[
                :,
                np.squeeze(where),
            ] = False

        if center is False:
            where = np.where((including[0, :] == row) & (including[1, :] == col))
            mask[
                :,
                np.squeeze(where),
            ] = False

        if diagonals is False:
            where = np.where((including[0, :] != row) & (including[1, :] != col))
            mask[
                :,
                np.squeeze(where),
            ] = False

        return tuple(including[mask, ...].reshape(2, -1))

    if len(shape) == 3:
        # 3D
        row_min = col_min = depth_min = 0
        row_max, col_max, depth_max = shape
        row, col, depth = index
        including = np.indices(shape)[
            :,
            max(row_min, row - 1) : min(row_max, row + 2),
            max(col_min, col - 1) : min(col_max, col + 2),
            max(depth_min, col - 1) : min(depth_max, col + 2),
        ].reshape(3, -1)

        mask = np.ones(including.shape, dtype=bool)

        if center is False:
            where = np.where(
                (including[0, :] == row)
                & (including[1, :] == col)
                & (including[2, :] == depth)
            )
            mask[
                :,
                np.squeeze(where),
            ] = False

        if diagonals is False:
            where = np.where(
                ((including[0, :] != row) & (including[1, :] != col))
                | ((including[2, :] != depth) & (including[1, :] != col))
                | ((including[0, :] != row) & (including[2, :] != depth))
            )
            mask[
                :,
                np.squeeze(where),
            ] = False

        return tuple(including[mask, ...].reshape(3, -1))

    else:
        raise ValueError
