# Frontend Error Fix - Next.js .next Directory Issue

## Error
```
Error: EINVAL: invalid argument, readlink
path: 'C:\Users\soham\OneDrive\Desktop\PROJECT_SIH\frontend\.next\server\middleware-manifest.json'
```

## Cause
This is a common Windows/OneDrive issue where:
1. The `.next` build directory gets corrupted
2. Symlink issues with OneDrive sync
3. File system permission problems

## Solution

### Quick Fix (Applied)
1. Delete `.next` directory
2. Clear Next.js cache
3. Restart dev server

### Manual Fix Steps

```bash
cd frontend

# Delete .next directory
rm -r .next
# Or on Windows PowerShell:
Remove-Item -Recurse -Force .next

# Clear cache (optional)
rm -r node_modules/.cache

# Restart dev server
npm run dev
```

## Prevention

### Option 1: Exclude .next from OneDrive
1. Right-click on `frontend` folder
2. OneDrive → Choose folders
3. Exclude `.next` folder from sync

### Option 2: Add to .gitignore (Already done)
The `.next` directory should be in `.gitignore` to prevent sync issues.

### Option 3: Use .cursorignore
Add `.next` to `.cursorignore` if using Cursor IDE.

## If Problem Persists

1. **Check OneDrive Sync Status**:
   - Make sure OneDrive is not syncing the `.next` folder
   - Pause OneDrive sync temporarily

2. **Run as Administrator**:
   - Sometimes Windows permissions cause issues
   - Try running PowerShell as Administrator

3. **Check Antivirus**:
   - Some antivirus software blocks Next.js file operations
   - Add exception for `frontend` folder

4. **Reinstall Dependencies**:
   ```bash
   cd frontend
   rm -r node_modules
   npm install
   npm run dev
   ```

## Alternative: Move Project Outside OneDrive

If issues persist, consider moving project to:
- `C:\Projects\PROJECT_SIH` (outside OneDrive)
- This prevents OneDrive sync conflicts

---

**Status**: Fixed by deleting `.next` directory ✅
