"""
Dataset 4 Download Script: Full-Scale Waste Water Treatment Plant Data (Kaggle)
URL: https://www.kaggle.com/datasets/d4rklucif3r/full-scale-waste-water-treatment-plant-data

Uses kagglehub to download the dataset.
"""
import os
import kagglehub 
import shutil
from pathlib import Path

# Configuration
DATASET_DIR = Path(__file__).parent.parent / "backend" / "data" / "dataset4"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

def download_dataset4():
    """Download Full-Scale WWTP dataset from Kaggle using kagglehub."""
    print("=" * 60)
    print("Dataset 4: Full-Scale Waste Water Treatment Plant Data (Kaggle)")
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
            path = kh.download_dataset("d4rklucif3r/full-scale-waste-water-treatment-plant-data")
        except Exception as e1:
            try:
                # Try alternative method
                path = kagglehub.dataset_download("d4rklucif3r/full-scale-waste-water-treatment-plant-data")
            except Exception as e2:
                raise Exception(f"Both methods failed: {e1}, {e2}")
        
        print(f"✓ Dataset downloaded to: {path}")
        
        # Copy files to our dataset directory
        source_path = Path(path)
        files_copied = []
        
        if source_path.is_dir():
            # Copy all CSV files
            for file in source_path.glob("*.csv"):
                dest_file = DATASET_DIR / file.name
                shutil.copy2(file, dest_file)
                files_copied.append(dest_file.name)
                print(f"✓ Copied: {file.name}")
            
            # Also check for other data files
            for ext in ['.xlsx', '.xls', '.txt', '.data']:
                for file in source_path.glob(f"*{ext}"):
                    dest_file = DATASET_DIR / file.name
                    shutil.copy2(file, dest_file)
                    files_copied.append(dest_file.name)
                    print(f"✓ Copied: {file.name}")
        
        if files_copied:
            print(f"\n✓ Dataset ready at: {DATASET_DIR}")
            print(f"  Total files: {len(files_copied)}")
            print(f"  Files: {', '.join(files_copied[:5])}{'...' if len(files_copied) > 5 else ''}")
            
            # Identify main file (usually the largest CSV)
            csv_files = list(DATASET_DIR.glob("*.csv"))
            if csv_files:
                main_file = max(csv_files, key=lambda f: f.stat().st_size)
                print(f"  Main file (largest): {main_file.name}")
        else:
            print("\n⚠ No data files found in downloaded dataset.")
            
    except Exception as e:
        print(f"\n✗ Error downloading dataset: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Make sure kagglehub is installed: pip install kagglehub")
        print("  2. You may need Kaggle API credentials")
        print("  3. Visit: https://www.kaggle.com/datasets/d4rklucif3r/full-scale-waste-water-treatment-plant-data")
        print("  4. Download manually and place in:", DATASET_DIR)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    download_dataset4()

