import numpy as np
import matplotlib.pyplot as plt

from calcs import calc_pearson, calc_spearman


plt.rcParams["font.family"] = "SimHei"


def render_contest_comparison_plot(
    contest_a_scores: list[float],
    contest_b_scores: list[float],
    contest_a: str,
    contest_b: str,
    *,
    dpi: int,
    alpha: float,
    polyfit_degree: int | None,
    export_image: str | bool,
    show_plot: bool,
) -> None:
    plt.figure(figsize=(10, 10), dpi=dpi)
    plt.title(f"{contest_a} vs {contest_b} Score Comparison Scatter Plot", fontsize=12)
    plt.scatter(contest_a_scores, contest_b_scores, s=10, c="blue", alpha=alpha)

    if polyfit_degree is not None:
        p = np.poly1d(np.polyfit(contest_a_scores, contest_b_scores, polyfit_degree))
        x = np.arange(min(contest_a_scores), max(contest_a_scores), 1)
        plt.plot(x, p(x), color="red")

    plt.xlabel(contest_a)
    plt.ylabel(contest_b)

    pearson_corr = calc_pearson(contest_a_scores, contest_b_scores)
    spearman_corr = calc_spearman(contest_a_scores, contest_b_scores)

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
