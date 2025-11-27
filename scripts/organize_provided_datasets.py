"""
Script to organize and analyze the provided datasets.
Copies them to correct locations and verifies structure.
"""
import pandas as pd
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Source paths
DOWNLOADS_DIR = Path("C:/Users/soham/Downloads")
SOURCE_FILES = {
    "dataset2": DOWNLOADS_DIR / "water_potability.csv",
    "dataset4": DOWNLOADS_DIR / "Data-Melbourne_F.csv",
    "dataset4_fixed": DOWNLOADS_DIR / "archive (1)" / "Data-Melbourne_F_fixed.csv"
}

# Target directories
BASE_DIR = Path(__file__).parent.parent
TARGET_DIRS = {
    "dataset2": BASE_DIR / "backend" / "data" / "dataset2",
    "dataset4": BASE_DIR / "backend" / "data" / "dataset4"
}

def analyze_dataset(file_path: Path, dataset_name: str):
    """Analyze a dataset and return info."""
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return None
    
    try:
        df = pd.read_csv(file_path)
        info = {
            "file": file_path.name,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.to_dict(),
            "sample_data": df.head(3).to_dict()
        }
        logger.info(f"\n{dataset_name} Analysis:")
        logger.info(f"  Rows: {info['rows']}, Columns: {info['columns']}")
        logger.info(f"  Columns: {info['column_names']}")
        logger.info(f"  Missing values: {sum(info['missing_values'].values())} total")
        return info
    except Exception as e:
        logger.error(f"Error analyzing {file_path}: {e}")
        return None

def copy_and_organize():
    """Copy datasets to correct locations."""
    logger.info("=" * 60)
    logger.info("Organizing Provided Datasets")
    logger.info("=" * 60)
    
    # Create target directories
    for target_dir in TARGET_DIRS.values():
        target_dir.mkdir(parents=True, exist_ok=True)
    
    # Dataset 2: Water Potability
    logger.info("\n--- Dataset 2: Water Potability ---")
    if SOURCE_FILES["dataset2"].exists():
        info = analyze_dataset(SOURCE_FILES["dataset2"], "Dataset 2")
        if info:
            target_file = TARGET_DIRS["dataset2"] / "water_potability.csv"
            shutil.copy2(SOURCE_FILES["dataset2"], target_file)
            logger.info(f"✓ Copied to: {target_file}")
    else:
        logger.warning("Dataset 2 source file not found")
    
    # Dataset 4: Melbourne WWTP
    logger.info("\n--- Dataset 4: Melbourne WWTP ---")
    # Try fixed version first, then original
    dataset4_source = None
    if SOURCE_FILES["dataset4_fixed"].exists():
        dataset4_source = SOURCE_FILES["dataset4_fixed"]
        logger.info("Using fixed version (Data-Melbourne_F_fixed.csv)")
    elif SOURCE_FILES["dataset4"].exists():
        dataset4_source = SOURCE_FILES["dataset4"]
        logger.info("Using original version (Data-Melbourne_F.csv)")
    
    if dataset4_source:
        info = analyze_dataset(dataset4_source, "Dataset 4")
        if info:
            target_file = TARGET_DIRS["dataset4"] / "melbourne_wwtp.csv"
            shutil.copy2(dataset4_source, target_file)
            logger.info(f"✓ Copied to: {target_file}")
            
            # Also save a cleaned version if needed
            df = pd.read_csv(dataset4_source)
            # Remove index column if present
            if df.columns[0] == 'Unnamed: 0' or df.columns[0] == '':
                df = df.drop(df.columns[0], axis=1)
            cleaned_file = TARGET_DIRS["dataset4"] / "melbourne_wwtp_cleaned.csv"
            df.to_csv(cleaned_file, index=False)
            logger.info(f"✓ Created cleaned version: {cleaned_file}")
    else:
        logger.warning("Dataset 4 source file not found")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Summary")
    logger.info("=" * 60)
    
    for dataset_name, target_dir in TARGET_DIRS.items():
        csv_files = list(target_dir.glob("*.csv"))
        if csv_files:
            logger.info(f"{dataset_name}: {len(csv_files)} file(s) ready")
            for f in csv_files:
                logger.info(f"  - {f.name}")
        else:
            logger.warning(f"{dataset_name}: No files found")

if __name__ == "__main__":
    copy_and_organize()

