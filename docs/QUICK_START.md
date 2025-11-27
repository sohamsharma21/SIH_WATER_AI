# Quick Start Guide - SIH WATER AI

## ✅ All Issues Fixed!

### Backend Error: Fixed ✅
- httpx version downgraded to 0.24.1
- Supabase client error handling added

### Frontend Error: Fixed ✅
- `.next` directory deleted (corrupted)
- Cache cleared

## 🚀 Start Application

### Step 1: Start Backend

**Terminal 1**:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Model manager initialized with 3 models
```

### Step 2: Start Frontend

**Terminal 2**:
```bash
cd frontend
npm run dev
```

**Expected Output**:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
```

### Step 3: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔐 Sign Up / Sign In

### Important: Supabase Dashboard Settings

Before using sign up/sign in, configure Supabase:

1. **Go to**: https://supabase.com/dashboard/project/iacnonclyjzheezjuvds/auth/url-configuration

2. **Set Site URL**: `http://localhost:3000`

3. **Add Redirect URLs**:
   - `http://localhost:3000/**`
   - `http://localhost:3000/dashboard`
   - `http://localhost:3000/auth/callback`

4. **Disable Email Confirmation** (for testing):
   - Go to: Authentication → Settings
   - Disable "Enable email confirmations"

### Test Sign Up/Login

1. Visit: http://localhost:3000/signup
2. Create account
3. Should redirect to dashboard (if email confirmation disabled)
4. Or visit: http://localhost:3000/login to login

## 🧪 Test Features

### 1. Make Prediction
- Go to Dashboard
- Scroll to "Make New Prediction"
- Select model (dataset2, dataset3, or dataset4)
- Enter features
- Click "Make Prediction"

### 2. View Real-time Data
- Dashboard automatically shows sensor data
- Digital twin visualization
- Recent predictions

### 3. Admin Panel
- Visit: http://localhost:3000/admin
- View all trained models
- Check model metrics

## 🐛 Troubleshooting

### Backend Not Starting
- Check if port 8000 is available
- Verify virtual environment is activated
- Check `.env` file exists

### Frontend Not Starting
- Delete `.next` directory: `Remove-Item -Recurse -Force .next`
- Clear cache: `Remove-Item -Recurse -Force node_modules/.cache`
- Restart: `npm run dev`

### Sign Up/Login Not Working
- Check Supabase dashboard settings (see above)
- Verify `.env.local` has correct credentials
- Check browser console (F12) for errors
- Try test auth page: http://localhost:3000/test-auth

## 📝 Environment Files

### Backend `.env`:
```env
SUPABASE_URL=https://iacnonclyjzheezjuvds.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### Frontend `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://iacnonclyjzheezjuvds.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:3000
- [ ] Can access http://localhost:8000/docs
- [ ] Sign up works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Can make predictions

---

**Last Updated**: November 26, 2025

