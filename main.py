from data import Data
from comparison import compare_contests


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
        compare_contests(
            data,
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
