# SIH WATER AI - Testing Guide

## Quick Start Testing

### 1. Backend Testing

**Start Backend Server**:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Run Backend Tests**:
```bash
python scripts/test_full_system.py
```

**Manual API Testing**:
- Visit: http://localhost:8000/docs
- Use Swagger UI to test endpoints interactively

### 2. Frontend Testing

**Start Frontend Server**:
```bash
cd frontend
npm run dev
```

**Access Frontend**:
- Landing: http://localhost:3000
- Login: http://localhost:3000/login
- Dashboard: http://localhost:3000/dashboard
- Admin: http://localhost:3000/admin

### 3. End-to-End Testing

**Test Flow**:
1. Start backend (port 8000)
2. Start frontend (port 3000)
3. Login to dashboard
4. Make a prediction using the form
5. Check real-time updates
6. View digital twin

## Test Scenarios

### Scenario 1: Make Prediction
1. Navigate to Dashboard
2. Scroll to "Make New Prediction"
3. Select model (dataset2, dataset3, or dataset4)
4. Enter feature values
5. Click "Make Prediction"
6. Verify results display

### Scenario 2: View Real-time Data
1. Open Dashboard
2. Check Sensor Dashboard section
3. Verify sensor data updates
4. Check Digital Twin visualization

### Scenario 3: Admin Panel
1. Navigate to Admin page
2. View available models
3. Check model metrics
4. Test model training (optional)

## API Endpoint Tests

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Get Models
```bash
curl http://localhost:8000/api/v1/models
```

### Make Prediction
```bash
curl -X POST http://localhost:8000/api/v1/predict_with \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "ph": 7.0,
      "Hardness": 200.0,
      "Solids": 20000.0,
      "Chloramines": 7.0,
      "Sulfate": 300.0,
      "Conductivity": 400.0,
      "Organic_carbon": 10.0,
      "Trihalomethanes": 50.0,
      "Turbidity": 3.0
    },
    "model_name": "dataset2"
  }'
```

### Ingest Sensor Data
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "sensor_001",
    "sensor_type": "pH",
    "parameter_name": "pH",
    "value": 7.2,
    "unit": "pH",
    "location": "Primary Treatment"
  }'
```

## Troubleshooting

### Backend Not Starting
- Check if port 8000 is available
- Verify Python virtual environment is activated
- Check if all dependencies are installed: `pip install -r requirements.txt`

### Frontend Not Starting
- Check if port 3000 is available
- Verify Node.js is installed: `node --version`
- Install dependencies: `npm install`

### API Connection Errors
- Verify backend is running
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Check CORS settings in backend

### Supabase Connection Errors
- Verify Supabase credentials in `.env` files
- Check if Supabase Realtime is enabled
- Verify RLS policies are set correctly

## Expected Results

### Backend Tests
- ✓ Health check returns 200
- ✓ Models endpoint returns model list
- ✓ Predictions work for all 3 models
- ✓ Sensor ingestion succeeds
- ✓ Twin status returns data

### Frontend Tests
- ✓ Dashboard loads without errors
- ✓ Predictions display correctly
- ✓ Real-time updates work
- ✓ Digital twin renders
- ✓ Admin panel shows models

## Performance Benchmarks

- Prediction response time: < 2 seconds
- Dashboard load time: < 3 seconds
- Real-time update latency: < 1 second
- Model loading time: < 5 seconds (on startup)

---

**Last Updated**: November 26, 2025

