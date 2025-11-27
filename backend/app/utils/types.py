"""
Request/Response Type Definitions
Centralized data models for API communication
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


# ============================================================================
# SENSOR DATA MODELS
# ============================================================================

class SensorDataRequest(BaseModel):
    """Request model for ingesting sensor data."""
    sensor_id: str = Field(..., description="Unique sensor identifier")
    sensor_type: str = Field(..., description="Type of sensor (e.g., pH, flow_meter, temperature)")
    parameter_name: str = Field(..., description="Name of measured parameter")
    value: float = Field(..., description="Measured value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    location: Optional[str] = Field(None, description="Physical location of sensor")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
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


class SensorDataResponse(BaseModel):
    """Response model for sensor data ingestion."""
    sensor_id: str
    parameter_name: str
    value: float
    recorded_at: str
    success: bool = True


# ============================================================================
# PREDICTION MODELS
# ============================================================================

class PredictionRequest(BaseModel):
    """Request model for making predictions."""
    features: Dict[str, float] = Field(..., description="Input features for prediction")
    model_name: Optional[str] = Field(None, description="Specific model to use (auto-select if None)")
    use_ensemble: bool = Field(False, description="Use ensemble prediction")
    sensor_data: Optional[Dict[str, float]] = Field(None, description="Associated sensor data")
    target_quality: str = Field("environmental", description="Target quality metric")
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": {"feature_0": 1.0, "feature_1": 2.0},
                "model_name": "dataset3",
                "use_ensemble": False
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    prediction: float
    model_name: str
    quality_score: float
    contamination_index: float
    confidence: Optional[float] = None
    features_used: List[str]
    probabilities: Optional[List[float]] = None
    timestamp: str


class EnsemblePredictionResponse(BaseModel):
    """Response model for ensemble predictions."""
    prediction: float
    individual_predictions: Dict[str, float]
    weights: List[float]
    method: str = "weighted_average"
    timestamp: str


# ============================================================================
# MODEL MANAGEMENT
# ============================================================================

class ModelInfo(BaseModel):
    """Information about a trained model."""
    dataset_name: str
    model_type: str
    feature_columns: List[str]
    target_column: Optional[str] = None
    accuracy: Optional[float] = None
    trained_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ModelsListResponse(BaseModel):
    """Response containing list of available models."""
    models: List[ModelInfo]
    total: int


# ============================================================================
# DIGITAL TWIN / STATUS MODELS
# ============================================================================

class TankStatus(BaseModel):
    """Status of a treatment tank."""
    tank_name: str
    volume_liters: float
    current_level: float
    turbidity: float
    temperature: float
    ph: float
    pressure_bar: Optional[float] = None
    status: str  # "normal", "warning", "alert"


class PlantStatus(BaseModel):
    """Overall plant status."""
    plant_name: str = "Wastewater Treatment Plant"
    operational_status: str
    total_capacity: float
    current_load: float
    efficiency_percentage: float
    tanks: List[TankStatus]
    last_updated: str


# ============================================================================
# TRAINING MODELS
# ============================================================================

class TrainRequest(BaseModel):
    """Request to train a model."""
    csv_path: Optional[str] = None
    target_column: Optional[str] = None
    dataset_name: Optional[str] = None
    test_size: float = 0.2
    random_state: int = 42


class TrainResponse(BaseModel):
    """Response from training."""
    dataset_name: str
    status: str
    accuracy: Optional[float] = None
    trained_at: str
    model_location: str


# ============================================================================
# REPORT MODELS
# ============================================================================

class ReportRequest(BaseModel):
    """Request to generate a report."""
    prediction_id: Optional[str] = None
    sensor_data: Optional[Dict[str, Any]] = None
    optimization_results: Optional[Dict[str, Any]] = None
    include_visualizations: bool = True
    date_range: Optional[Dict[str, str]] = None


class ReportResponse(BaseModel):
    """Response containing generated report."""
    report_id: str
    format: str = "PDF"
    file_size_bytes: int
    generated_at: str
    download_url: Optional[str] = None


# ============================================================================
# GENERIC API RESPONSES
# ============================================================================

class SuccessResponse(BaseModel):
    """Standardized success response."""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    status_code: int = 200


class ErrorDetail(BaseModel):
    """Error detail."""
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Standardized error response."""
    success: bool = False
    message: str
    error_code: str
    status_code: int
    details: Optional[Dict[str, Any]] = None
    timestamp: str
    request_id: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response."""
    service: str
    status: str
    timestamp: float
    version: str
    
    class DependencyStatus(BaseModel):
        status: str
        available: Optional[int] = None
        
    class ModelsDependency(DependencyStatus):
        models: List[str] = []
    
    class DatabaseDependency(DependencyStatus):
        type: str = "Supabase PostgreSQL"
    
    class MqttDependency(DependencyStatus):
        type: str = "Mosquitto"
    
    dependencies: Optional[Dict[str, Any]] = None


# ============================================================================
# PAGINATION
# ============================================================================

class PaginationMeta(BaseModel):
    """Pagination metadata."""
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(BaseModel):
    """Paginated response."""
    success: bool = True
    data: List[Dict[str, Any]]
    pagination: PaginationMeta
    message: str = "Request successful"
