"""
Dataset 2 Download Script: Water Potability (Kaggle)
URL: https://www.kaggle.com/datasets/adityakadiwal/water-potability

Uses kagglehub to download the dataset.
"""
import os
import kagglehub
import shutil
from pathlib import Path

# Configuration
DATASET_DIR = Path(__file__).parent.parent / "backend" / "data" / "dataset2"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

def download_dataset2():
    """Download Water Potability dataset from Kaggle using kagglehub."""
    print("=" * 60)
    print("Dataset 2: Water Potability (Kaggle)")
    print("=" * 60)
    
    try:
        print("\nDownloading dataset using kagglehub...")
        print("This may take a few minutes...")
        
        # Download latest version using kagglehub
        # Note: kagglehub API may require authentication
        # Alternative: Use kaggle API directly or manual download
        import kagglehub.kagglehub as kh
        try:
            # Try the kagglehub module
            path = kh.download_dataset("adityakadiwal/water-potability")
        except Exception as e1:
            try:
                # Try alternative method
                path = kagglehub.dataset_download("adityakadiwal/water-potability")
            except Exception as e2:
                raise Exception(f"Both methods failed: {e1}, {e2}")
        
        print(f"✓ Dataset downloaded to: {path}")
        
        # Copy files to our dataset directory
        source_path = Path(path)
        files_copied = []
        
        if source_path.is_dir():
            for file in source_path.glob("*.csv"):
                dest_file = DATASET_DIR / file.name
                shutil.copy2(file, dest_file)
                files_copied.append(dest_file.name)
                print(f"✓ Copied: {file.name}")
        
        if files_copied:
            print(f"\n✓ Dataset ready at: {DATASET_DIR}")
            print(f"  Files: {', '.join(files_copied)}")
            
            # Validate by checking if water_potability.csv exists
            main_file = DATASET_DIR / "water_potability.csv"
            if not main_file.exists():
                # Look for any CSV file
                csv_files = list(DATASET_DIR.glob("*.csv"))
                if csv_files:
                    main_file = csv_files[0]
                    print(f"  Main file: {main_file.name}")
        else:
            print("\n⚠ No CSV files found in downloaded dataset.")
            
    except Exception as e:
        print(f"\n✗ Error downloading dataset: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Make sure kagglehub is installed: pip install kagglehub")
        print("  2. You may need Kaggle API credentials")
        print("  3. Visit: https://www.kaggle.com/datasets/adityakadiwal/water-potability")
        print("  4. Download manually and place in:", DATASET_DIR)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    download_dataset2()

