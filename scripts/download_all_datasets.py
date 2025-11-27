"""
Master script to download all datasets.
Runs all individual dataset download scripts sequentially.
"""
import subprocess
import sys
from pathlib import Path

def run_script(script_name):
    """Run a dataset download script."""
    script_path = Path(__file__).parent / script_name
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ {script_name} completed successfully")
        else:
            print(f"⚠ {script_name} completed with warnings")
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error running {script_name}: {str(e)}")
        return False

def main():
    """Download all datasets."""
    print("=" * 60)
    print("SIH WATER AI - Download All Datasets")
    print("=" * 60)
    
    scripts = [
        "download_dataset1.py",
        "download_dataset2.py",
        "download_dataset3.py",
        "download_dataset4.py"
    ]
    
    results = []
    for script in scripts:
        success = run_script(script)
        results.append((script, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    
    for script, success in results:
        status = "✓ Success" if success else "⚠ Check manually"
        print(f"{script}: {status}")
    
    print("\n" + "=" * 60)
    print("Note: Dataset 3 (UCI) requires manual download.")
    print("Please follow instructions in download_dataset3.py")
    print("=" * 60)

if __name__ == "__main__":
    main()

