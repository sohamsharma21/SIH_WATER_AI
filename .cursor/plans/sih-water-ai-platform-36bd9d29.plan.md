<!-- 36bd9d29-31a6-41a8-8871-ab3c20e2f7df 23604b64-57d5-4ea8-943c-1ded840729a9 -->
# SIH WATER AI - Complete Platform Build Plan

## Project Overview

Build a complete Industrial Wastewater Treatment Optimization System with real-time sensor ingestion, 4 ML models, 3D digital twin visualization, automated treatment optimization, PDF reports, and SIH presentation.

---

## Phase 1: Project Setup & Structure

### 1.1 Directory Structure

Create complete folder hierarchy:

```
PROJECT_SIH/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py (FastAPI app)
│   │   ├── models/ (ML model files)
│   │   ├── ml/ (ML pipeline code)
│   │   ├── api/ (API routes)
│   │   ├── services/ (business logic)
│   │   ├── utils/ (helpers)
│   │   └── config.py
│   ├── data/ (datasets - gitignored)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/ (Next.js 14 App Router)
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   └── .env.local.example
├── migrations/
│   ├── schema.sql
│   ├── add_models_table.sql
│   └── rls_policies.sql
├── scripts/
│   ├── download_dataset1.py (NYC DEP - manual URL)
│   ├── download_dataset2.py (Kaggle potability - kagglehub)
│   ├── download_dataset3.py (UCI - placeholder for manual)
│   ├── download_dataset4.py (Kaggle WWTP - kagglehub)
│   └── setup_mqtt_broker.md
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── API_DOCS.md
│   └── SIH_presentation.pptx (auto-generated)
├── assets/
│   └── models/ (3D model placeholders)
└── README.md
```

### 1.2 Configuration Files

- Backend `.env.example` with Supabase, MQTT placeholders
- Frontend `.env.local.example`
- Python `requirements.txt` with all dependencies
- Node `package.json` with Next.js, Three.js, etc.

---

## Phase 2: Dataset Download Scripts

### 2.1 Dataset 1 (NYC DEP)

- Manual download script (CSV/API fetch)
- Data preprocessing pipeline
- Validation checks

### 2.2 Dataset 2 (Water Potability - Kaggle)

```python
import kagglehub
path = kagglehub.dataset_download("adityakadiwal/water-potability")
```

### 2.3 Dataset 3 (UCI Water Treatment)

- Placeholder script with instructions
- User will add manually - document location in `backend/data/dataset3/`

### 2.4 Dataset 4 (Full-Scale WWTP - Kaggle)

```python
import kagglehub
path = kagglehub.dataset_download("d4rklucif3r/full-scale-waste-water-treatment-plant-data")
```

---

## Phase 3: Supabase Database Setup

### 3.1 Tables Schema

- `sensors` - real-time sensor readings
- `predictions` - ML model predictions
- `models` - ML model metadata
- `reports` - PDF report metadata
- `users` - Supabase Auth extension

### 3.2 Migrations

- `schema.sql` - all table definitions
- `add_models_table.sql` - model registry
- `rls_policies.sql` - Row Level Security
- Indexes for performance

### 3.3 Storage Bucket

- `reports` bucket for PDF storage
- Public access policies

---

## Phase 4: ML Pipeline & Models

### 4.1 Unified ML Pipeline

Location: `backend/app/ml/pipeline.py`

- `Imputer` → `PolynomialFeatures(degree=2)` → `StandardScaler` → `RandomForestRegressor/Classifier`
- Hyperparameter grid: `n_estimators=[50,100,200]`, `max_depth=[6,12,20]`
- Cross-validation with GridSearchCV

### 4.2 Model Training Functions

- `train_on_csv(dataset_name, csv_path)` - single model training
- `train_all()` - train all 4 models sequentially
- Model saving: `backend/app/models/{dataset_name}_model_v{timestamp}.pkl`
- Metadata saved to Supabase `models` table

### 4.3 Model Management

- `model_selector(features)` - auto-select appropriate model
- `ensemble_predict(features)` - optional blending
- Model versioning system

