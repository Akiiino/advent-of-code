import pathlib
import re
import time

import requests

data_path = (pathlib.Path(__file__).parent / "../../data/").resolve()

COOKIE = open(data_path / "tokens.txt", "r").read().strip()

HEADERS = {"User-Agent": "My AOC parser v1.0", "From": "aoc@akiiino.me"}
INPUT_URL = "https://adventofcode.com/{}/day/{}/input"


def get_input(day, year=2022):
    input_path = data_path / str(year) / str(day) / "input[0].in"

    try:
        with open(input_path, "r") as input_file:
            data = input_file.read()

    except FileNotFoundError:
        data = requests.get(
            INPUT_URL.format(year, day), cookies={"session": COOKIE}, headers=HEADERS
        ).text

        input_path.parent.mkdir(parents=True, exist_ok=True)
        with open(input_path, "w") as input_file:
            input_file.write(data)

    return data.rstrip()


def check_answer(answer, day, level, year=2022):
    answer_path = data_path / str(year) / str(day) / f"input[0].out.{level}"
    answer = str(answer)

    try:
        with open(answer_path, "r") as answer_file:
            correct = answer_file.read().strip() == answer

    except FileNotFoundError:
        correct = submit(answer, day, level)

        if correct:
            answer_path.parent.mkdir(parents=True, exist_ok=True)
            with open(answer_path, "w") as answer_file:
                answer_file.write(answer + "\n")

    return correct
    

def submit(answer, day, level):
    url = f"https://adventofcode.com/2022/day/{day}/answer"
    answer = str(answer)

    resp = requests.post(
        url,
        data={"level": level, "answer": answer},
        cookies={"session": COOKIE},
        headers=HEADERS,
    )

    if "That's the right answer!" in resp.text:
        return True

    elif "You don't seem to be solving the right level" in resp.text:
        url = f"https://adventofcode.com/2022/day/{day}"
        resp = requests.get(url, cookies={"session": COOKIE}, headers=HEADERS)
        correct_answer = re.findall(
            r"Your puzzle answer was <code>(.*?)</code>", resp.text
        )[level - 1]
        return answer == correct_answer

    elif "You gave an answer too recently" in resp.text:
        waiting_time = re.findall(r"You have (\d+)?m? (\d+)s left to wait", resp.text)[0]
        if len(waiting_time) == 1:
            waiting_time = ["0"] + waiting_time
        waiting_time = int(waiting_time[-1] or "0") + 60 * int(waiting_time[-2])

        print(f"Waiting for {waiting_time} seconds")
        time.sleep(waiting_time + 5)
        return submit(answer, day, level)
    else:
        raise NotImplementedError("Unexpected response")
