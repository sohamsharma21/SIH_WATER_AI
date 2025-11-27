"""
Dataset 3 Download Script: UCI Water Treatment Plant
URL: https://archive.ics.uci.edu/ml/datasets/water+treatment+plant

NOTE: This dataset requires manual download.
Place the downloaded files in: backend/data/dataset3/
"""
import os
from pathlib import Path

# Configuration
DATASET_DIR = Path(__file__).parent.parent / "backend" / "data" / "dataset3"
DATASET_DIR.mkdir(parents=True, exist_ok=True)

def download_dataset3():
    """Guide manual download of UCI Water Treatment Plant dataset."""
    print("=" * 60)
    print("Dataset 3: UCI Water Treatment Plant")
    print("=" * 60)
    
    dataset_url = "https://archive.ics.uci.edu/ml/datasets/water+treatment+plant"
    
    print(f"\nDataset URL: {dataset_url}")
    print("\n⚠ This dataset requires MANUAL DOWNLOAD")
    print("\nInstructions:")
    print(f"  1. Visit: {dataset_url}")
    print("  2. Click on 'Data Folder' to access dataset files")
    print("  3. Download the dataset files (typically .data or .csv format)")
    print(f"  4. Place downloaded files in: {DATASET_DIR}")
    print("  5. Rename main file to: water_treatment_plant.csv (or keep original name)")
    
    # Create instructions file
    readme_file = DATASET_DIR / "README.txt"
    with open(readme_file, 'w') as f:
        f.write(f"""UCI Water Treatment Plant Dataset

Dataset Information:
- URL: {dataset_url}
- Purpose: Contamination severity assessment and treatment class prediction
- Features: Multiple sensor readings and treatment parameters

Download Instructions:
1. Visit the UCI ML Repository link above
2. Navigate to the "Data Folder"
3. Download the dataset files
4. Place them in this directory
5. Expected file names may include:
   - water-treatment.data
   - water-treatment.names
   - or similar variations

Expected Features:
- Water quality parameters
- Treatment process variables
- Classification labels for treatment stages

Once files are placed here, the ML pipeline will automatically detect and process them.
""")
    
    print(f"\n✓ Created README.txt at: {readme_file}")
    
    # Check if dataset already exists
    existing_files = list(DATASET_DIR.glob("*"))
    if existing_files:
        print(f"\n✓ Found existing files in dataset directory:")
        for file in existing_files:
            if file.name != "README.txt":
                print(f"  - {file.name}")
    else:
        print("\n⚠ No dataset files found yet. Please download and add them.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    download_dataset3()

