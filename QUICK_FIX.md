# 🎯 Quick Fix Guide - Visual Steps

## Problem: Render Using Wrong Start Command

Your Render service is running:
```
❌ python manage.py runserver  (WRONG - Development server)
```

It should be running:
```
✅ gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application  (CORRECT - Production server)
```

---

## 🔧 Fix in 5 Easy Steps

### Step 1: Open Render Dashboard
Go to: **https://dashboard.render.com/**

### Step 2: Select Your Service
Click on: **`airaware-backend`** (or whatever you named it)

### Step 3: Go to Settings
- Click **"Settings"** in the left sidebar
- Or click the gear icon ⚙️

### Step 4: Update Start Command
- Scroll down to **"Build & Deploy"** section
- Find **"Start Command"** field
- **DELETE** the old command
- **PASTE** this new command:

```bash
gunicorn --bind 0.0.0.0:$PORT pollution_project.wsgi:application
```

### Step 5: Save and Deploy
1. Scroll to bottom, click **"Save Changes"**
2. Go to top right, click **"Manual Deploy"**
3. Click **"Deploy latest commit"**
4. Wait 5-7 minutes ⏱️

---

## ✅ Success Indicators

### In Render Logs (you should see):
```
✅ [INFO] Starting gunicorn 21.2.0
✅ [INFO] Listening at: http://0.0.0.0:10000
✅ [INFO] Booting worker with pid: 123
✅ Deploy succeeded
✅ Service is live
```

### What You Should NOT See:
```
❌ Running 'python manage.py runserver'
❌ Watching for file changes with StatReloader
❌ No open ports detected on 0.0.0.0
```

---

## 🚀 Test Your Deployment

After deployment succeeds:

**1. Visit your site:**
```
https://airaware-1-d5y8.onrender.com/
```

**2. Check admin:**
```
https://airaware-1-d5y8.onrender.com/admin/
```

**3. Expected result:**
- ✅ Page loads (might show Django default page or your app)
- ✅ No 400/500 errors
- ✅ Admin login page appears

---

## 📋 Checklist

- [ ] Opened Render Dashboard
- [ ] Clicked on airaware-backend service
- [ ] Went to Settings
- [ ] Found "Start Command" field
- [ ] Pasted gunicorn command
- [ ] Clicked "Save Changes"
- [ ] Clicked "Manual Deploy"
- [ ] Waiting for deployment to complete
- [ ] Checked logs for "Listening at" message
- [ ] Tested site URL in browser

---

## ⏰ Timeline

- **Updating settings:** 1-2 minutes
- **Redeployment:** 5-7 minutes
- **Total time:** ~8 minutes

---

## 🆘 If You Get Stuck

### Can't find Start Command field?
- Make sure you're in **Settings** tab (not Overview)
- Scroll down to **"Build & Deploy"** section
- It's between "Build Command" and "Auto-Deploy"

### Save Changes button grayed out?
- Make sure you actually changed the Start Command text
- Try clicking in the field first, then pasting

### Deploy button not appearing?
- It's at the top right of the page
- Says "Manual Deploy" with a rocket icon 🚀
- If not there, refresh the page

### Still seeing runserver in logs?
- Wait for current deploy to fail first
- Clear build cache: Settings → Danger Zone → Clear Build Cache
- Try deploying again

---

## 📞 Need More Help?

Check these files in your repo:
- `RENDER_MANUAL_FIX.md` - Detailed troubleshooting
- `PORT_BINDING_FIX.md` - Technical explanation
- `DEPLOYMENT.md` - Full deployment guide

---

**Remember:** The Render dashboard update is REQUIRED. Pushing code alone won't fix this because Render has cached the old start command!
