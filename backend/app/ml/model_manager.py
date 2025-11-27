"""
Model Management and Selection
Handles loading models and selecting appropriate model for predictions
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import joblib
from datetime import datetime

from .pipeline import UnifiedMLPipeline
from ..config import settings

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages ML models and handles model selection."""
    
    def __init__(self):
        """Initialize model manager."""
        self.models: Dict[str, UnifiedMLPipeline] = {}
        self.model_metadata: Dict[str, Dict[str, Any]] = {}
        self._load_all_models()
    
    def _load_all_models(self) -> None:
        """Load all available models from the models directory."""
        model_dir = Path(settings.MODEL_DIR)
        
        if not model_dir.exists():
            logger.warning(f"Model directory not found: {model_dir}")
            return
        
        # Find all model files (exclude .meta.pkl files)
        model_files = [f for f in model_dir.glob("*_model_v*.pkl") if not str(f).endswith(".meta.pkl")]
        
        for model_file in model_files:
            try:
                # Extract dataset name from filename
                # Format: {dataset_name}_model_v{timestamp}.pkl
                parts = model_file.stem.split('_model_v')
                if len(parts) == 2:
                    dataset_name = parts[0]
                    
                    # Load model
                    pipeline = UnifiedMLPipeline.load(model_file)
                    
                    # Store model
                    self.models[dataset_name] = pipeline
                    
                    # Load metadata
                    metadata_file = model_file.with_suffix('.meta.pkl')
                    if metadata_file.exists():
                        metadata = joblib.load(metadata_file)
                        self.model_metadata[dataset_name] = metadata
                    
                    logger.info(f"Loaded model: {dataset_name}")
                    
            except Exception as e:
                logger.error(f"Error loading model {model_file}: {str(e)}")
        
        logger.info(f"Loaded {len(self.models)} models")
    
    def model_selector(self, features: Dict[str, float]) -> Optional[str]:
        """
        Auto-select appropriate model based on available features.
        
        Args:
            features: Dictionary of feature names and values
            
        Returns:
            Dataset name of selected model, or None
        """
        feature_names = set(features.keys())
        
        # Score each model based on feature overlap
        scores = {}
        
        for dataset_name, pipeline in self.models.items():
            if pipeline.feature_columns is None:
                continue
            
            model_features = set(pipeline.feature_columns)
            overlap = len(feature_names.intersection(model_features))
            overlap_ratio = overlap / len(model_features) if len(model_features) > 0 else 0
            
            scores[dataset_name] = {
                'overlap': overlap,
                'ratio': overlap_ratio,
                'total_features': len(model_features)
            }
        
        if not scores:
            return None
        
        # Select model with highest overlap ratio
        best_model = max(scores.items(), key=lambda x: x[1]['ratio'])
        
        if best_model[1]['ratio'] > 0.5:  # At least 50% feature overlap
            logger.info(f"Selected model: {best_model[0]} (overlap: {best_model[1]['ratio']:.2%})")
            return best_model[0]
        
        logger.warning("No suitable model found with sufficient feature overlap")
        return None
    
    def predict(self, dataset_name: str, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Make prediction using specified model.
        
        Args:
            dataset_name: Name of dataset/model
            features: Dictionary of feature values
            
        Returns:
            Prediction results
        """
        if dataset_name not in self.models:
            raise ValueError(f"Model '{dataset_name}' not found")
        
        pipeline = self.models[dataset_name]
        
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Ensure all required features are present
        missing_features = set(pipeline.feature_columns) - set(features.keys())
        if missing_features:
            # Fill missing features with median/default values
            for feat in missing_features:
                feature_df[feat] = 0.0  # Default value
            logger.warning(f"Missing features filled with defaults: {missing_features}")
        
        # Select only required features in correct order
        feature_df = feature_df[pipeline.feature_columns]
        
        # Make prediction
        prediction = pipeline.predict(feature_df)[0]
        
        result = {
            'prediction': float(prediction) if isinstance(prediction, (int, float, np.number)) else prediction,
            'model_name': dataset_name,
            'features_used': pipeline.feature_columns
        }
        
        # Add probabilities for classifiers
        if pipeline.model_type == "classifier":
            try:
                probabilities = pipeline.predict_proba(feature_df)[0]
                result['probabilities'] = probabilities.tolist()
                result['confidence'] = float(np.max(probabilities))
            except:
                pass
        
        return result
    
    def ensemble_predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Make ensemble prediction using multiple models.
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Ensemble prediction results
        """
        predictions = []
        weights = []
        
        for dataset_name, pipeline in self.models.items():
            try:
                result = self.predict(dataset_name, features)
                predictions.append(result['prediction'])
                
                # Weight by confidence or model accuracy
                confidence = result.get('confidence', 0.5)
                weights.append(confidence)
                
            except Exception as e:
                logger.warning(f"Error in ensemble prediction for {dataset_name}: {str(e)}")
                continue
        
        if not predictions:
            raise ValueError("No models could make predictions")
        
        # Weighted average
        weights = np.array(weights)
        weights = weights / weights.sum()  # Normalize
        
        ensemble_pred = np.average(predictions, weights=weights)
        
        return {
            'prediction': float(ensemble_pred),
            'individual_predictions': {name: self.predict(name, features)['prediction'] 
                                     for name in self.models.keys()},
            'weights': weights.tolist(),
            'method': 'weighted_average'
        }
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models."""
        models_info = []
        
        for dataset_name, pipeline in self.models.items():
            metadata = self.model_metadata.get(dataset_name, {})
            
            info = {
                'dataset_name': dataset_name,
                'model_type': pipeline.model_type,
                'feature_columns': pipeline.feature_columns,
                'target_column': pipeline.target_column,
                'metadata': metadata
            }
            models_info.append(info)
        
        return models_info


# Global model manager instance
_model_manager: Optional[ModelManager] = None


def get_model_manager() -> ModelManager:
    """Get or create global model manager instance."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager

