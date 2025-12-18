import csv
import json
import math

from typing import cast, Any, Literal

import numpy as np
import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "SimHei"


class OIer:
    name: str
    gender: Literal[-1, 0, 1]
    enroll_middle: int
    records: dict[str, tuple[float, int]]

    def __init__(self, data: list[str], contests: list[dict]) -> None:
        # self.oierid = int(data[0])
        self.name = data[2]
        self.gender = cast(Literal[-1, 0, 1], int(data[3]))
        assert self.gender in (-1, 0, 1)
        self.enroll_middle = int(data[4])
        self.parse_records(data[-1], contests)

    def parse_records(self, raw_records: str, contests: list[dict]) -> None:
        self.records = {}

        for contest in map(lambda record: tuple(record.split(":")), raw_records.split("/")):
            contest_id = int(contest[0])
            score = float(contest[2]) if contest[2] != "" else float("nan")
            rank = int(contest[3]) if contest[3] != "" else -1
            contest_name = contests[contest_id]["name"]
            self.records[contest_name] = (score, rank)

    def participated(self, contest_name: str) -> bool:
        return contest_name in self.records


class Data:
    oier_table: list[OIer] = []

    def __init__(self) -> None:
        with open("OIerDb-data-generator/static/contests.json", "r", encoding="utf-8") as file:
            contests = json.load(file)

        with open("OIerDb-data-generator/dist/result.txt", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                self.oier_table.append(OIer(row, contests))

    def get_oiers_by_contest(self, contest_name: str) -> set[int]:
        return {i for i, oier in enumerate(self.oier_table) if oier.participated(contest_name)}

    def compare_contests(self, contest_a: str, contest_b: str) -> None:
        contest_a_oiers = self.get_oiers_by_contest(contest_a)
        contest_b_oiers = self.get_oiers_by_contest(contest_b)
        target_oiers = contest_a_oiers & contest_b_oiers

        if len(target_oiers) == 0:
            print(f"{contest_a} 与 {contest_b} 无重合选手")
            return

        # contest_a_ranks = []
        # contest_b_ranks = []
        contest_a_scores = []
        contest_b_scores = []

        for oier_index in target_oiers:
            oier = self.oier_table[oier_index]
            score_a, rank_a = oier.records[contest_a]
            score_b, rank_b = oier.records[contest_b]
            # contest_a_ranks.append(rank_a)
            # contest_b_ranks.append(rank_b)
            contest_a_scores.append(score_a)
            contest_b_scores.append(score_b)

        plt.figure(figsize=(10, 10), dpi=80)
        plt.title(f"{contest_a} 与 {contest_b} 成绩对比散点图")
        plt.scatter(contest_a_scores, contest_b_scores, s=10, c="blue", alpha=0.5)
        plt.xlabel(contest_a)
        plt.ylabel(contest_b)

        plt.show()


if __name__ == "__main__":
    data = Data()
    data.compare_contests("CSP2025提高", "NOIP2025")
