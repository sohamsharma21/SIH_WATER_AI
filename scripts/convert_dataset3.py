"""
Utility script to convert the UCI water-treatment .data file into CSV.
"""
import csv
from pathlib import Path


def convert_dataset():
    """Convert raw .data file to CSV for training."""
    data_dir = Path(__file__).parent.parent / "backend" / "data" / "dataset3"
    src = data_dir / "water-treatment.data"
    dst = data_dir / "water_treatment_plant.csv"

    if not src.exists():
        raise FileNotFoundError(f"Source data file not found: {src}")

    rows = []
    max_cols = 0
    with src.open("r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        for raw_row in reader:
            if not raw_row:
                continue
            row = [value.strip() if value.strip() != "?" else "" for value in raw_row]
            rows.append(row)
            max_cols = max(max_cols, len(row))

    if not rows:
        raise ValueError("No rows found in source dataset")

    # Pad rows to equal length and build header names
    for row in rows:
        if len(row) < max_cols:
            row.extend([""] * (max_cols - len(row)))
    header = [f"feature_{i}" for i in range(max_cols)]

    with dst.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Converted {src.name} -> {dst.name} with {len(rows)} rows and {max_cols} columns")


if __name__ == "__main__":
    convert_dataset()

