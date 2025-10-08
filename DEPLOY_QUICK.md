# 🚀 Quick Deployment Reference

## ⚡ Fastest Path to Deploy

```bash
# 1. Make sure all changes are committed
git add .
git commit -m "Ready for Render deployment"
git push origin main

# 2. Go to Render Dashboard
# → https://dashboard.render.com/
# → Click "New" → "Blueprint"
# → Connect GitHub repo
# → Deploy!
```

## 📋 Pre-Deployment Checklist

- [ ] All code pushed to GitHub
- [ ] Using `requirements-render.txt` (not requirements.txt)
- [ ] `render.yaml` file exists in root
- [ ] `settings_production.py` configured
- [ ] Database migrations ready

## 🔧 Build Command (if manual setup)
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements-render.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

## 🚀 Start Command (if manual setup)
```bash
gunicorn pollution_project.wsgi:application
```

## 🌍 Environment Variables (Render Dashboard)

| Variable | Value |
|----------|-------|
| `PYTHON_VERSION` | `3.13.0` |
| `DJANGO_SETTINGS_MODULE` | `pollution_project.settings_production` |
| `SECRET_KEY` | Auto-generate ✅ |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | Auto from DB ✅ |

## 📦 Key Files for Deployment

```
air-aware/
├── requirements-render.txt       ← Use this for deployment
├── render.yaml                   ← Auto-config file
├── build.sh                      ← Build script
├── pollution_project/
│   └── settings_production.py   ← Production settings
└── DEPLOYMENT.md                 ← Full guide
```

## ⚠️ Common Errors & Quick Fixes

### Error: KeyError '__version__'
✅ **Fix:** Use `requirements-render.txt` instead of `requirements.txt`

### Error: Module not found
✅ **Fix:** Add missing package to `requirements-render.txt`

### Error: Database connection
✅ **Fix:** Verify `DATABASE_URL` env var is set

### Error: Static files 404
✅ **Fix:** Check `collectstatic` ran in build command

## 🧪 Test After Deployment

1. ✅ Visit your backend URL
2. ✅ Check `/admin` page loads
3. ✅ Create superuser (Shell in Render)
4. ✅ Test API endpoints

## 📱 Create Superuser

```bash
# In Render Dashboard → Your Service → Shell tab
python manage.py createsuperuser
```

## 🔄 Update Deployed App

```bash
git add .
git commit -m "Your update message"
git push origin main
# Render auto-deploys ✨
```

## 💰 Cost

**Free Tier:** 750 hours/month
- Backend: Python web service
- Database: PostgreSQL (1GB)
- Frontend: Static site (unlimited)
- HTTPS: Included

## 📊 Monitoring

**Render Dashboard:**
- Logs tab: Real-time logs
- Metrics: Performance data
- Events: Deployment history

## 🆘 Need Help?

1. Check `DEPLOYMENT.md` for detailed guide
2. Check `BUILD_FIX_SUMMARY.md` for troubleshooting
3. View Render logs for errors
4. Render docs: https://render.com/docs

---

**🎯 Success Indicators:**
- Build: ✅ "Build succeeded"
- Deploy: ✅ "Live"
- Health: ✅ Green checkmark

**Ready to deploy? Go to:** https://dashboard.render.com/
