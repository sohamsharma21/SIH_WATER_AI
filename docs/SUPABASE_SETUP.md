# Supabase Setup Guide for SIH WATER AI

## Step-by-Step Instructions

### 1. Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or Log in
3. Click **"New Project"**
4. Fill in the details:
   - **Name**: SIH WATER AI (or any name you prefer)
   - **Database Password**: Create a strong password (save it securely)
   - **Region**: Choose closest region (e.g., Asia Pacific - Mumbai)
5. Click **"Create new project"**
6. Wait 2-3 minutes for project to be created

### 2. Get Your Project Credentials

Once project is ready:

1. Go to **Settings** (gear icon) → **API**
2. You'll see:
   - **Project URL**: Copy this (looks like `https://xxxxx.supabase.co`)
   - **anon/public key**: Copy this (starts with `eyJ...`)
   - **service_role key**: Copy this (starts with `eyJ...`) - **Keep this secret!**

### 3. Run Database Migrations

1. Go to **SQL Editor** in Supabase dashboard
2. Create a new query
3. Run each migration file in order:

#### Migration 1: Schema
- Open `migrations/schema.sql`
- Copy all SQL code
- Paste in SQL Editor
- Click **"Run"** or press `Ctrl+Enter`

#### Migration 2: Models Table
- Open `migrations/add_models_table.sql`
- Copy all SQL code
- Paste in SQL Editor
- Click **"Run"**

#### Migration 3: RLS Policies
- Open `migrations/rls_policies.sql`
- Copy all SQL code
- Paste in SQL Editor
- Click **"Run"**

### 4. Create Storage Bucket

1. Go to **Storage** in left sidebar
2. Click **"New bucket"**
3. Fill in:
   - **Name**: `reports`
   - **Public bucket**: ✅ **Enable** (check this box)
4. Click **"Create bucket"**

### 5. Verify Setup

Check these tables exist in **Table Editor**:
- ✅ `sensors`
- ✅ `predictions`
- ✅ `models`
- ✅ `reports`

Check Storage:
- ✅ `reports` bucket exists and is public

---

## Next Steps

1. Copy credentials to:
   - `backend/.env`
   - `frontend/.env.local`

2. Follow the instructions in each `.env.example` file to fill in values.

---

## Troubleshooting

### Migration Errors
- Make sure you run migrations in order
- If table already exists, you can skip that migration or delete the table first

### Storage Issues
- Make sure bucket is set to **public**
- Check RLS policies if upload fails

### Connection Issues
- Verify URLs and keys are correct (no extra spaces)
- Check if project is paused (free tier projects pause after inactivity)

