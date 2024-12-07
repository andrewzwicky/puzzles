import pathlib
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import numpy as np

from session import SESSION

PROBLEM_URL = "https://adventofcode.com/2024/day/{}"
INPUT_URL = PROBLEM_URL + "/input"
ANSWER_URL = PROBLEM_URL + "/answer"

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
INPUT_FILE_NAME = "input_{}.txt"
ANSWER_FILE_NAME = "answer_{}_{}.txt"

HEADERS = {"User-Agent": "github.com/andrewzwicky/puzzles"}


def get_input_save_location(day):
    return ROOT_DIR.joinpath(INPUT_FILE_NAME.format(day))


def get_answer_save_location(day, level):
    return ROOT_DIR.joinpath(ANSWER_FILE_NAME.format(day, level))


def get_raw_input(day):
    try:
        with open(get_input_save_location(day), "r", encoding="utf8") as input_file:
            raw_text = input_file.read()
    except FileNotFoundError:
        input_response = requests.get(
            INPUT_URL.format(day), cookies={"session": SESSION}, timeout=10
        )

        raw_text = input_response.text

        with open(get_input_save_location(day), "w", encoding="utf8") as input_file:
            input_file.write(raw_text)

    return raw_text


def parse_problem_input(raw_text):
    return raw_text.rstrip().split("\n")


def get_problem_input(day):
    raw_text = get_raw_input(day)
    cleaned_data = parse_problem_input(raw_text)

    return raw_text, cleaned_data


def submit_answer(day, level, answer):
    if answer is None:
        return False

    print(f"Day {day} - Part {level}")
    print(answer)

    try:
        with open(
            get_answer_save_location(day, level), "r", encoding="utf8"
        ) as input_file:
            cached_answer = input_file.read().strip()
            correct = str(answer) ==  cached_answer
            print(f"{cached_answer} (cached)")


    except FileNotFoundError:
        answer_response = requests.post(
            url=ANSWER_URL.format(day),
            cookies={"session": SESSION},
            data={"level": level, "answer": answer},
            headers=HEADERS,
            timeout=10,
        )

        answer_soup = BeautifulSoup(answer_response.text, "html.parser")

        message = answer_soup.article.text
        print(message)
        correct = "That's the right answer" in message
        if correct:
            with open(
                get_answer_save_location(day, level), "w", encoding="utf8"
            ) as input_file:
                input_file.write(str(answer))

    if correct:
        print("✔️")
    else:
        print("❌")
    return correct


def neighbors(
    arr: np.array,
    index,
    center=True,
    diagonals=True,
    upper_left=True,
    bottom_right=True,
):
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

        if upper_left is False:
            where = np.where((including[0, :] <= row) & (including[1, :] <= col))
            mask[
                :,
                np.squeeze(where),
            ] = False

        if bottom_right is False:
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
