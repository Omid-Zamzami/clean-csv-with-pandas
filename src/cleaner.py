import argparse
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


def parse_argument(arg=None):
    parser = argparse.ArgumentParser(description="CLI tool for fetching messy dataset file name.")

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="File name of the messy dataset in need for cleaning"
    )

    return parser.parse_args(arg)


def load_data(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"file in {file_path} was not found!")

    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_path)
    elif suffix in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    elif suffix == ".json":
        return pd.read_json(file_path)
    else:
        raise ValueError(f"{suffix} is not supported. Allowed formats: csv, xlsx, json.")


def cleaner():
    arg = parse_argument()

    file_path = BASE_DIR / "data" / f"{arg.file}"

    df = load_data(file_path)

    print(df.head(10))


if __name__ == "__main__":
    cleaner()