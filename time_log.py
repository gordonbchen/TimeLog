import csv
import pandas as pd

from argparse import ArgumentParser, Namespace
from pathlib import Path
from datetime import datetime


def add_entry(args: Namespace) -> None:
    """Add a time log entry."""
    csv_file = Path(args.filename)

    if not csv_file.exists():
        create_time_log(csv_file)

    date = datetime.now().strftime(r"%m/%d/%Y")

    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, args.desc, args.mins])


def create_time_log(csv_file: Path) -> None:
    """Create a csv file for the time log."""
    col_names = ["date", "desc", "mins"]

    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(col_names)


def show_total_time(args: Namespace) -> None:
    """Show total logged time."""
    time_log = pd.read_csv(args.filename)

    mins = time_log["mins"]
    total_mins = mins.sum()
    print(f"Total time: {total_mins // 60} hrs {total_mins % 60} mins")


if __name__ == "__main__":
    # Create arg parsers.
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        help="Time log csv filename",
        default="time_log.csv",
        required=False
    )

    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("desc", help="Activity description")
    add_parser.add_argument("mins", help="Minutes spent on activity")
    add_parser.set_defaults(func=add_entry)

    show_parser = subparsers.add_parser("show")
    show_parser.set_defaults(func=show_total_time)

    # Parse args and call funcs.
    args = parser.parse_args()
    args.func(args)
