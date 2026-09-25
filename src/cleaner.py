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


def remove_duplicate_rows(df: pd.DataFrame):
    return df.drop_duplicates()


def clean_missing_values(df: pd.DataFrame):
    df = df.dropna(subset=["Employee_ID"])

    if "Age" in df.columns:
        age_median = df["Age"].median()
        df["Age"] = df["Age"].fillna(age_median)

    if "Salary" in df.columns:
        salary_median = df["Salary"].median()
        df["Salary"] = df["Salary"].fillna(salary_median)

    excluded_columns = ["Employee_ID", "Age", "Salary", "Join_Date", "Phone"]

    for column in df.columns:
        if column not in excluded_columns:
            df[column] = df[column].fillna("Unknown")

    return df

def clean_data_types(df: pd.DataFrame):
    if "Join_Date" in df.columns:
        df["Join_Date"] = pd.to_datetime(df["Join_Date"], errors="coerce")

    if "Age" in df.columns:
        df["Age"] = df["Age"].astype(int)

    return df


def cleaner():
    arg = parse_argument()

    file_path = BASE_DIR / "data" / f"{arg.file}"

    df = load_data(file_path=file_path)

    df = remove_duplicate_rows(df=df)

    df = clean_missing_values(df=df)

    df = clean_data_types(df=df)

    print(df.head(10))
    print(df.info())


if __name__ == "__main__":
    cleaner()