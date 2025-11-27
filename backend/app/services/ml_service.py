"""
ML Service - Handles model predictions and management
"""
import logging
from typing import Dict, Any, Optional
from ..ml.model_manager import get_model_manager

logger = logging.getLogger(__name__)


class MLService:
    """Service for ML model operations."""
    
    def __init__(self):
        """Initialize ML service."""
        self.model_manager = get_model_manager()
    
    def predict(self, features: Dict[str, float], model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Make prediction using ML models.
        
        Args:
            features: Dictionary of feature values
            model_name: Optional specific model to use, otherwise auto-select
            
        Returns:
            Prediction results
            
        Raises:
            ValueError: If no model found or features invalid
        """
        try:
            if not features:
                raise ValueError("Features dictionary cannot be empty")
            
            # Treat 'auto' string the same as unspecified (None)
            if model_name is None or (isinstance(model_name, str) and model_name.strip().lower() == 'auto'):
                model_name = self.model_manager.model_selector(features)
                if model_name is None:
                    raise ValueError("No suitable model found for given features. Available models: " + 
                                   ", ".join(list(self.model_manager.models.keys())) if self.model_manager.models else "None")
            
            if model_name not in self.model_manager.models:
                raise ValueError(f"Model '{model_name}' not found. Available: " + 
                               ", ".join(list(self.model_manager.models.keys())))
            
            # Make prediction
            prediction_result = self.model_manager.predict(model_name, features)
            
            # Calculate quality score and contamination index from prediction
            # These are derived metrics based on the prediction
            prediction_value = prediction_result['prediction']
            model_type = self.model_manager.models[model_name].model_type
            
            # Convert prediction to quality score (0-100)
            if model_type == "classifier":
                # For classification: prediction is 0 or 1 (potability)
                # If prediction is 1 (potable), quality is high
                if prediction_value == 1 or prediction_value == 1.0:
                    quality_score = 85.0  # High quality for potable water
                    contamination_index = 15.0
                else:
                    quality_score = 30.0  # Low quality for non-potable
                    contamination_index = 70.0
                
                # Adjust based on confidence if available
                confidence = prediction_result.get('confidence', 0.5)
                if confidence > 0.7:
                    quality_score = min(100, quality_score + 10)
                    contamination_index = max(0, contamination_index - 10)
                elif confidence < 0.5:
                    quality_score = max(0, quality_score - 10)
                    contamination_index = min(100, contamination_index + 10)
            else:
                # For regression models
                # Dataset 3: feature_38 is typically 0-100 range (treatment efficiency)
                # Dataset 4: BOD is typically 100-1000 range
                if 'dataset3' in model_name.lower():
                    # UCI dataset - prediction is treatment efficiency/contamination
                    # Higher value = better treatment = higher quality
                    quality_score = max(0, min(100, float(prediction_value)))
                    contamination_index = 100 - quality_score
                elif 'dataset4' in model_name.lower():
                    # Melbourne WWTP - prediction is BOD (lower is better)
                    # BOD range: ~100-1000, normalize to quality score
                    bod_value = float(prediction_value)
                    if bod_value < 200:
                        quality_score = 90.0
                    elif bod_value < 400:
                        quality_score = 70.0
                    elif bod_value < 600:
                        quality_score = 50.0
                    else:
                        quality_score = 30.0
                    contamination_index = 100 - quality_score
                else:
                    # Generic regression - normalize to 0-100
                    quality_score = max(0, min(100, (float(prediction_value) / 200.0) * 100))
                    contamination_index = 100 - quality_score
            
            # Add derived metrics
            prediction_result['quality_score'] = round(quality_score, 2)
            prediction_result['contamination_index'] = round(contamination_index, 2)
            
            return prediction_result
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}", exc_info=True)
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def ensemble_predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Make ensemble prediction using multiple models.
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Ensemble prediction results
        """
        try:
            result = self.model_manager.ensemble_predict(features)
            
            # Calculate quality metrics
            prediction_value = result['prediction']
            quality_score = max(0, min(100, (prediction_value / 200.0) * 100))
            contamination_index = 100 - quality_score
            
            result['quality_score'] = round(quality_score, 2)
            result['contamination_index'] = round(contamination_index, 2)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in ensemble prediction: {str(e)}")
            raise
    
    def get_available_models(self) -> list:
        """Get list of available models."""
        return self.model_manager.get_available_models()

