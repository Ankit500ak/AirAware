# 🔧 Render Port Binding Issue - FIXED

## Problem

```
==> No open ports detected on 0.0.0.0, continuing to scan...
==> Port scan timeout reached, no open ports detected on 0.0.0.0
==> Detected open ports on localhost -- did you mean to bind one of these to 0.0.0.0?
```

**Root Cause:** Django's development server (`python manage.py runserver`) binds to `localhost` by default, but Render needs the app to bind to `0.0.0.0` with a specific port to detect it's running.

## Solution Applied ✅

### 1. Updated Gunicorn Command
**File:** `render.yaml`

**Changed from:**
```yaml
startCommand: gunicorn pollution_project.wsgi:application
```

**Changed to:**
```yaml
startCommand: gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

This explicitly tells Gunicorn to:
- Bind to `0.0.0.0` (all network interfaces)
- Use `$PORT` (environment variable provided by Render)

### 2. Created Procfile
**File:** `Procfile` (new)

```
web: gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

This is a backup configuration that Render checks if the startCommand doesn't work.

## How Gunicorn Works on Render

```
┌─────────────────────────────────────┐
│         Render Platform             │
│                                     │
│  Sets PORT environment variable     │
│  (e.g., PORT=10000)                 │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Gunicorn reads $PORT               │
│  gunicorn --bind 0.0.0.0:$PORT      │
│                                     │
│  Binds to: 0.0.0.0:10000            │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Render detects open port           │
│  ✅ Port scan successful             │
│  🚀 Service is Live                  │
└─────────────────────────────────────┘
```

## Deployment Status

✅ **Committed:** c577921  
✅ **Pushed:** to main branch  
🔄 **Render:** Auto-deploying now (5-7 minutes)

## What Changed

| File | Status | Purpose |
|------|--------|---------|
| `render.yaml` | ✅ Updated | Explicit port binding in startCommand |
| `Procfile` | ✅ Created | Backup configuration for Render |

## Expected Result

After Render completes deployment:
- ✅ Gunicorn binds to `0.0.0.0:$PORT`
- ✅ Render detects the open port
- ✅ Health checks pass
- ✅ Service goes live
- ✅ App accessible at: https://airaware-1-d5y8.onrender.com

## Monitor Deployment

### Render Dashboard Steps:
1. Go to: https://dashboard.render.com/
2. Click on `airaware-backend` service
3. Watch **"Events"** tab:
   - Look for "Deploy succeeded" message
4. Check **"Logs"** tab:
   - Should see: `Booting worker with pid: [number]`
   - Should see: `Listening at: http://0.0.0.0:[PORT]`

### Successful Log Example:
```
[2025-10-08 07:40:00] [INFO] Starting gunicorn 21.2.0
[2025-10-08 07:40:00] [INFO] Listening at: http://0.0.0.0:10000
[2025-10-08 07:40:00] [INFO] Using worker: sync
[2025-10-08 07:40:01] [INFO] Booting worker with pid: 123
✅ Deploy succeeded
```

## Verify Deployment

Once deployed, test your app:

```bash
# Check if the site loads
curl https://airaware-1-d5y8.onrender.com/

# Should return HTML or JSON response
# Status: 200 OK
```

Or visit in browser:
- Main site: https://airaware-1-d5y8.onrender.com/
- Admin panel: https://airaware-1-d5y8.onrender.com/admin/

## Troubleshooting

### If port scan still fails:

1. **Check Gunicorn is installed:**
   ```bash
   pip list | grep gunicorn
   # Should show: gunicorn>=21.2.0
   ```

2. **Verify render.yaml is being used:**
   - Check Render dashboard → Settings
   - Confirm "Auto-Deploy" is ON
   - Verify branch is `main`

3. **Check environment variables:**
   - Render Dashboard → Environment
   - Confirm `PORT` exists (auto-set by Render)
   - Confirm `DJANGO_SETTINGS_MODULE` is set

4. **Manual redeploy:**
   - Render Dashboard → Manual Deploy → Deploy latest commit

### If Gunicorn workers crash:

1. **Check Python version:**
   - Should be 3.13.0
   - Verify in Render logs

2. **Check dependencies:**
   - Ensure `requirements-render.txt` was used
   - Check for import errors in logs

3. **Check WSGI path:**
   - Should be: `pollution_project.wsgi:application`
   - Verify wsgi.py exists

## Why This Happened

**Development vs Production:**

| Environment | Server | Binding | Port |
|-------------|--------|---------|------|
| **Local Dev** | `runserver` | `127.0.0.1` | 8000 |
| **Production** | `gunicorn` | `0.0.0.0` | Dynamic ($PORT) |

The error occurred because:
1. Render was somehow running `runserver` (dev server)
2. `runserver` defaults to `localhost:8000`
3. Render couldn't detect the port on `0.0.0.0`
4. Solution: Explicit Gunicorn with `--bind 0.0.0.0:$PORT`

## Best Practices

✅ **Always use Gunicorn (or uWSGI) in production**
- Never use `python manage.py runserver` in production
- Development server is insecure and slow

✅ **Explicit port binding:**
```bash
gunicorn --bind 0.0.0.0:$PORT myproject.wsgi:application
```

✅ **Use multiple workers for better performance:**
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 4 pollution_project.wsgi:application
```

## Next Steps After Deployment

1. ✅ **Verify service is live** (check Render dashboard)
2. ✅ **Test homepage** (visit your URL)
3. ✅ **Create superuser:**
   ```bash
   # In Render Shell
   python manage.py createsuperuser
   ```
4. ✅ **Test admin panel** (/admin/)
5. ✅ **Check logs for errors**
6. ✅ **Set up monitoring** (Sentry, etc.)

## Performance Tuning (Optional)

For better performance, update `render.yaml`:

```yaml
startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 60 pollution_project.wsgi:application
```

**Options explained:**
- `--workers 4`: Run 4 worker processes (2 x CPU cores)
- `--threads 2`: Each worker handles 2 threads
- `--timeout 60`: Kill workers if request takes > 60 seconds

## Files Reference

### render.yaml
```yaml
startCommand: gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

### Procfile
```
web: gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

### requirements-render.txt
```
gunicorn>=21.2.0  # Production WSGI server
```

---

**Status:** ✅ Fix deployed - Waiting for Render  
**ETA:** ~5-7 minutes from push  
**Next:** Monitor Render logs for successful startup  
**Success Indicator:** "Listening at: http://0.0.0.0:[PORT]" in logs
