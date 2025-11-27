# Supabase Auth Setup Guide

## Issue: Sign In / Sign Up Not Working

### Common Causes:
1. **Email Confirmation Required** - Supabase might be requiring email confirmation
2. **Redirect URLs Not Configured** - Site URL and redirect URLs need to be set
3. **Auth Settings** - Email provider or auth settings might need adjustment

## Steps to Fix:

### 1. Check Supabase Dashboard Auth Settings

Go to: https://supabase.com/dashboard/project/iacnonclyjzheezjuvds/auth/url-configuration

#### Configure Site URL:
- **Site URL**: `http://localhost:3000` (for development)
- **Redirect URLs**: Add these:
  - `http://localhost:3000/**`
  - `http://localhost:3000/dashboard`
  - `http://localhost:3000/auth/callback`

### 2. Disable Email Confirmation (For Development)

Go to: https://supabase.com/dashboard/project/iacnonclyjzheezjuvds/auth/providers

1. Scroll down to **Email Auth**
2. Find **"Confirm email"** toggle
3. **Turn OFF** email confirmation for faster testing
4. Save changes

### 3. Test Auth Flow

1. Open: `http://localhost:3000/test-auth`
2. Try signing up with a test email
3. Check browser console for errors
4. Check Network tab for API calls

### 4. Verify Environment Variables

Make sure `.env.local` has:
```env
NEXT_PUBLIC_SUPABASE_URL=https://iacnonclyjzheezjuvds.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5. Check Browser Console

Open browser DevTools (F12) and check:
- Console tab for errors
- Network tab for failed requests
- Application tab > Cookies for Supabase session

## Quick Test Commands

```bash
# Test Supabase connection
curl https://iacnonclyjzheezjuvds.supabase.co/auth/v1/health

# Check if frontend is running
curl http://localhost:3000
```

## If Still Not Working:

1. **Clear browser cache and cookies**
2. **Restart frontend dev server**
3. **Check Supabase logs**: Dashboard > Logs > Auth
4. **Verify email is not already registered** (try different email)

---

**Updated:** November 25, 2025

