"""
scripts/clean_data.py
---------------------
Reads raw CSVs from /data/raw, cleans them using the shared data_cleaner module,
and outputs cleaned files into /data/cleaned.
"""

import pandas as pd
from pathlib import Path
from modules.data_cleaner import clean_dataframe


def clean_all_raw():
    raw_dir = Path("data/raw")
    cleaned_dir = Path("data/cleaned")
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    for file in raw_dir.glob("*.csv"):
        print(f"Cleaning {file.name}...")
        df = pd.read_csv(file)
        cleaned = clean_dataframe(df)
        out_path = cleaned_dir / file.name
        cleaned.to_csv(out_path, index=False)
        print(f"Saved cleaned file -> {out_path}")


if __name__ == "__main__":
    clean_all_raw()
