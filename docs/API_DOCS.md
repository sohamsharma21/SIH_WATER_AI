# SIH WATER AI - API Documentation

## Base URL

- Development: `http://localhost:8000/api`
- Production: `{your-production-url}/api`

## Authentication

Most endpoints require authentication via Supabase JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer {your_jwt_token}
```

---

## Endpoints

### Health Check

#### GET `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "SIH WATER AI"
}
```

---

### Sensor Data Ingestion

#### POST `/ingest`

Ingest sensor data from MQTT or HTTP.

**Request Body:**
```json
{
  "sensor_id": "temp_001",
  "sensor_type": "temperature",
  "parameter_name": "temperature",
  "value": 25.5,
  "unit": "°C",
  "location": "treatment_plant_1",
  "metadata": {
    "additional": "data"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "sensor_id": "temp_001",
  "recorded_at": "2024-01-15T10:30:00Z"
}
```

---

### ML Predictions

#### POST `/predict_with`

Make predictions using ML models.

**Request Body:**
```json
{
  "features": {
    "bod": 200.0,
    "cod": 400.0,
    "ph": 7.2,
    "temperature": 25.0,
    "ammonia": 15.0
  },
  "model_name": "dataset1",  // Optional: auto-select if not provided
  "use_ensemble": false,      // Optional: use ensemble prediction
  "sensor_data": {            // Optional: additional sensor data
    "flow_rate_lpm": 1000.0
  },
  "target_quality": "environmental"  // environmental/industrial/irrigation/drinking
}
```

**Response:**
```json
{
  "prediction": {
    "prediction": 75.5,
    "model_name": "dataset1",
    "quality_score": 75.5,
    "contamination_index": 24.5,
    "confidence": 0.92,
    "features_used": ["bod", "cod", "ph", "temperature", "ammonia"]
  },
  "optimization": {
    "quality_score": 75.5,
    "contamination_index": 24.5,
    "primary_treatment": {
      "settling_time_min": 90.0,
      "coagulant_dose_ml": 75.0,
      "sludge_volume_index": 95.0,
      "recommendations": [...]
    },
    "secondary_treatment": {
      "aeration_time_min": 300.0,
      "do_target_ppm": 2.8,
      "blower_speed_rpm": 1200,
      "sludge_age_days": 10.0,
      "recommendations": [...]
    },
    "tertiary_treatment": {
      "filtration_rate_lpm": 8.5,
      "chlorine_dose_ml": 2.5,
      "ro_trigger": false,
      "recommendations": [...]
    },
    "final_reuse": {
      "reuse_type": "environmental",
      "recovery_percentage": 95.0,
      "description": "Suitable for environmental discharge"
    },
    "dosing_ml": {
      "coagulant": 75.0,
      "chlorine": 2.5
    },
    "recommended_process_steps": [...],
    "expected_recovery_percentage": 95.0
  },
  "prediction_id": "uuid-here"
}
```

---

### Model Training

#### POST `/train/{dataset}`

Train a model for a specific dataset.

**Path Parameters:**
- `dataset`: Dataset identifier (`dataset1`, `dataset2`, `dataset3`, `dataset4`)

**Request Body:**
```json
{
  "csv_path": "/path/to/csv",  // Optional: auto-detect if not provided
  "target_column": "target"     // Optional: auto-detect if not provided
}
```

**Response:**
```json
{
  "status": "success",
  "model_metadata": {
    "dataset_name": "dataset1",
    "model_name": "dataset1_model_v20240115_103000.pkl",
    "model_version": "20240115_103000",
    "model_path": "/path/to/model.pkl",
    "model_type": "regressor",
    "training_date": "2024-01-15T10:30:00Z",
    "accuracy": 0.92,
    "r2_score": 0.89,
    "feature_columns": [...],
    "target_column": "quality_score"
  }
}
```

---

#### POST `/train_all`

Train all available models sequentially.

**Request Body:** None

**Response:**
```json
{
  "status": "completed",
  "results": {
    "dataset1": {
      "status": "success",
      "metadata": {...}
    },
    "dataset2": {
      "status": "success",
      "metadata": {...}
    },
    "dataset3": {
      "status": "skipped",
      "reason": "no_csv_files"
    },
    "dataset4": {
      "status": "success",
      "metadata": {...}
    }
  }
}
```

---

### Model Management

#### GET `/models`

Get list of all available models.

**Response:**
```json
{
  "manager_models": [
    {
      "dataset_name": "dataset1",
      "model_type": "regressor",
      "feature_columns": [...],
      "target_column": "quality_score",
      "metadata": {...}
    }
  ],
  "database_models": [
    {
      "id": "uuid",
      "dataset_name": "dataset1",
      "model_name": "dataset1_model_v20240115_103000.pkl",
      "model_version": "20240115_103000",
      "is_active": true,
      "training_date": "2024-01-15T10:30:00Z",
      "accuracy": 0.92,
      "r2_score": 0.89
    }
  ]
}
```

---

### Digital Twin Status

#### GET `/twin_status`

Get current digital twin status for frontend visualization.

**Response:**
```json
{
  "sensor_status": {
    "temperature": {
      "current_value": 25.5,
      "unit": "°C",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    "ph": {
      "current_value": 7.2,
      "unit": "pH",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  },
  "latest_prediction": {
    "id": "uuid",
    "quality_score": 75.5,
    "contamination_index": 24.5,
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "twin_state": {
    "water_levels": {},
    "turbidity": 24.5,
    "alerts": []
  }
}
```

---

### Sensor Data

#### GET `/sensors/recent`

Get recent sensor readings.

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 100)

**Response:**
```json
{
  "sensors": [
    {
      "id": "uuid",
      "sensor_id": "temp_001",
      "sensor_type": "temperature",
      "parameter_name": "temperature",
      "value": 25.5,
      "unit": "°C",
      "timestamp": "2024-01-15T10:30:00Z",
      "location": "treatment_plant_1"
    }
  ],
  "count": 100
}
```

---

### Predictions

#### GET `/predictions/recent`

Get recent predictions.

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 50)

**Response:**
```json
{
  "predictions": [
    {
      "id": "uuid",
      "model_name": "dataset1",
      "quality_score": 75.5,
      "contamination_index": 24.5,
      "timestamp": "2024-01-15T10:30:00Z",
      "input_data": {...},
      "predictions": {...}
    }
  ],
  "count": 50
}
```

---

### Report Generation

#### POST `/report`

Generate PDF report with comprehensive analysis.

**Request Body:**
```json
{
  "prediction_id": "uuid",  // Optional: fetch prediction from database
  "sensor_data": {          // Optional: provide sensor data directly
    "temperature": 25.5,
    "ph": 7.2
  },
  "optimization_results": {  // Optional: provide optimization results
    "primary_treatment": {...},
    "secondary_treatment": {...}
  }
}
```

**Response:**
```json
{
  "status": "success",
  "report_url": "https://supabase.co/storage/v1/object/public/reports/report_20240115_103000.pdf",
  "file_size": 245760
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently, no rate limiting is enforced. In production, consider implementing:
- Per-user rate limits
- Per-IP rate limits
- Endpoint-specific limits

---

## WebSocket (Realtime)

Supabase Realtime provides WebSocket connections for:
- Sensor data updates
- Prediction updates
- Digital twin state changes

Subscribe to table changes:
```javascript
const subscription = supabase
  .channel('sensors')
  .on('postgres_changes', 
    { event: 'INSERT', schema: 'public', table: 'sensors' },
    (payload) => {
      console.log('New sensor data:', payload.new)
    }
  )
  .subscribe()
```

---

## API Versioning

Current version: `v1`

All endpoints are prefixed with `/api`. Future versions may use `/api/v2`, etc.

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger/OpenAPI documentation where you can:
- Test endpoints directly
- View request/response schemas
- See example requests

---

## Example Usage

### Python

```python
import requests

API_URL = "http://localhost:8000/api"

# Make prediction
response = requests.post(f"{API_URL}/predict_with", json={
    "features": {
        "bod": 200.0,
        "cod": 400.0,
        "ph": 7.2
    },
    "target_quality": "environmental"
})

print(response.json())
```

### JavaScript/TypeScript

```typescript
import api from '@/lib/api'

// Make prediction
const response = await api.predict({
  features: {
    bod: 200.0,
    cod: 400.0,
    ph: 7.2
  },
  target_quality: 'environmental'
})

console.log(response.data)
```

---

## Support

For issues or questions, please refer to the main README.md or create an issue in the project repository.

