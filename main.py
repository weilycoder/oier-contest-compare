import csv
import json
import math

from typing import cast, Any, Literal

import numpy as np
import matplotlib.pyplot as plt

from utils import provinces


plt.rcParams["font.family"] = "SimHei"


class OIer:
    name: str
    gender: Literal[-1, 0, 1]
    enroll_middle: int
    records: dict[str, tuple[float, int, str]]  # contest_name -> (score, rank, province)

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
            province = provinces[int(contest[4])]
            contest_name = contests[contest_id]["name"]
            self.records[contest_name] = (score, rank, province)

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

    def get_oiers_by_contest(self, contest_name: str, provenance: set[str] | None = None) -> set[int]:
        return {
            i
            for i, oier in enumerate(self.oier_table)
            if oier.participated(contest_name) and (provenance is None or oier.records[contest_name][2] in provenance)
        }

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

    def compare_contests(
        self,
        contest_a: str,
        contest_b: str,
        provenance: set[str] | None = None,
        *,
        dpi: int = 80,
        alpha: float = 0.5,
        polyfit_degree: int | None = None,
        export_image: str | bool = False,
        show_plot: bool = True,
    ) -> None:
        contest_a_oiers = self.get_oiers_by_contest(contest_a, provenance)
        contest_b_oiers = self.get_oiers_by_contest(contest_b, provenance)
        target_oiers = contest_a_oiers & contest_b_oiers

        contest_a_scores = []
        contest_b_scores = []

        for oier_index in target_oiers:
            oier = self.oier_table[oier_index]
            score_a = oier.records[contest_a][0]
            score_b = oier.records[contest_b][0]
            contest_a_scores.append(score_a)
            contest_b_scores.append(score_b)

        plt.figure(figsize=(10, 10), dpi=dpi)
        plt.title(f"{contest_a} vs {contest_b} Score Comparison Scatter Plot", fontsize=12)
        plt.scatter(contest_a_scores, contest_b_scores, s=10, c="blue", alpha=alpha)

        if polyfit_degree is not None:
            p = np.poly1d(np.polyfit(contest_a_scores, contest_b_scores, polyfit_degree))
            x = np.arange(min(contest_a_scores), max(contest_a_scores), 1)
            plt.plot(x, p(x), color="red")

        plt.xlabel(contest_a)
        plt.ylabel(contest_b)

        pearson_corr = self.calc_pearson(contest_a_scores, contest_b_scores)
        spearman_corr = self.calc_spearman(contest_a_scores, contest_b_scores)

        plt.figtext(0.14, 0.86, f"Pearson  corr: {pearson_corr:.4f}", fontsize=12)
        plt.figtext(0.14, 0.84, f"Spearman corr: {spearman_corr:.4f}", fontsize=12)

        if export_image:
            if isinstance(export_image, str):
                filename = str(export_image)
            else:
                filename = f"{contest_a}_vs_{contest_b}.png"
            plt.savefig(filename, dpi=dpi)
        if show_plot:
            plt.show()


def main() -> None:
    import argparse

    def validate_alpha(value: str) -> float:
        try:
            alpha = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError("alpha is not a valid float")
        if not (0.0 <= alpha <= 1.0):
            raise argparse.ArgumentTypeError(f"alpha ({alpha}) is out of 0-1 range")
        return alpha

    def validate_polyfit(value: str) -> int:
        try:
            degree = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("polyfit degree is not a valid integer")
        if degree < 0:
            raise argparse.ArgumentTypeError(f"polyfit degree ({degree}) must be at least 0")
        return degree

    parser = argparse.ArgumentParser(description="Compare contest results of OIers.")
    parser.add_argument(
        "contest_a",
        type=str,
        help="Name of contest A",
    )
    parser.add_argument(
        "contest_b",
        type=str,
        help="Name of contest B",
    )
    parser.add_argument(
        "provenance",
        type=str,
        nargs="*",
        default=None,
        help="Provenance filter (e.g., provinces). If omitted, all provenances are included.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=80,
        help="DPI for the plot",
    )
    parser.add_argument(
        "--alpha",
        type=validate_alpha,
        default=0.5,
        help="Alpha transparency for scatter points",
    )
    parser.add_argument(
        "--polyfit",
        dest="degree",
        type=validate_polyfit,
        default=None,
        help="Degree of polynomial fit line to draw",
    )
    parser.add_argument(
        "--save",
        dest="filename",
        type=str,
        default=None,
        help="Path to save the plot image",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not display the plot",
    )

    args = parser.parse_args()

    try:
        data = Data()
    except FileNotFoundError:
        print(
            "Data files not found. "
            "Please ensure that the OIerDb-data-generator submodule has generated the necessary data files."
        )
        exit(1)
    else:
        data.compare_contests(
            args.contest_a,
            args.contest_b,
            provenance=set(args.provenance) if args.provenance else None,
            dpi=args.dpi,
            alpha=args.alpha,
            polyfit_degree=args.degree,
            export_image=args.filename if args.filename else False,
            show_plot=not args.no_show,
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", flush=True)
        exit(1)