### 4.4 Model-Specific Goals

1. **NYC DEP Model**: Primary+Secondary behavior, nitrogen removal prediction
2. **Potability Model**: Tertiary treatment classification
3. **UCI Model**: Contamination severity, treatment class
4. **WWTP Model**: Aeration control, BOD/COD prediction

---

## Phase 5: Treatment Optimization Engine

### 5.1 Optimizer Functions

Location: `backend/app/services/optimizers.py`

#### Primary Treatment Optimizer

- Input: AI predictions (quality_score, contamination_index)
- Output: settling_time, coagulant_dose_ml, sludge_volume_index

#### Secondary Treatment Optimizer

- Output: aeration_time_min, do_target_ppm, blower_speed_rpm, sludge_age_days

#### Tertiary Treatment Optimizer

- Output: filtration_rate_lpm, chlorine_dose_ml, ro_trigger_boolean

#### Final Reuse Engine

- Output: reuse_type (irrigation/industrial/environmental/drinking), recovery_percentage

### 5.2 Optimization Logic

- Rule-based + ML-driven recommendations
- Threshold-based decision trees
- Safety margins and constraints

---

## Phase 6: Backend API (FastAPI)

### 6.1 Main Application

- FastAPI app with CORS, error handling
- Supabase client initialization
- MQTT client connection

### 6.2 API Endpoints

- `POST /api/train/{dataset}` - train specific model
- `POST /api/train_all` - train all models
- `GET /api/models` - list all trained models
- `POST /api/predict_with` - make prediction with model selection
- `POST /api/ingest` - sensor data ingestion (MQTT/HTTP)
- `POST /api/report` - generate PDF report
- `GET /api/twin_status` - digital twin state for frontend
- `GET /api/health` - health check

### 6.3 Services Layer

- `ml_service.py` - model loading, prediction logic
- `optimizer_service.py` - treatment optimization
- `report_service.py` - PDF generation (ReportLab)
- `mqtt_service.py` - MQTT subscription/publishing

---

## Phase 7: PDF Report Generator

### 7.1 Report Structure (ReportLab)

Location: `backend/app/services/report_service.py`

Pages:

1. **Cover**: Title, date, plant info
2. **Summary**: Key metrics, quality_score, recommendations
3. **Plant Diagram**: ASCII/text diagram of treatment flow
4. **Raw Sensor Table**: Tabular sensor data
5. **Predictions**: ML model outputs
6. **Treatment Flow**: Recommended steps with dosages
7. **Graphs**: Time-series charts (matplotlib/plotly)
8. **Digital Twin Snapshot**: Status indicators

### 7.2 Storage

- Generate PDF → Upload to Supabase Storage → Return public URL
- Metadata saved to `reports` table

---

## Phase 8: MQTT Integration

### 8.1 MQTT Listener

Location: `backend/app/services/mqtt_service.py`

- Subscribe to `plant/sensors/#` topic
- Parse incoming JSON sensor data
- Forward to `/api/ingest` endpoint
- Update digital twin state in real-time

### 8.2 MQTT Simulator

Location: `scripts/mqtt_publisher_simulator.py`

- Simulate realistic sensor readings
- Random variation + realistic patterns
- Publish to MQTT broker for testing

### 8.3 MQTT Configuration

- Environment variables for broker URL, port, credentials
- Support for local Mosquitto or cloud brokers

---

## Phase 9: Frontend (Next.js 14)

### 9.1 App Router Structure

```
frontend/app/
├── page.tsx (Landing)
├── login/page.tsx
├── signup/page.tsx
├── dashboard/page.tsx
├── reports/page.tsx
├── admin/page.tsx
└── layout.tsx
```

### 9.2 Components

- `DigitalTwin.tsx` - 3D visualization component
- `SensorDashboard.tsx` - real-time charts
- `PredictionCard.tsx` - ML predictions display
- `TreatmentOptimizer.tsx` - optimizer recommendations UI
- `ReportViewer.tsx` - PDF viewer
- `ModelTrainer.tsx` - admin model training UI

### 9.3 Digital Twin Component

