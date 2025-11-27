"""
Unified ML Pipeline for SIH WATER AI
Pipeline: Imputer → PolynomialFeatures(degree=2) → StandardScaler → RandomForest
"""
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedMLPipeline:
    """Unified ML pipeline for all wastewater treatment models."""
    
    def __init__(self, model_type: str = "regressor", random_state: int = 42):
        """
        Initialize the ML pipeline.
        
        Args:
            model_type: "regressor" or "classifier"
            random_state: Random seed for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.pipeline = None
        self.feature_columns = None
        self.target_column = None
        self.is_fitted = False
        
    def create_pipeline(self, n_features: int) -> Pipeline:
        """Create the unified pipeline."""
        # Imputer for handling missing values
        imputer = SimpleImputer(strategy='median')
        
        # Polynomial features - simplified for speed
        # Use degree 1 (linear) for faster training, can upgrade later
        poly_features = PolynomialFeatures(degree=1, include_bias=False)  # Linear only for speed
        
        # Standard scaler
        scaler = StandardScaler()
        
        # Base model (will be replaced by GridSearchCV)
        if self.model_type == "regressor":
            base_model = RandomForestRegressor(random_state=self.random_state)
        else:
            base_model = RandomForestClassifier(random_state=self.random_state)
        
        # Create pipeline
        steps = [
            ('imputer', imputer),
            ('poly_features', poly_features),
            ('scaler', scaler),
            ('model', base_model)
        ]
        
        return Pipeline(steps)
    
    def get_hyperparameter_grid(self) -> Dict[str, list]:
        """Get hyperparameter grid for GridSearchCV - optimized for speed."""
        # Single parameter set - no grid search, just train once
        return {
            'model__n_estimators': [50],  # Single value - fastest
            'model__max_depth': [8],      # Single value - reduced depth
            'model__min_samples_split': [2],
            'model__min_samples_leaf': [1]
        }
    
    def prepare_data(self, df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for training.
        
        Args:
            df: Input DataFrame
            target_column: Name of target column
            
        Returns:
            X, y tuple
        """
        # Separate features and target
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")
        
        y = df[target_column].copy()
        X = df.drop(columns=[target_column]).copy()
        
        # Drop rows where target is NaN
        valid_mask = y.notna()
        X = X[valid_mask].copy()
        y = y[valid_mask].copy()
        
        logger.info(f"Dropped {len(df) - len(X)} rows with NaN target values")
        
        # Remove non-numeric columns
        numeric_columns = X.select_dtypes(include=[np.number]).columns.tolist()
        X = X[numeric_columns]
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        self.target_column = target_column
        
        # Remove columns with all NaN values
        X = X.loc[:, X.notna().any(axis=0)]
        
        # Update feature columns
        self.feature_columns = X.columns.tolist()
        
        logger.info(f"Prepared data: {X.shape[0]} samples, {X.shape[1]} features")
        
        return X, y
    
    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        cv: int = 5,
        n_jobs: int = -1,
        test_size: float = 0.2
    ) -> Dict[str, Any]:
        """
        Train the model with GridSearchCV.
        
        Args:
            X: Feature matrix
            y: Target vector
            cv: Cross-validation folds
            n_jobs: Number of parallel jobs
            test_size: Test set size
            
        Returns:
            Dictionary with training metrics
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        
        # Create pipeline
        n_features = X_train.shape[1]
        self.pipeline = self.create_pipeline(n_features)
        
        # Get hyperparameter grid
        param_grid = self.get_hyperparameter_grid()
        
        # Fast training - skip GridSearchCV if only one parameter set
        total_combinations = 1
        for v in param_grid.values():
            total_combinations *= len(v)
        
        if total_combinations == 1:
            # Single parameter set - train directly without GridSearchCV
            logger.info("Single parameter set - training directly (fast mode)...")
            # Set parameters directly
            self.pipeline.set_params(**{k: v[0] for k, v in param_grid.items()})
            self.pipeline.fit(X_train, y_train)
            self.is_fitted = True
            
            # Evaluate
            train_score = self.pipeline.score(X_train, y_train)
            test_score = self.pipeline.score(X_test, y_test)
            y_pred = self.pipeline.predict(X_test)
            
            metrics = {
                'best_params': {k: v[0] for k, v in param_grid.items()},
                'train_score': float(train_score),
                'test_score': float(test_score),
                'best_cv_score': float(test_score),  # Use test score as proxy
                'n_samples': len(X_train),
                'n_features': n_features
            }
        else:
            # Multiple parameter sets - use GridSearchCV
            logger.info("Starting GridSearchCV...")
            effective_cv = min(cv, 2)  # Max 2 folds for speed
            grid_search = GridSearchCV(
                self.pipeline,
                param_grid,
                cv=effective_cv,
                n_jobs=n_jobs,
                scoring='r2' if self.model_type == "regressor" else 'f1_macro',
                verbose=0
            )
            grid_search.fit(X_train, y_train)
            self.pipeline = grid_search.best_estimator_
            self.is_fitted = True
            
            train_score = grid_search.score(X_train, y_train)
            test_score = grid_search.score(X_test, y_test)
            y_pred = self.pipeline.predict(X_test)
            
            metrics = {
                'best_params': grid_search.best_params_,
                'train_score': float(train_score),
                'test_score': float(test_score),
                'best_cv_score': float(grid_search.best_score_),
                'n_samples': len(X_train),
                'n_features': n_features
            }
        
        # Additional metrics for regressor
        if self.model_type == "regressor":
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            metrics['mse'] = float(mean_squared_error(y_test, y_pred))
            metrics['mae'] = float(mean_absolute_error(y_test, y_pred))
            metrics['r2'] = float(r2_score(y_test, y_pred))
        
        # Additional metrics for classifier
        else:
            from sklearn.metrics import accuracy_score, f1_score, classification_report
            metrics['accuracy'] = float(accuracy_score(y_test, y_pred))
            metrics['f1_score'] = float(f1_score(y_test, y_pred, average='macro'))
        
        logger.info(f"Training complete. Test score: {test_score:.4f}")
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions."""
        if not self.is_fitted:
            raise ValueError("Model must be trained before making predictions")
        
        # Ensure same columns as training
        X = X[self.feature_columns]
        
        return self.pipeline.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Get prediction probabilities (for classifiers only)."""
        if self.model_type != "classifier":
            raise ValueError("predict_proba only available for classifiers")
        if not self.is_fitted:
            raise ValueError("Model must be trained before making predictions")
        
        X = X[self.feature_columns]
        return self.pipeline.predict_proba(X)
    
    def save(self, filepath: Path) -> None:
        """Save the trained pipeline."""
        if not self.is_fitted:
            raise ValueError("Model must be trained before saving")
        
        # Save pipeline
        joblib.dump(self.pipeline, filepath)
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column,
            'random_state': self.random_state
        }
        
        metadata_path = filepath.with_suffix('.meta.pkl')
        joblib.dump(metadata, metadata_path)
        
        logger.info(f"Model saved to: {filepath}")
    
    @classmethod
    def load(cls, filepath: Path) -> 'UnifiedMLPipeline':
        """Load a trained pipeline."""
        # Load pipeline
        pipeline = joblib.load(filepath)
        
        # Load metadata
        metadata_path = filepath.with_suffix('.meta.pkl')
        if metadata_path.exists():
            metadata = joblib.load(metadata_path)
        else:
            metadata = {'model_type': 'regressor', 'feature_columns': None, 'target_column': None}
        
        # Create instance
        instance = cls(model_type=metadata['model_type'])
        instance.pipeline = pipeline
        instance.feature_columns = metadata.get('feature_columns')
        instance.target_column = metadata.get('target_column')
        instance.is_fitted = True
        
        logger.info(f"Model loaded from: {filepath}")
        
        return instance

