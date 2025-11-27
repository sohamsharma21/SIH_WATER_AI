# SIH WATER AI - Getting Started Guide

## Project Overview

**SIH WATER AI** is an AI-powered Industrial Wastewater Treatment Optimization System featuring:
- ✅ 4 trained ML models for accurate predictions
- ✅ Real-time sensor data ingestion (HTTP & MQTT)
- ✅ 3D digital twin visualization
- ✅ Automated treatment optimization
- ✅ PDF report generation
- ✅ Production-ready deployment

---

## Quick Start (5 minutes)

### Minimum Requirements
- Python 3.11+
- Node.js 18+
- Supabase account (free tier works)

### Step 1: Clone & Setup Environment

```bash
# Navigate to project root
cd PROJECT_SIH

# Create backend .env
echo 'SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
MQTT_BROKER_URL=localhost
MQTT_BROKER_PORT=1883' > backend/.env

# Create frontend .env
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key' > frontend/.env.local
```

### Step 2: Start Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Step 3: Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

### Step 4: Login & Explore

1. Go to http://localhost:3000
2. Sign up with email/password
3. Explore the dashboard
4. Make predictions using the prediction form

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 14)                │
│   - 3D Digital Twin (Three.js/React-Three-Fiber)       │
│   - Real-time Dashboard (Supabase Realtime)            │
│   - ML Prediction Interface                            │
│   - PDF Report Viewer                                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│              Backend (FastAPI)                          │
│   ┌──────────────────────────────────────────────────┐  │
│   │  ML Pipeline                                     │  │
│   │  - 4 Trained Models (Random Forest)             │  │
│   │  - Auto Model Selection                         │  │
│   │  - Ensemble Predictions                         │  │
│   └──────────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────────┐  │
│   │  Treatment Optimization Engine                  │  │
│   │  - Primary/Secondary/Tertiary Stages           │  │
│   │  - AI-driven parameter optimization            │  │
│   │  - Recovery percentage estimation              │  │
│   └──────────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────────┐  │
│   │  Report Generation (ReportLab)                 │  │
│   │  - PDF generation with charts                  │  │
│   │  - Supabase Storage integration                │  │
│   └──────────────────────────────────────────────────┘  │
└────────────────┬───────────────────┬────────────────────┘
                 │                   │
        MQTT     │                   │ REST
                 │                   │
         ┌───────▼───────┐   ┌──────▼──────────┐
         │  MQTT Broker  │   │  Supabase DB    │
         │  (Mosquitto)  │   │  (PostgreSQL)   │
         └───────────────┘   └─────────────────┘
         
Sensor Data    Sensor Data ──► Predictions
(IoT/Devices)                  Reports
                               ML Models
