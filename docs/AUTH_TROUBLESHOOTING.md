# Authentication Troubleshooting Guide

## Common Issues & Solutions

### Issue 1: Sign Up Not Working

**Symptoms:**
- Signup form submits but nothing happens
- Error message appears
- User not created

**Solutions:**

1. **Check Supabase Dashboard Settings:**
   - Go to: https://supabase.com/dashboard/project/iacnonclyjzheezjuvds/auth/url-configuration
   - **Site URL**: Should be `http://localhost:3000` (for development)
   - **Redirect URLs**: Add `http://localhost:3000/**`

2. **Disable Email Confirmation (for development):**
   - Go to: Authentication → Settings
   - Find "Enable email confirmations"
   - **Disable it** for testing
   - This allows immediate login after signup

3. **Check Environment Variables:**
   ```bash
   # In frontend/.env.local
   NEXT_PUBLIC_SUPABASE_URL=https://iacnonclyjzheezjuvds.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
   ```

4. **Test with Test Auth Page:**
   - Visit: http://localhost:3000/test-auth
   - Try signup/login there
   - Check console for errors

### Issue 2: Login Not Working

**Symptoms:**
- Login form submits but redirects back to login
- Error: "Invalid login credentials"
- Session not created

**Solutions:**

1. **Verify User Exists:**
   - Go to Supabase Dashboard → Authentication → Users
   - Check if user is created
   - If email confirmation is enabled, user must confirm email first

2. **Check Password:**
   - Password must be at least 6 characters
   - Try resetting password if needed

3. **Check Browser Console:**
   - Open DevTools (F12)
   - Check Console tab for errors
   - Check Network tab for failed requests

4. **Clear Browser Storage:**
   - Open DevTools → Application → Storage
   - Clear Local Storage and Session Storage
   - Try login again

### Issue 3: Session Not Persisting

**Symptoms:**
- Login works but redirects to login page
- Session lost on page refresh
- Dashboard shows "not authenticated"

**Solutions:**

1. **Check Supabase Client Configuration:**
   - Verify `frontend/lib/supabase.ts` uses `createBrowserClient`
   - Check `persistSession: true` is set

2. **Check Dashboard Auth Check:**
   - Verify `frontend/app/dashboard/page.tsx` checks session correctly
   - Check if auth state listener is set up

3. **Check CORS Settings:**
   - In Supabase Dashboard → Settings → API
   - Verify CORS is enabled for your domain

### Issue 4: Email Confirmation Required

**Symptoms:**
- Signup succeeds but login fails
- Message: "Email not confirmed"

**Solutions:**

1. **For Development (Disable Email Confirmation):**
   - Supabase Dashboard → Authentication → Settings
   - Disable "Enable email confirmations"

2. **For Production (Keep Enabled):**
   - User must click confirmation link in email
   - Check spam folder
   - Resend confirmation email from Supabase Dashboard

### Quick Fix Checklist

- [ ] Supabase credentials in `.env.local`
- [ ] Site URL set to `http://localhost:3000`
- [ ] Redirect URLs include `http://localhost:3000/**`
- [ ] Email confirmation disabled (for dev)
- [ ] Browser console checked for errors
- [ ] Test auth page tried: `/test-auth`
- [ ] Browser storage cleared
- [ ] Frontend server restarted after .env changes

### Testing Steps

1. **Test Signup:**
   ```
   - Go to /signup
   - Enter email and password (min 6 chars)
   - Click Sign Up
   - Check browser console for errors
   - Check Supabase Dashboard → Users for new user
   ```

2. **Test Login:**
   ```
   - Go to /login
   - Enter credentials
   - Click Login
   - Should redirect to /dashboard
   - Check browser console for errors
   ```

3. **Test Session:**
   ```
   - After login, refresh page
   - Should stay on dashboard
   - If redirected to login, session not persisting
   ```

### Debug Commands

**Check Supabase Connection:**
```javascript
// In browser console
import { supabase } from '@/lib/supabase'
supabase.auth.getSession().then(console.log)
```

**Check Environment Variables:**
```javascript
// In browser console
console.log('URL:', process.env.NEXT_PUBLIC_SUPABASE_URL)
console.log('Key:', process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? 'Set' : 'Missing')
```

### Still Not Working?

1. Check Supabase Dashboard → Logs for errors
2. Check browser Network tab for failed requests
3. Try the test auth page: `/test-auth`
4. Verify Supabase project is active
5. Check if RLS policies allow auth operations

---

**Last Updated**: November 26, 2025

