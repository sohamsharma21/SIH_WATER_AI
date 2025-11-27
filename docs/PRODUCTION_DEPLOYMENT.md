# SIH WATER AI - Production Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL/Supabase account
- MQTT Broker (local or cloud)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env from .env.example
cp .env.example .env
# Edit .env with your Supabase credentials

# Run migrations on Supabase dashboard
# Execute migrations/schema.sql, migrations/add_models_table.sql, migrations/rls_policies.sql

# Start backend
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env.local from .env.local.example
cp .env.local.example .env.local
# Edit .env.local with your Supabase URL and API URL

npm run dev
```

Visit http://localhost:3000

---

## Docker Deployment

### Using Docker Compose (Recommended for Production)

```bash
# Create .env file with all credentials
cp .env.example .env
# Edit .env with production values

# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Individual Docker Images

```bash
# Build backend image
docker build -f Dockerfile.backend -t sih-water-ai-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t sih-water-ai-frontend:latest .

# Run backend
docker run -p 8000:8000 \
  -e SUPABASE_URL=your_url \
  -e SUPABASE_KEY=your_key \
  sih-water-ai-backend:latest

# Run frontend
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  sih-water-ai-frontend:latest
```

---

## Environment Variables

### Backend (.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
MQTT_BROKER_URL=localhost
MQTT_BROKER_PORT=1883
ENV=production
FRONTEND_URL=https://your-frontend-url.com
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## Database Setup

### 1. Create Supabase Project
- Go to https://supabase.com
- Create new project
- Get URL and API keys

### 2. Run Migrations
Run these SQL files in Supabase SQL Editor in order:
1. `migrations/schema.sql` - Create all tables
2. `migrations/add_models_table.sql` - Add model registry
3. `migrations/rls_policies.sql` - Enable RLS

### 3. Enable Realtime
- Go to Supabase dashboard
- Enable Realtime for tables: sensors, predictions

---

## API Endpoints

All endpoints require the backend to be running.

### Health Check
```
GET /api/v1/health
```

### Sensor Data
```
POST /api/v1/ingest
GET /api/v1/sensors/recent?limit=100
```

### Predictions
```
POST /api/v1/predict
GET /api/v1/predictions/recent?limit=50
```

### Models
```
GET /api/v1/models
POST /api/v1/train/{dataset}
POST /api/v1/train_all
```

### Reports
```
POST /api/v1/report
```

### Digital Twin
```
GET /api/v1/twin_status
```

---

## ML Models Training

### Automatic Training (First Run)
```bash
# Inside backend directory
from app.ml.trainer import train_all
results = train_all()
```

### Manual Training
```bash
from app.ml.trainer import train_on_csv
from pathlib import Path

metadata = train_on_csv(
    "dataset2",
    Path("backend/data/dataset2/water_potability.csv"),
    target_column="Potability"
)
```

### Available Datasets
- dataset1: NYC Wastewater (manual download required)
- dataset2: Water Potability (auto-downloaded via Kaggle)
- dataset3: UCI Water Treatment (manual setup)
- dataset4: Melbourne WWTP (auto-downloaded via Kaggle)

---

## Production Checklist

- [ ] All environment variables configured
- [ ] Database migrations completed
- [ ] Supabase Realtime enabled
- [ ] CORS configured for production domain
- [ ] API rate limiting configured
- [ ] MQTT broker running or cloud broker configured
- [ ] Error logging configured
- [ ] Database backups scheduled
- [ ] Models trained and stored
- [ ] SSL/TLS certificates configured
- [ ] Monitoring and alerting setup
- [ ] Log aggregation configured

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Verify dependencies
pip install -r requirements.txt --upgrade

# Check logs
tail -f app.log
```

### Frontend won't connect to backend
```bash
# Verify backend is running
curl http://localhost:8000/api/v1/health

# Check NEXT_PUBLIC_API_URL in .env.local
# Should match backend URL
```

### Supabase connection errors
```bash
# Verify credentials
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Test connection with curl
curl -H "apikey: $SUPABASE_KEY" \
     https://your-project.supabase.co/rest/v1/sensors?limit=1
```

### MQTT connection issues
```bash
# Test MQTT broker
mosquitto_sub -h localhost -t "plant/sensors/#"

# Check broker running
ps aux | grep mosquitto
```

---

## Scaling Considerations

### For Production Use

1. **Database**: Increase Supabase resources
2. **Backend**: Run multiple instances with load balancer
3. **Frontend**: Deploy to CDN (Vercel, Netlify)
4. **MQTT**: Use cloud broker (AWS IoT, Azure IoT Hub, HiveMQ Cloud)
5. **Storage**: Increase Supabase storage for reports
6. **Caching**: Add Redis for faster queries
7. **Monitoring**: Setup APM (Application Performance Monitoring)

---

## Security

- Keep environment variables secure (use .env files, never commit to git)
- Enable HTTPS/SSL in production
- Implement API key rotation
- Enable RLS policies on Supabase tables
- Add request signing for MQTT
- Regular security updates for dependencies
- Monitor API usage and implement rate limiting
- Enable audit logging

---

## Support & Documentation

- Backend API: See `/docs` endpoint when backend is running
- Architecture: See `docs/ARCHITECTURE.md`
- API Docs: See `docs/API_DOCS.md`
- Quick Start: See `README.md`