```

---

## Key Features

### 1. ML Models (4 Trained Models)
- **Dataset 1**: NYC Wastewater Treatment
- **Dataset 2**: Water Potability Classification
- **Dataset 3**: UCI Water Treatment (Contamination)
- **Dataset 4**: Melbourne WWTP (BOD/COD Prediction)

### 2. Treatment Optimization
- **Primary Treatment**: Settling time, coagulant dosing
- **Secondary Treatment**: Aeration parameters, DO levels
- **Tertiary Treatment**: Filtration, disinfection, RO trigger
- **Final Reuse**: Determines best reuse type (drinking/industrial/irrigation/environmental)

### 3. Real-time Monitoring
- Live sensor data ingestion
- MQTT integration for IoT devices
- Instant predictions
- Automatic alerts

### 4. Digital Twin
- 3D visualization of treatment plant
- Real-time parameter updates
- Interactive controls
- Animation-based insights

---

## Available Endpoints

### Health & Status
```
GET  /api/v1/health
```

### Sensor Data
```
POST /api/v1/ingest              # Ingest sensor reading
GET  /api/v1/sensors/recent      # Get recent sensors
```

### Predictions
```
POST /api/v1/predict             # Make prediction
GET  /api/v1/predictions/recent  # Get predictions
GET  /api/v1/twin_status         # Digital twin state
```

### Models
```
GET  /api/v1/models              # List available models
POST /api/v1/train/{dataset}     # Train specific model
POST /api/v1/train_all           # Train all models
```

### Reports
```
POST /api/v1/report              # Generate PDF report
```

---

## Configuration

### Environment Variables

**Backend** (backend/.env):
```
SUPABASE_URL          # Your Supabase project URL
SUPABASE_KEY          # Anon key from Supabase
SUPABASE_SERVICE_ROLE_KEY  # Service role key
MQTT_BROKER_URL       # MQTT broker address (default: localhost)
MQTT_BROKER_PORT      # MQTT port (default: 1883)
ENV                   # development or production
FRONTEND_URL          # Frontend URL (for CORS)
```

**Frontend** (frontend/.env.local):
```
NEXT_PUBLIC_API_URL            # Backend API URL
NEXT_PUBLIC_SUPABASE_URL       # Supabase URL
NEXT_PUBLIC_SUPABASE_ANON_KEY  # Supabase anon key
```

---

## Troubleshooting

### "Backend API not responding"
1. Check backend is running: `curl http://localhost:8000/api/v1/health`
2. Verify `NEXT_PUBLIC_API_URL` in frontend/.env.local
3. Check CORS configuration if deployed

### "Supabase connection error"
1. Verify credentials in .env file
2. Check Supabase project is active
3. Run database migrations

### "MQTT connection refused"
1. Start MQTT broker: `docker run -p 1883:1883 eclipse-mosquitto:2.0`
2. Or configure cloud MQTT broker in .env

### "ML models not loading"
1. Check backend/app/models/ directory exists
2. Train models first: `python scripts/train_all_datasets.py`
3. Verify model files have correct naming

---

## Production Deployment

### Using Docker Compose (Recommended)

```bash
# Setup environment
cp backend/.env.example backend/.env
# Edit backend/.env with production credentials

# Build and start
docker-compose up -d

# Check services
docker-compose ps
docker-compose logs -f backend
```

### Manual Deployment

See `docs/PRODUCTION_DEPLOYMENT.md` for comprehensive deployment guide.

---

## Project Structure

```
PROJECT_SIH/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configuration
│   │   ├── api/routes.py      # API endpoints
│   │   ├── ml/                # ML pipeline code
│   │   ├── services/          # Business logic
│   │   └── models/            # Trained models (created at runtime)
│   └── requirements.txt
│
├── frontend/                   # Next.js 14 frontend
│   ├── app/                   # Next.js app router
│   ├── components/            # React components
│   ├── lib/                   # Utilities
│   └── package.json
│
├── migrations/                # Database migrations
├── docs/                      # Documentation
├── scripts/                   # Helper scripts
├── docker-compose.yml         # Docker orchestration
└── Dockerfile.backend         # Backend containerization
    Dockerfile.frontend        # Frontend containerization
```

---

## Testing & Validation

### Run System Validation
```bash
python validate_system.py
```

This validates:
- ✅ Project structure
- ✅ Dependencies
- ✅ Configuration files
- ✅ Documentation

---

## Next Steps

1. **Complete Supabase Setup**
   - Create Supabase account
   - Get API credentials
   - Run migrations

2. **Train ML Models**
   - Download datasets (auto or manual)
   - Run: `python scripts/train_all_datasets.py`

3. **Configure MQTT** (Optional)
   - Setup MQTT broker
   - Configure IoT devices
   - Start sensor ingestion

4. **Customize & Deploy**
   - Modify components
   - Add more models
   - Deploy to production

---

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs (when backend running)
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Production Guide**: See `docs/PRODUCTION_DEPLOYMENT.md`
- **API Reference**: See `docs/API_DOCS.md`

---

## Team

**Team Nova_Minds** - SIH 2024 Project

---

## License

This project is part of Smart India Hackathon 2024

