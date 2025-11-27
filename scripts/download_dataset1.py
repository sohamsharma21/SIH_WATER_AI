"""
Dataset 1 Download Script: NYC DEP Wastewater Treatment Plants
URL: https://www.uvm.edu/femc/data/archive/project/NYC_DEP_Wastewater_Treatment_Plants

This script attempts to download or guide manual download of NYC DEP dataset.
Since the dataset may require manual access, this script provides instructions.
"""
import os
import requests
import pandas as pd
from pathlib import Path

# Configuration
DATASET_DIR = Path(__file__).parent.parent / "backend" / "data" / "dataset1"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

def download_dataset1():
    """Download or guide download of NYC DEP Wastewater dataset."""
    print("=" * 60)
    print("Dataset 1: NYC DEP Wastewater Treatment Plants")
    print("=" * 60)
    
    # The dataset URL might require manual download
    dataset_url = "https://www.uvm.edu/femc/data/archive/project/NYC_DEP_Wastewater_Treatment_Plants"
    
    print(f"\nDataset URL: {dataset_url}")
    print("\nAttempting to fetch dataset...")
    
    try:
        # Try to download if there's a direct CSV link
        csv_links = [
            f"{dataset_url}/NYC_DEP_Wastewater_Plants.csv",
            f"{dataset_url}/data.csv",
            f"{dataset_url}/wastewater_data.csv"
        ]
        
        downloaded = False
        for link in csv_links:
            try:
                response = requests.get(link, timeout=30)
                if response.status_code == 200:
                    output_path = DATASET_DIR / "nyc_dep_wastewater.csv"
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ Downloaded dataset to: {output_path}")
                    
                    # Validate the CSV
                    df = pd.read_csv(output_path)
                    print(f"✓ Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
                    print(f"  Columns: {list(df.columns)[:10]}...")
                    downloaded = True
                    break
            except:
                continue
        
        if not downloaded:
            print("\n⚠ Direct download not available.")
            print("\nPlease manually download the dataset:")
            print(f"  1. Visit: {dataset_url}")
            print(f"  2. Download the CSV file(s)")
            print(f"  3. Place them in: {DATASET_DIR}")
            print(f"  4. Rename the main file to: nyc_dep_wastewater.csv")
            
            # Create a sample structure file
            sample_file = DATASET_DIR / "README.txt"
            with open(sample_file, 'w') as f:
                f.write(f"""NYC DEP Wastewater Treatment Plants Dataset

Expected Parameters (18+):
- Ammonia (NH3)
- Nitrate (NO3)
- Phosphorus (P)
- BOD (Biological Oxygen Demand)
- COD (Chemical Oxygen Demand)
- pH
- Temperature
- Dissolved Oxygen
- Total Suspended Solids
- And more...

Place the main CSV file here with name: nyc_dep_wastewater.csv
""")
            print(f"\n✓ Created README.txt at {sample_file}")
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nPlease manually download the dataset and place it in:")
        print(f"   {DATASET_DIR}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    download_dataset1()

