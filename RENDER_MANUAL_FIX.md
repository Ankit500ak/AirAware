# 🚨 URGENT: Manual Render Dashboard Fix Required

## Problem
Render is running `python manage.py runserver` instead of `gunicorn` because it cached the old start command.

## ✅ SOLUTION: Update Start Command in Render Dashboard

### Step-by-Step Instructions:

#### 1. Go to Render Dashboard
🔗 https://dashboard.render.com/

#### 2. Click on your `airaware-backend` service

#### 3. Click on **"Settings"** tab (left sidebar)

#### 4. Scroll down to **"Build & Deploy"** section

#### 5. Find **"Start Command"** field

#### 6. Replace the current command with:
```bash
gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

#### 7. Click **"Save Changes"** button at the bottom

#### 8. Go back to **"Manual Deploy"** (top right)

#### 9. Click **"Deploy latest commit"** button

---

## Alternative: Delete and Recreate Service with render.yaml

If updating doesn't work, do this:

### Option A: Using Blueprint (Recommended)

1. **Delete existing service:**
   - Go to your service → Settings → Danger Zone
   - Click "Delete Web Service"
   - Confirm deletion

2. **Create new service from Blueprint:**
   - Dashboard → New → Blueprint
   - Connect your GitHub repo
   - Render auto-detects `render.yaml`
   - Click "Apply"

### Option B: Manual Service Creation

1. **Create Web Service:**
   - Dashboard → New → Web Service
   - Connect GitHub repo: `Ankit500ak/AirAware`
   - Branch: `main`

2. **Configure:**
   ```
   Name: airaware-backend
   Runtime: Python 3
   Build Command: pip install --upgrade pip setuptools wheel && pip install -r requirements-render.txt && python manage.py collectstatic --no-input && python manage.py migrate
   Start Command: gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
   ```

3. **Environment Variables:**
   ```
   PYTHON_VERSION = 3.13.0
   DJANGO_SETTINGS_MODULE = pollution_project.settings
   SECRET_KEY = [auto-generate]
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com,airaware-1-d5y8.onrender.com,localhost
   DATABASE_URL = [from database]
   ```

4. **Click "Create Web Service"**

---

## ⚠️ Important Notes

### Why This Happened:
- Render **caches** the start command from initial service creation
- Even if you push `render.yaml`, old services don't auto-update
- You must **manually update** in dashboard OR recreate the service

### What NOT to Do:
❌ Don't use `python manage.py runserver` in production
❌ Don't bind to `localhost` or `127.0.0.1`
❌ Don't forget the `--bind 0.0.0.0:$PORT` flag

### What TO Do:
✅ Always use Gunicorn for production
✅ Bind to `0.0.0.0:$PORT` for Render
✅ Use `render.yaml` for new services
✅ Update dashboard settings for existing services

---

## Verification After Update

### 1. Check Logs (should see):
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123
```

### 2. Check Events (should see):
```
✅ Deploy succeeded
✅ Service is live
```

### 3. Test in Browser:
- Visit: https://airaware-1-d5y8.onrender.com/
- Should load without errors
- Check: https://airaware-1-d5y8.onrender.com/admin/

---

## Quick Command Reference

### Correct Start Command:
```bash
gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

### With Performance Options:
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 pollution_project.wsgi:application
```

### For Debugging (temporary):
```bash
gunicorn --bind 0.0.0.0:$PORT --log-level debug pollution_project.wsgi:application
```

---

## Troubleshooting After Fix

### If still seeing "runserver" in logs:
1. Clear Render cache: Settings → Danger Zone → Clear Build Cache
2. Trigger new deploy: Manual Deploy → Deploy latest commit
3. Check Start Command in Settings (verify it saved correctly)

### If Gunicorn starts but crashes:
1. Check Python version: Should be 3.13.0
2. Check DJANGO_SETTINGS_MODULE: Should be `pollution_project.settings`
3. Check WSGI path: Should be `pollution_project.wsgi:application`
4. View full error in Logs tab

### If port still not detected:
1. Verify command has `--bind 0.0.0.0:$PORT`
2. Check $PORT variable exists (auto-set by Render)
3. Try adding --log-level debug to see what port Gunicorn binds to

---

## Summary

🎯 **Action Required:** Go to Render Dashboard NOW and update the Start Command manually.

📍 **Where:** Dashboard → Your Service → Settings → Start Command

🔧 **Change To:** `gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application`

💾 **Save & Deploy:** Click "Save Changes" then "Manual Deploy"

⏱️ **Time:** 2 minutes to update, 5-7 minutes to redeploy

---

**Priority:** 🔴 HIGH - Your service won't work until this is fixed!
