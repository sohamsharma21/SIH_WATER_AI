"""
FastAPI Routes for SIH WATER AI
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import logging
from datetime import datetime

from ..services.ml_service import MLService
from ..services.optimizers import TreatmentOptimizerEngine
from ..services.supabase_service import SupabaseService
from ..services.report_service import ReportGenerator
from ..ml.trainer import train_on_csv, train_all
from ..ml.model_manager import get_model_manager
from ..utils.responses import (
    success_response, error_response, created_response,
    validation_error_response, not_found_response,
    paginated_response, internal_error_response
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
ml_service = MLService()
optimizer_engine = TreatmentOptimizerEngine()
supabase_service = SupabaseService()
report_generator = ReportGenerator()


# Request/Response Models
class SensorDataRequest(BaseModel):
    sensor_id: str
    sensor_type: str
    parameter_name: str
    value: float
    unit: Optional[str] = None
    location: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": "SENSOR_001",
                "sensor_type": "flow_meter",
                "parameter_name": "flow_rate",
                "value": 1000.5,
                "unit": "LPM",
                "location": "Primary Tank",
                "metadata": {"device": "device_001"}
            }
        }


class PredictionRequest(BaseModel):
    features: Dict[str, float]
    model_name: Optional[str] = None
    use_ensemble: bool = False
    sensor_data: Optional[Dict[str, float]] = None
    target_quality: str = "environmental"
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": {
                    "ph": 7.0,
                    "Hardness": 200.0,
                    "Solids": 20000.0
                },
                "model_name": "dataset2",
                "use_ensemble": False
            }
        }


class TrainRequest(BaseModel):
    csv_path: Optional[str] = None
    target_column: Optional[str] = None


class ReportRequest(BaseModel):
    prediction_id: Optional[str] = None
    sensor_data: Optional[Dict[str, Any]] = None
    optimization_results: Optional[Dict[str, Any]] = None


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return success_response(
        {"service": "SIH WATER AI", "status": "healthy"},
        "Service is healthy"
    )


@router.post("/ingest")
async def ingest_sensor_data(data: SensorDataRequest):
    """Ingest sensor data from MQTT or HTTP."""
    try:
        # Validate required fields
        if not data.sensor_id or not data.sensor_type:
            return validation_error_response(
                "Missing required fields",
                {"sensor_id": "Required", "sensor_type": "Required"}
            )
        
        sensor_record = {
            'sensor_id': data.sensor_id,
            'sensor_type': data.sensor_type,
            'parameter_name': data.parameter_name,
            'value': data.value,
            'unit': data.unit,
            'location': data.location,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': data.metadata or {}
        }
        
        # Insert into database
        result = supabase_service.insert_sensor_data(sensor_record)
        
        return created_response(
            {
                "sensor_id": data.sensor_id,
                "recorded_at": result.get('timestamp') if result else datetime.utcnow().isoformat()
            },
            "Sensor data ingested successfully"
        )
    except Exception as e:
        logger.error(f"Error ingesting sensor data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=error_response(f"Failed to ingest sensor data: {str(e)}", 500)
        )


@router.post("/predict")
async def predict_with_model(request: PredictionRequest):
    """Make prediction using ML models."""
    try:
        # Make prediction
        if request.use_ensemble:
            prediction_result = ml_service.ensemble_predict(request.features)
            model_name = "ensemble"
        else:
            try:
                prediction_result = ml_service.predict(request.features, request.model_name)
                model_name = prediction_result.get('model_name', 'unknown')
            except ValueError as ve:
                logger.error(f"Prediction error: {str(ve)}")
                raise HTTPException(status_code=400, detail=str(ve))
        
        # Store prediction in database
        from datetime import datetime
        prediction_record = {
            'model_name': model_name,
            'input_data': request.features,
            'predictions': prediction_result,
            'quality_score': prediction_result.get('quality_score'),
            'contamination_index': prediction_result.get('contamination_index'),
            'confidence': prediction_result.get('confidence', 0.0),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        db_record = supabase_service.insert_prediction(prediction_record)
        
        # Run optimization if sensor data provided
        optimization_results = None
        if request.sensor_data or request.features:
            optimization_results = optimizer_engine.optimize_all(
                quality_score=prediction_result.get('quality_score', 50),
                contamination_index=prediction_result.get('contamination_index', 50),
                sensor_data=request.sensor_data or request.features,
                target_quality=request.target_quality
            )
        
        return {
            "status": "success",
            "prediction": prediction_result,
            "optimization": optimization_results,
            "prediction_id": db_record.get('id') if db_record else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to make prediction")


@router.post("/train/{dataset}")
async def train_model(dataset: str, request: TrainRequest):
    """Train a model for a specific dataset."""
    try:
        from pathlib import Path
        from ..config import settings
        
        # Find CSV file
        if request.csv_path:
            csv_path = Path(request.csv_path)
        else:
            # Auto-detect from dataset name
            data_dir = Path(settings.DATA_DIR) / dataset
            csv_files = list(data_dir.glob("*.csv"))
            if not csv_files:
                raise HTTPException(
                    status_code=404,
                    detail=f"No CSV files found for dataset: {dataset}"
                )
            csv_path = max(csv_files, key=lambda f: f.stat().st_size)
        
        # Train model
        model_metadata = train_on_csv(dataset, csv_path, request.target_column)
        
        # Store metadata in database
        supabase_metadata = {
            'dataset_name': model_metadata['dataset_name'],
            'model_name': model_metadata['model_name'],
            'model_version': model_metadata['model_version'],
            'model_path': model_metadata['model_path'],
            'model_type': model_metadata['model_type'],
            'training_date': model_metadata['training_date'],
            'accuracy': model_metadata.get('accuracy'),
            'f1_score': model_metadata.get('f1_score'),
            'r2_score': model_metadata.get('r2_score'),
            'training_params': model_metadata.get('training_params', {}),
            'feature_columns': model_metadata.get('feature_columns', []),
            'target_column': model_metadata.get('target_column'),
            'model_metrics': model_metadata.get('metrics', {})
        }
        
        supabase_service.insert_model_metadata(supabase_metadata)
        
        # Reload model manager to include new model
        from ..ml.model_manager import _model_manager
        global _model_manager
        _model_manager = None
        get_model_manager()
        
        return {
            "status": "success",
            "model_metadata": model_metadata
        }
        
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train_all")
async def train_all_models():
    """Train all available models."""
    try:
        results = train_all()
        
        # Store successful models in database
        for dataset_key, result in results.items():
            if result.get('status') == 'success':
                metadata = result.get('metadata', {})
                supabase_metadata = {
                    'dataset_name': metadata['dataset_name'],
                    'model_name': metadata['model_name'],
                    'model_version': metadata['model_version'],
                    'model_path': metadata['model_path'],
                    'model_type': metadata['model_type'],
                    'training_date': metadata['training_date'],
                    'accuracy': metadata.get('accuracy'),
                    'f1_score': metadata.get('f1_score'),
                    'r2_score': metadata.get('r2_score'),
                    'training_params': metadata.get('training_params', {}),
                    'feature_columns': metadata.get('feature_columns', []),
                    'target_column': metadata.get('target_column'),
                    'model_metrics': metadata.get('metrics', {})
                }
                supabase_service.insert_model_metadata(supabase_metadata)
        
        # Reload model manager
        from ..ml.model_manager import _model_manager
        global _model_manager
        _model_manager = None
        get_model_manager()
        
        return {
            "status": "completed",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error training all models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def get_models():
    """Get list of available models."""
    try:
        # Get from model manager
        manager_models = ml_service.get_available_models()
        
        # Also get from database
        db_models = supabase_service.get_active_models()
        
        return {
            "status": "success",
            "manager_models": manager_models,
            "database_models": db_models,
            "count": {
                "manager": len(manager_models),
                "database": len(db_models)
            }
        }
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch models")


@router.get("/twin_status")
async def get_twin_status():
    """Get current digital twin status for frontend."""
    try:
        # Get recent sensor data
        recent_sensors = supabase_service.get_recent_sensors(limit=50)
        
        # Get recent predictions
        recent_predictions = supabase_service.get_recent_predictions(limit=10)
        
        # Aggregate sensor data by parameter
        sensor_status = {}
        for sensor in recent_sensors:
            param = sensor.get('parameter_name')
            if param not in sensor_status:
                sensor_status[param] = {
                    'current_value': sensor.get('value'),
                    'unit': sensor.get('unit'),
                    'timestamp': sensor.get('timestamp')
                }
        
        # Get latest prediction
        latest_prediction = recent_predictions[0] if recent_predictions else None
        
        return {
            "status": "success",
            "sensor_status": sensor_status,
            "latest_prediction": latest_prediction,
            "twin_state": {
                "water_levels": {},
                "turbidity": latest_prediction.get('contamination_index') if latest_prediction else 50,
                "alerts": []
            }
        }
    except Exception as e:
        logger.error(f"Error fetching twin status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch twin status")


@router.get("/sensors/recent")
async def get_recent_sensors(limit: int = 100):
    """Get recent sensor readings."""
    try:
        if limit < 1 or limit > 10000:
            limit = 100
        sensors = supabase_service.get_recent_sensors(limit=limit)
        return {
            "status": "success",
            "sensors": sensors, 
            "count": len(sensors)
        }
    except Exception as e:
        logger.error(f"Error fetching sensors: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch sensors")


@router.get("/predictions/recent")
async def get_recent_predictions(limit: int = 50):
    """Get recent predictions."""
    try:
        if limit < 1 or limit > 10000:
            limit = 50
        predictions = supabase_service.get_recent_predictions(limit=limit)
        return {
            "status": "success",
            "predictions": predictions, 
            "count": len(predictions)
        }
    except Exception as e:
        logger.error(f"Error fetching predictions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch predictions")


@router.post("/report")
async def generate_report(request: ReportRequest):
    """Generate PDF report."""
    try:
        # Get prediction data if prediction_id provided
        prediction_data = {}
        optimization_results = request.optimization_results
        
        if request.prediction_id:
            # Fetch prediction from database
            # This is a simplified version - in production, fetch from DB
            prediction_data = {
                'quality_score': 75.0,
                'contamination_index': 25.0,
                'model_name': 'dataset1'
            }
        
        # Get sensor data
        sensor_data = None
        if request.sensor_data:
            sensor_data = request.sensor_data
        else:
            sensor_data = supabase_service.get_recent_sensors(limit=100)
        
        # Generate optimization if not provided
        if not optimization_results:
            optimization_results = optimizer_engine.optimize_all(
                quality_score=prediction_data.get('quality_score', 75),
                contamination_index=prediction_data.get('contamination_index', 25),
                sensor_data=request.sensor_data or {},
                target_quality="environmental"
            )
        
        # Generate PDF
        pdf_bytes = report_generator.generate_report(
            prediction_data=prediction_data,
            optimization_results=optimization_results,
            sensor_data=sensor_data if isinstance(sensor_data, list) else None,
            plant_info={"name": "Treatment Plant 1", "location": "Unknown"}
        )
        
        # Upload to Supabase Storage
        public_url = report_generator.save_and_upload_report(pdf_bytes)
        
        return {
            "status": "success",
            "report_url": public_url,
            "file_size": len(pdf_bytes)
        }
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