- React-Three-Fiber setup
- 3D plant model (tanks, pipes, clarifiers)
- Real-time water level animations (GSAP)
- Turbidity → color changes
- Aeration bubble effects
- Camera controls (OrbitControls from Drei)
- Hover parameter overlays
- Reactive visuals on contamination alerts

### 9.4 Styling & Animations

- TailwindCSS for styling
- Framer Motion for UI animations
- GSAP for complex industrial animations
- Vanta.js for animated backgrounds

---

## Phase 10: 3D Visualization Libraries Integration

### 10.1 Three.js Setup

- Scene, camera, renderer initialization
- Lighting (ambient + directional)
- Shadows enabled

### 10.2 Plant Model

- Basic 3D geometry (BoxGeometry, CylinderGeometry for tanks)
- Texture mapping for realistic look
- Group organization (primary, secondary, tertiary sections)

### 10.3 Real-time Updates

- Supabase Realtime subscription for sensor data
- WebSocket connection for live updates
- Animation triggers based on ML predictions

### 10.4 Advanced Features

- Plotly 3D graphs for time-series visualization
- Motion Canvas for animated process diagrams
- Water shader effects (Babylon.js style)

---

## Phase 11: Supabase Integration

### 11.1 Client Setup

- Frontend: `@supabase/supabase-js`
- Backend: `supabase-py`
- Environment variable configuration

### 11.2 Authentication

- Login/Signup pages
- Protected routes middleware
- Session management

### 11.3 Realtime Subscriptions

- Listen to `sensors` table changes
- Listen to `predictions` table updates
- Auto-update digital twin

---

## Phase 12: Documentation

### 12.1 README.md

- Project overview
- Setup instructions
- Environment variables
- Running locally (no Docker)
- Dataset download instructions
- API documentation link

### 12.2 ARCHITECTURE.md

- System architecture diagram (text/Mermaid)
- Component interactions
- Data flow diagrams
- ML pipeline flow

### 12.3 API_DOCS.md

- All endpoints documented
- Request/response examples
- Authentication requirements

---

## Phase 13: SIH Presentation Generation

### 13.1 Presentation Content (8-12 slides)

1. **Title Slide**: "SIH WATER AI" - Team Nova_Minds
2. **Problem Statement**: Industrial wastewater challenges
3. **Solution Overview**: Multi-model AI + Digital Twin
4. **Architecture**: System diagram
5. **ML Models**: 4 models explanation
6. **Digital Twin**: 3D visualization features
7. **Treatment Optimization**: Primary/Secondary/Tertiary
8. **Results**: Screenshots, metrics
9. **Technology Stack**: All technologies used
10. **Future Scope**: Enhancements
11. **Team**: Nova_Minds
12. **Thank You**

### 13.2 Generation Method

- Use `python-pptx` library
- Auto-generate from templates
- Include placeholder images (user adds screenshots later)
- Output: `docs/SIH_presentation.pptx`

---

## Phase 14: Testing & Validation

### 14.1 Backend Tests

- Unit tests for ML pipeline
- API endpoint tests
- Integration tests

### 14.2 Frontend Tests

- Component rendering tests
- Digital twin interaction tests

### 14.3 End-to-End Flow

- Sensor ingestion → ML prediction → Optimization → Report generation

---

## Implementation Notes

### Dataset 3 (UCI) Manual Addition

- User will manually add Dataset 3 to `backend/data/dataset3/`
- Document this location in README
- Script will detect and process if present

### Environment Variables Required

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `MQTT_BROKER_URL`
- `MQTT_BROKER_PORT`
- `MQTT_USERNAME` (optional)
- `MQTT_PASSWORD` (optional)

### Local Run Commands

```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

---

## File Generation Order

1. Project structure (directories)
2. Configuration files (.env examples, requirements.txt, package.json)
3. Supabase migrations
4. Dataset download scripts
5. ML pipeline code
6. Backend API code
7. PDF report generator
8. MQTT services
9. Frontend pages and components
10. Digital Twin component
11. Documentation
12. SIH presentation script

### To-dos

- [ ] 