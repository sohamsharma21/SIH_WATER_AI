"""
Train model on Dataset 3 (UCI Water Treatment Plant)
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

import logging
from app.ml.trainer import train_on_csv
from app.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Train model on dataset3"""
    logger.info("=" * 60)
    logger.info("Training Model for Dataset 3 (UCI Water Treatment Plant)")
    logger.info("=" * 60)
    
    # Dataset configuration
    dataset_name = "dataset3"
    csv_path = Path(settings.DATA_DIR) / "dataset3" / "water_treatment_plant.csv"
    
    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        return
    
    logger.info(f"Training on CSV: {csv_path}")
    
    try:
        # Train the model (target column will be auto-detected)
        result = train_on_csv(dataset_name, csv_path, target_column=None)
        
        logger.info("=" * 60)
        logger.info("Training Complete!")
        logger.info("=" * 60)
        logger.info(f"Model saved: {result['model_path']}")
        logger.info(f"Model type: {result['model_type']}")
        logger.info(f"Metrics: {result.get('metrics', {})}")
        logger.info(f"Target column: {result['target_column']}")
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()

