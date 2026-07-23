from data import Data
from plot import render_contest_comparison_plot


def compare_contests(
    data: "Data",
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
    contest_a_oiers = data.get_oiers_by_contest(contest_a, provenance)
    contest_b_oiers = data.get_oiers_by_contest(contest_b, provenance)
    target_oiers = contest_a_oiers & contest_b_oiers

    contest_a_scores = []
    contest_b_scores = []

    for oier_index in target_oiers:
        oier = data.oier_table[oier_index]
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
