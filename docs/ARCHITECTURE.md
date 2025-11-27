# SIH WATER AI - System Architecture

## Overview

SIH WATER AI is a full-stack industrial wastewater treatment optimization platform that integrates real-time sensor data, multi-model machine learning, 3D visualization, and automated treatment recommendations.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Landing  │  │ Dashboard│  │  Reports │  │  Admin   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐     │
│  │          Digital Twin (React-Three-Fiber)            │     │
│  │      Real-time 3D visualization with animations      │     │
│  └──────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              │ WebSocket (Realtime)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   API Routes │  │   Services   │  │  ML Pipeline │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Optimizers   │  │ PDF Reports  │  │  MQTT Service│        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Supabase   │    │  MQTT Broker │    │  ML Models   │
│              │    │              │    │              │
│ - PostgreSQL │    │ - Mosquitto  │    │ - dataset1   │
│ - Auth       │    │ - Cloud      │    │ - dataset2   │
│ - Storage    │    │   Broker     │    │ - dataset3   │
│ - Realtime   │    │              │    │ - dataset4   │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## Component Details

### 1. Frontend Layer (Next.js 14)

**Technology Stack:**
- Next.js 14 with App Router
- React 18
- TypeScript
- TailwindCSS for styling
- React-Three-Fiber for 3D visualization
- Framer Motion for animations
- Supabase Auth for authentication

**Pages:**
- `/` - Landing page
- `/login` - User authentication
- `/signup` - User registration
- `/dashboard` - Main dashboard with real-time data
- `/reports` - PDF report viewer
- `/admin` - Model management and training

**Key Components:**
- `DigitalTwin.tsx` - 3D plant visualization
- `SensorDashboard.tsx` - Real-time sensor readings
- `PredictionCard.tsx` - ML prediction display
- `TreatmentOptimizer.tsx` - Treatment recommendations UI

### 2. Backend Layer (FastAPI)

**Technology Stack:**
- FastAPI (Python 3.11)
- Pydantic for validation
- Supabase-py for database
- scikit-learn for ML
- ReportLab for PDF generation
- paho-mqtt for MQTT communication

**Main Modules:**

#### API Routes (`app/api/routes.py`)
- RESTful endpoints for all operations
- Request/response validation with Pydantic
- Error handling and logging

#### ML Pipeline (`app/ml/`)
- `pipeline.py` - Unified ML pipeline
- `trainer.py` - Model training functions
- `model_manager.py` - Model loading and selection

#### Services (`app/services/`)
- `ml_service.py` - ML prediction service
- `optimizers.py` - Treatment optimization engine
- `supabase_service.py` - Database operations
- `report_service.py` - PDF report generation
- `mqtt_service.py` - MQTT message handling

### 3. Database Layer (Supabase)

**Tables:**
- `sensors` - Real-time sensor readings
- `predictions` - ML model predictions
- `models` - ML model metadata
- `reports` - PDF report metadata
- `treatment_recommendations` - Optimization outputs

**Features:**
- Row Level Security (RLS) policies
- Real-time subscriptions via WebSocket
- Storage bucket for PDF reports
- Authentication and authorization

### 4. ML Models

**Unified Pipeline:**
```
Input Data → Imputer → PolynomialFeatures(2) → StandardScaler → RandomForest → Predictions
```

**Model Training:**
- GridSearchCV for hyperparameter tuning
- Cross-validation for model validation
- Model versioning and metadata storage
- Automatic model selection based on features

**Four Models:**
1. **NYC DEP Model** - Primary/Secondary treatment prediction
2. **Potability Model** - Tertiary treatment classification
3. **UCI Model** - Contamination severity assessment
4. **WWTP Model** - Aeration control and BOD/COD prediction

### 5. Treatment Optimization Engine

**Three-Stage Optimization:**

1. **Primary Treatment Optimizer**
   - Calculates settling time based on contamination
   - Determines coagulant dosing
   - Estimates sludge volume index

2. **Secondary Treatment Optimizer**
   - Computes aeration time from BOD/COD levels
   - Sets DO targets
   - Controls blower speed (ML-driven)
   - Manages sludge age

3. **Tertiary Treatment Optimizer**
   - Adjusts filtration rates
   - Calculates chlorine dosing
   - Determines RO requirement

4. **Final Reuse Engine**
   - Classifies reuse type (irrigation/industrial/environmental/drinking)
   - Calculates expected recovery percentage

### 6. MQTT Integration

