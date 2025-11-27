# Frontend Setup Guide

## Node.js Status ✅

Node.js is installed:
- **Version**: v22.14.0
- **npm Version**: 10.9.2
- **Location**: C:\Program Files\nodejs\node.exe

## Next Steps

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

This will install all required packages from `package.json`.

### 2. Start Frontend Development Server

```bash
npm run dev
```

The frontend will start on: **http://localhost:3000**

### 3. Access the Application

- **Landing Page**: http://localhost:3000
- **Login**: http://localhost:3000/login
- **Signup**: http://localhost:3000/signup
- **Dashboard**: http://localhost:3000/dashboard (after login)
- **Test Auth**: http://localhost:3000/test-auth

## Common Issues

### Issue: "npm install" fails

**Solution:**
1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```
2. Delete `node_modules` and `package-lock.json`:
   ```bash
   rm -r node_modules
   rm package-lock.json
   ```
3. Reinstall:
   ```bash
   npm install
   ```

### Issue: Port 3000 already in use

**Solution:**
1. Find process using port 3000:
   ```powershell
   netstat -ano | findstr :3000
   ```
2. Kill the process or use different port:
   ```bash
   npm run dev -- -p 3001
   ```

### Issue: "Module not found" errors

**Solution:**
- Make sure you ran `npm install`
- Check if `node_modules` folder exists
- Try deleting `node_modules` and reinstalling

## Quick Start Commands

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

## Environment Variables

Make sure `frontend/.env.local` exists with:
```env
NEXT_PUBLIC_SUPABASE_URL=https://iacnonclyjzheezjuvds.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

**Note**: Make sure backend is also running on port 8000 for full functionality!

