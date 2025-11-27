# Node.js Setup Guide for SIH WATER AI

## Problem: Node.js Not Found

If you're getting "node nahi" (Node.js not found), you need to install Node.js first.

## Solution: Install Node.js

### Option 1: Download from Official Website (Recommended)

1. **Visit**: https://nodejs.org/
2. **Download**: LTS version (Long Term Support)
   - For Windows: Download the `.msi` installer
   - Version: 18.x or 20.x (recommended)
3. **Install**:
   - Run the installer
   - Follow the installation wizard
   - Make sure "Add to PATH" is checked
4. **Verify**:
   ```bash
   node --version
   npm --version
   ```

### Option 2: Using Chocolatey (Windows)

If you have Chocolatey installed:
```powershell
choco install nodejs
```

### Option 3: Using Winget (Windows 10/11)

```powershell
winget install OpenJS.NodeJS.LTS
```

## After Installation

1. **Restart Terminal/PowerShell**
   - Close and reopen your terminal
   - This ensures PATH is updated

2. **Verify Installation**:
   ```bash
   node --version
   npm --version
   ```

3. **Install Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

4. **Start Frontend**:
   ```bash
   npm run dev
   ```

## Troubleshooting

### Issue: "node is not recognized"

**Solution:**
1. Restart your terminal/PowerShell
2. Check if Node.js is in PATH:
   ```powershell
   $env:PATH -split ';' | Select-String node
   ```
3. If not found, reinstall Node.js with "Add to PATH" option

### Issue: "npm is not recognized"

**Solution:**
- npm comes with Node.js
- If node works but npm doesn't, reinstall Node.js

### Issue: Permission Errors

**Solution:**
- Run PowerShell as Administrator
- Or use `npm install --global` with admin rights

## Required Versions

- **Node.js**: 18.x or 20.x (LTS)
- **npm**: Comes with Node.js (usually 9.x or 10.x)

## Quick Check Commands

```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# Check if installed correctly
where.exe node
where.exe npm
```

## Next Steps After Installation

1. **Install Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Access Frontend**:
   - Open: http://localhost:3000

---

**Note**: Make sure to restart your terminal after installing Node.js!

