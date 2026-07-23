import csv
import json

from typing import cast, Literal

from utils import provinces
from plot import render_contest_comparison_plot


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

        render_contest_comparison_plot(
            contest_a_scores,
            contest_b_scores,
            contest_a,
            contest_b,
            dpi=dpi,
            alpha=alpha,
            polyfit_degree=polyfit_degree,
            export_image=export_image,
            show_plot=show_plot,
        )
