# Sign Up / Sign In Fix Guide

## Current Issue
Sign up and sign in are not working.

## Step-by-Step Fix

### Step 1: Verify Environment Variables

Check `frontend/.env.local` file exists and has:

```env
NEXT_PUBLIC_SUPABASE_URL=https://iacnonclyjzheezjuvds.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlhY25vbmNseWp6aGVlemp1dmRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5NzMxODUsImV4cCI6MjA3OTU0OTE4NX0.vjNy4AsnpPUrUvO3UICk5wbG9NhNufNk94VngjClK7U
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Important**: After changing `.env.local`, **restart the frontend server**!

### Step 2: Configure Supabase Dashboard

Go to: https://supabase.com/dashboard/project/iacnonclyjzheezjuvds

#### A. Authentication → URL Configuration

1. **Site URL**: 
   - Set to: `http://localhost:3000`
   - This is your frontend URL

2. **Redirect URLs**:
   - Add: `http://localhost:3000/**`
   - Add: `http://localhost:3000/dashboard`
   - Add: `http://localhost:3000/auth/callback`

#### B. Authentication → Settings

1. **Enable email confirmations**: 
   - **DISABLE** for development/testing
   - This allows immediate login after signup
   - For production, keep it enabled

2. **Enable email change confirmations**: 
   - Can be disabled for testing

### Step 3: Test Authentication

#### Option A: Use Test Auth Page

1. Start frontend: `cd frontend && npm run dev`
2. Visit: http://localhost:3000/test-auth
3. Try signup/login there
4. Check browser console (F12) for errors

#### Option B: Use Browser Console

Open browser console (F12) and run:

```javascript
// Check Supabase config
console.log('URL:', process.env.NEXT_PUBLIC_SUPABASE_URL)
console.log('Key:', process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? 'Set' : 'Missing')

// Test signup
const { supabase } = await import('/lib/supabase')
const { data, error } = await supabase.auth.signUp({
  email: 'test@example.com',
  password: 'test123456'
})
console.log('Signup:', { data, error })
```

### Step 4: Common Issues & Solutions

#### Issue 1: "Invalid API key"

**Solution**:
- Check `.env.local` has correct `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Restart frontend server after changing `.env.local`
- Clear browser cache

#### Issue 2: "Email already registered"

**Solution**:
- Go to Supabase Dashboard → Authentication → Users
- Delete the test user
- Or use a different email

#### Issue 3: "Email confirmation required"

**Solution**:
- Go to Supabase Dashboard → Authentication → Settings
- Disable "Enable email confirmations"
- Or check your email for confirmation link

#### Issue 4: "Redirect URL mismatch"

**Solution**:
- Go to Supabase Dashboard → Authentication → URL Configuration
- Add `http://localhost:3000/**` to Redirect URLs
- Make sure Site URL is `http://localhost:3000`

#### Issue 5: Session not persisting

**Solution**:
- Clear browser localStorage:
  ```javascript
  // In browser console
  localStorage.clear()
  sessionStorage.clear()
  ```
- Try login again
- Check if cookies are enabled

### Step 5: Debug Checklist

- [ ] `.env.local` file exists in `frontend/` directory
- [ ] Environment variables are set correctly
- [ ] Frontend server restarted after `.env.local` changes
- [ ] Supabase Site URL is `http://localhost:3000`
- [ ] Redirect URLs include `http://localhost:3000/**`
- [ ] Email confirmation is disabled (for testing)
- [ ] Browser console checked for errors (F12)
- [ ] Network tab checked for failed requests
- [ ] Test auth page tried: `/test-auth`

### Step 6: Manual Test

1. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open Browser**:
   - Go to: http://localhost:3000/signup
   - Open DevTools (F12) → Console tab

3. **Try Signup**:
   - Enter email: `test@example.com`
   - Enter password: `test123456` (min 6 chars)
   - Click "Sign Up"
   - Watch console for errors

4. **Check Result**:
   - If success: Should redirect to `/dashboard` or show success message
   - If error: Check console for error message

### Step 7: Verify in Supabase Dashboard

After signup attempt:

1. Go to: https://supabase.com/dashboard/project/iacnonclyjzheezjuvds/auth/users
2. Check if new user appears
3. If user exists but can't login:
   - Check if email is confirmed
   - Check user metadata

## Quick Fix Commands

```bash
# 1. Check environment variables
cd frontend
cat .env.local

# 2. Restart frontend (if .env.local changed)
# Stop current server (Ctrl+C)
npm run dev

# 3. Clear browser storage
# Open browser console (F12) and run:
localStorage.clear()
sessionStorage.clear()
```

## Still Not Working?

1. **Check Supabase Logs**:
   - Dashboard → Logs → API
   - Look for authentication errors

2. **Check Browser Network Tab**:
   - F12 → Network tab
   - Try signup/login
   - Look for failed requests (red)
   - Check request/response details

3. **Test with curl**:
   ```bash
   curl -X POST 'https://iacnonclyjzheezjuvds.supabase.co/auth/v1/signup' \
     -H "apikey: YOUR_ANON_KEY" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123456"}'
   ```

4. **Contact Support**:
   - Share error messages from console
   - Share Supabase dashboard settings screenshot

---

**Last Updated**: November 26, 2025

