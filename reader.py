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

    @staticmethod
    def discrete_compact_rank(data: list[Any]) -> list[int]:
        unique_data = sorted(set(data))
        data_map = {value: index for index, value in enumerate(unique_data, 1)}
        return [data_map[value] for value in data]

    @staticmethod
    def discrete_average_rank(data: list[Any]) -> list[float]:
        unique_data = sorted(set(data))

        occurrence_count = {value: 0 for value in unique_data}
        for value in data:
            occurrence_count[value] += 1

        data_map = {}
        cumulative_rank = 0
        for value in unique_data:
            count = occurrence_count[value]
            average_rank = (cumulative_rank + 1 + cumulative_rank + count) / 2
            data_map[value] = average_rank
            cumulative_rank += count

        return [data_map[value] for value in data]

    @staticmethod
    def calc_pearson(x: list[float], y: list[float]) -> float:
        ax = sum(x) / len(x)
        ay = sum(y) / len(y)
        xx = [xi - ax for xi in x]
        yy = [yi - ay for yi in y]
        sx = math.sqrt(sum(xi * xi for xi in xx))
        sy = math.sqrt(sum(yi * yi for yi in yy))
        return sum(xx[i] * yy[i] for i in range(len(x))) / (sx * sy)

    @staticmethod
    def calc_spearman(x: list[float], y: list[float]) -> float:
        rx = Data.discrete_average_rank(x)
        ry = Data.discrete_average_rank(y)
        return Data.calc_pearson(rx, ry)

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

        pearson_corr = self.calc_pearson(contest_a_scores, contest_b_scores)
        spearman_corr = self.calc_spearman(contest_a_scores, contest_b_scores)

        plt.figtext(0.14, 0.86, f"Pearson   相关系数: {pearson_corr:.4f}", fontsize=12)
        plt.figtext(0.14, 0.84, f"Spearman  相关系数: {spearman_corr:.4f}", fontsize=12)
        plt.show()


if __name__ == "__main__":
    try:
        data = Data()
    except FileNotFoundError:
        print("请先初始化子模块：")
        print("  git submodule update --init --recursive")
        print("若已经初始化子模块，运行 OIerDb-data-generator 生成数据：")
        print("  cd OIerDb-data-generator")
        print("  python main.py")
        print("可能需要安装依赖，请参阅子项目的 README.md 文件。")
        print("完成后回到本项目根目录重新运行此脚本。")
        exit(1)
    else:
        data.compare_contests("CSP2025提高", "NOIP2025")