**Message Flow:**
```
Sensors → MQTT Broker → MQTT Service → Ingest API → Supabase → Frontend (Realtime)
```

**Topics:**
- `plant/sensors/#` - Wildcard subscription for all sensors
- `plant/sensors/{sensor_type}/{sensor_id}` - Specific sensor data

**Simulator:**
- Generates realistic sensor readings
- Simulates 10 different sensor types
- Configurable publish interval

### 7. Digital Twin (3D Visualization)

**Features:**
- 3D plant model with tanks, pipes, clarifiers
- Real-time water level animations
- Color changes based on turbidity/contamination
- Aeration bubble effects
- Camera controls for navigation
- Hover overlays for parameter display

**Technology:**
- Three.js for 3D graphics
- React-Three-Fiber for React integration
- Drei for helpers and controls
- GSAP for animations

---

## Data Flow

### Sensor Data Ingestion

1. Sensor sends data via MQTT → `plant/sensors/{type}/{id}`
2. MQTT Service receives message
3. Data parsed and validated
4. Stored in Supabase `sensors` table
5. Frontend receives update via Realtime subscription
6. Digital Twin updates visualizations

### ML Prediction Flow

1. User/sensor provides feature data
2. API endpoint `/api/predict_with` called
3. Model Manager selects appropriate model
4. Model makes prediction
5. Optimization engine calculates treatment recommendations
6. Results stored in Supabase
7. Frontend displays predictions and recommendations

### Report Generation Flow

1. User requests report via `/api/report`
2. System collects:
   - Recent sensor data
   - Latest predictions
   - Optimization results
3. ReportGenerator creates PDF using ReportLab
4. PDF uploaded to Supabase Storage
5. Public URL returned to frontend
6. User can view/download report

---

## Security

### Authentication
- Supabase Auth with email/password
- JWT tokens for API access
- Session management

### Authorization
- Row Level Security (RLS) policies
- Role-based access (admin/user)
- Service role for backend operations

### Data Security
- Environment variables for secrets
- Encrypted connections (HTTPS/WSS)
- Input validation with Pydantic

---

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- CDN for static assets

### Performance Optimization
- Model caching in memory
- Database indexes on frequently queried columns
- Async operations for I/O-bound tasks
- WebSocket connections for real-time updates

### Future Enhancements
- Redis for caching
- Message queue for async processing
- Load balancing for API servers
- Distributed model serving

---

## Deployment Architecture

### Development
- Local FastAPI server (Uvicorn)
- Local Next.js dev server
- Local MQTT broker (Mosquitto)
- Supabase cloud database

### Production (Recommended)
- Backend: Vercel/Heroku/Railway
- Frontend: Vercel
- Database: Supabase Cloud
- Storage: Supabase Storage
- MQTT: HiveMQ Cloud / AWS IoT Core

---

## Monitoring & Logging

### Backend Logging
- Python logging module
- Structured logs with timestamps
- Error tracking and alerts

### Frontend Monitoring
- Browser console logs
- Error boundaries
- API request tracking

### Database Monitoring
- Supabase dashboard
- Query performance metrics
- Storage usage tracking

---

## API Architecture

### REST Endpoints
- Standard HTTP methods (GET, POST)
- JSON request/response format
- OpenAPI/Swagger documentation at `/docs`

### WebSocket
- Supabase Realtime for live updates
- Automatic reconnection
- Message queuing

---

## File Structure

See project `README.md` for detailed file structure.

---

## Technology Decisions

### Why FastAPI?
- Fast performance with async support
- Automatic API documentation
- Type safety with Pydantic
- Easy to integrate with ML libraries

### Why Next.js?
- Server-side rendering for SEO
- Built-in routing
- Optimized production builds
- Great React ecosystem

### Why Supabase?
- PostgreSQL with real-time capabilities
- Built-in authentication
- Easy storage integration
- Generous free tier

### Why Three.js/React-Three-Fiber?
- Industry-standard 3D library
- React integration
- Large ecosystem
- Good performance

---

## Future Architecture Enhancements

1. **Microservices**
   - Separate ML service
   - Separate report service
   - API gateway

2. **Event-Driven Architecture**
   - Event streaming with Kafka
   - Asynchronous processing
   - Event sourcing for audit trail

3. **Edge Computing**
   - Edge functions for preprocessing
   - Reduced latency
   - Offline capability

4. **AI/ML Enhancements**
   - Real-time model updates
   - Federated learning
   - Model versioning with MLflow

---

This architecture provides a solid foundation for a production-ready industrial wastewater treatment optimization system.

