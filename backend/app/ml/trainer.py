"""
Model Training Functions for SIH WATER AI
Handles training of all 4 ML models
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import logging

from .pipeline import UnifiedMLPipeline
from ..config import settings

logger = logging.getLogger(__name__)


def detect_target_column(df: pd.DataFrame, dataset_name: str) -> str:
    """
    Automatically detect or infer target column based on dataset.
    
    Args:
        df: DataFrame
        dataset_name: Name of the dataset
        
    Returns:
        Target column name
    """
    # Common target column names
    target_candidates = [
        'target', 'label', 'y', 'class', 'quality',
        'potability', 'water_potability', 'quality_score',
        'contamination', 'treatment_class', 'bod', 'cod',
        'nitrogen_removal', 'efficiency'
    ]
    
    # Check for exact matches
    for col in target_candidates:
        if col in df.columns:
            return col
    
    # Dataset-specific logic
    if 'dataset1' in dataset_name.lower() or 'nyc' in dataset_name.lower():
        # NYC DEP - predict nitrogen removal or quality
        nitrogen_cols = [c for c in df.columns if 'nitrogen' in c.lower()]
        if nitrogen_cols:
            return nitrogen_cols[0]
        return 'quality_score' if 'quality_score' in df.columns else df.columns[-1]
    
    elif 'dataset2' in dataset_name.lower() or 'potability' in dataset_name.lower():
        # Water Potability
        return 'Potability' if 'Potability' in df.columns else 'potability'
    
    elif 'dataset3' in dataset_name.lower() or 'uci' in dataset_name.lower():
        # UCI - contamination or treatment class
        class_cols = [c for c in df.columns if 'class' in c.lower()]
        if class_cols:
            return class_cols[0]
        return 'contamination_index' if 'contamination_index' in df.columns else df.columns[-1]
    
    elif 'dataset4' in dataset_name.lower() or 'wwtp' in dataset_name.lower() or 'melbourne' in dataset_name.lower():
        # WWTP - BOD/COD prediction
        # Check for full names first
        if 'Biological Oxygen Demand' in df.columns:
            return 'Biological Oxygen Demand'
        elif 'Chemical Oxygen Demand' in df.columns:
            return 'Chemical Oxygen Demand'
        # Check for short names
        bod_cols = [c for c in df.columns if 'biological oxygen demand' in c.lower() or c.lower() == 'bod']
        if bod_cols:
            return bod_cols[0]
        cod_cols = [c for c in df.columns if 'chemical oxygen demand' in c.lower() or c.lower() == 'cod']
        if cod_cols:
            return cod_cols[0]
        return df.columns[-1]
    
    # Default: last column
    return df.columns[-1]


def train_on_csv(dataset_name: str, csv_path: Path, target_column: Optional[str] = None) -> Dict[str, Any]:
    """
    Train a model on a CSV file.
    
    Args:
        dataset_name: Name/identifier of the dataset
        csv_path: Path to CSV file
        target_column: Name of target column (auto-detected if None)
        
    Returns:
        Dictionary with training results and model metadata
    """
    logger.info(f"Training model for dataset: {dataset_name}")
    logger.info(f"CSV path: {csv_path}")
    
    # Load data
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                logger.info(f"Loaded CSV with encoding: {encoding}")
                break
            except:
                continue
        
        if df is None:
            raise ValueError("Could not read CSV with any encoding")
            
    except Exception as e:
        raise ValueError(f"Error loading CSV: {str(e)}")
    
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Columns: {list(df.columns)[:10]}...")
    
    # Detect target column
    if target_column is None:
        target_column = detect_target_column(df, dataset_name)
        logger.info(f"Auto-detected target column: {target_column}")
    
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")
    
    # Determine model type
    # If target is numeric with many unique values -> regressor
    # Otherwise -> classifier
    target_values = df[target_column].dropna()
    n_unique = target_values.nunique()
    is_numeric = pd.api.types.is_numeric_dtype(target_values)
    
    if is_numeric and n_unique > 10:
        model_type = "regressor"
    else:
        model_type = "classifier"
    
    logger.info(f"Model type: {model_type}")
    
    # Create and train pipeline
    pipeline = UnifiedMLPipeline(model_type=model_type)
    
    try:
        X, y = pipeline.prepare_data(df, target_column)
        
        # Train with minimal CV for speed
        metrics = pipeline.train(X, y, cv=2, n_jobs=1)  # Minimal CV for fastest training
        
        # Save model
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{dataset_name}_model_v{timestamp}.pkl"
        model_path = Path(settings.MODEL_DIR) / model_filename
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        pipeline.save(model_path)
        
        # Prepare metadata for Supabase
        model_metadata = {
            'dataset_name': dataset_name,
            'model_name': model_filename,
            'model_version': timestamp,
            'model_path': str(model_path),
            'model_type': model_type,
            'training_date': datetime.now().isoformat(),
            'accuracy': metrics.get('accuracy') or metrics.get('r2'),
            'f1_score': metrics.get('f1_score'),
            'r2_score': metrics.get('r2'),
            'training_params': metrics.get('best_params', {}),
            'feature_columns': pipeline.feature_columns,
            'target_column': pipeline.target_column,
            'metrics': metrics
        }
        
        logger.info(f"Training complete. Model saved to: {model_path}")
        
        return model_metadata
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise


def train_all() -> Dict[str, Any]:
    """
    Train all 4 models sequentially.
    
    Returns:
        Dictionary with results for all models
    """
    results = {}
    datasets = {
        'dataset1': 'nyc_dep_wastewater',
        'dataset2': 'water_potability',
        'dataset3': 'water_treatment_plant',
        'dataset4': 'full_scale_wwtp'
    }
    
    data_dir = Path(settings.DATA_DIR)
    
    for dataset_key, dataset_prefix in datasets.items():
        dataset_dir = data_dir / dataset_key
        
        if not dataset_dir.exists():
            logger.warning(f"Dataset directory not found: {dataset_dir}")
            results[dataset_key] = {'status': 'skipped', 'reason': 'directory_not_found'}
            continue
        
        # Find CSV files
        csv_files = list(dataset_dir.glob("*.csv"))
        
        if not csv_files:
            logger.warning(f"No CSV files found in: {dataset_dir}")
            results[dataset_key] = {'status': 'skipped', 'reason': 'no_csv_files'}
            continue
        
        # Use the first/largest CSV file
        main_csv = max(csv_files, key=lambda f: f.stat().st_size)
        logger.info(f"Training {dataset_key} with file: {main_csv.name}")
        
        try:
            model_metadata = train_on_csv(dataset_key, main_csv)
            results[dataset_key] = {
                'status': 'success',
                'metadata': model_metadata
            }
        except Exception as e:
            logger.error(f"Error training {dataset_key}: {str(e)}")
            results[dataset_key] = {
                'status': 'error',
                'error': str(e)
            }
    
    return results

