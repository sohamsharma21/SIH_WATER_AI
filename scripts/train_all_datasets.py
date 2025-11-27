"""
Script to train all available datasets.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.ml.trainer import train_on_csv
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dataset configurations
DATASETS = {
    "dataset2": {
        "name": "dataset2",
        "path": Path(__file__).parent.parent / "backend" / "data" / "dataset2" / "water_potability.csv",
        "target": "Potability"
    },
    "dataset3": {
        "name": "dataset3",
        "path": Path(__file__).parent.parent / "backend" / "data" / "dataset3" / "water_treatment_plant.csv",
        "target": None  # Auto-detect
    },
    "dataset4": {
        "name": "dataset4",
        "path": Path(__file__).parent.parent / "backend" / "data" / "dataset4" / "melbourne_wwtp_cleaned.csv",
        "target": None  # Auto-detect (should be BOD or COD)
    }
}

def train_all_available():
    """Train all available datasets."""
    logger.info("=" * 60)
    logger.info("SIH WATER AI - Training All Available Models")
    logger.info("=" * 60)
    
    results = {}
    
    for dataset_id, config in DATASETS.items():
        if not config["path"].exists():
            logger.warning(f"⚠ {dataset_id}: File not found at {config['path']}")
            continue
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Training: {dataset_id}")
        logger.info(f"File: {config['path']}")
        logger.info(f"{'='*60}")
        
        try:
            result = train_on_csv(
                dataset_name=config["name"],
                csv_path=config["path"],
                target_column=config["target"]
            )
            results[dataset_id] = {
                "status": "success",
                "model_path": result.get("model_path"),
                "metrics": result.get("metrics", {}),
                "accuracy": result.get("accuracy"),
                "r2_score": result.get("r2_score")
            }
            logger.info(f"✓ {dataset_id} training completed successfully")
            logger.info(f"  Model: {result.get('model_name')}")
            logger.info(f"  Accuracy/R2: {result.get('accuracy') or result.get('r2_score')}")
            
        except Exception as e:
            logger.error(f"✗ {dataset_id} training failed: {str(e)}")
            results[dataset_id] = {
                "status": "failed",
                "error": str(e)
            }
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Training Summary")
    logger.info("=" * 60)
    
    for dataset_id, result in results.items():
        if result["status"] == "success":
            logger.info(f"✓ {dataset_id}: SUCCESS")
            logger.info(f"  Model: {result.get('model_path', 'N/A')}")
            logger.info(f"  Metrics: {result.get('metrics', {})}")
        else:
            logger.error(f"✗ {dataset_id}: FAILED")
            logger.error(f"  Error: {result.get('error', 'Unknown error')}")
    
    return results

if __name__ == "__main__":
    train_all_available()

