# Deployment Guide for Render

## Quick Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Environment Variables**
   The following will be auto-generated, but you can customize:
   - `SECRET_KEY` - Auto-generated
   - `DEBUG` - Set to `False`
   - `ALLOWED_HOSTS` - Set to `.onrender.com`
   - `DATABASE_URL` - Auto-connected to database

### Option 2: Manual Web Service Setup

1. **Create PostgreSQL Database**
   - In Render Dashboard, click "New" → "PostgreSQL"
   - Name: `airaware-db`
   - Plan: Free
   - Copy the "Internal Database URL"

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your repository
   - Configure:
     ```
     Name: airaware-backend
     Runtime: Python 3
     Build Command: pip install --upgrade pip && pip install -r requirements-render.txt && python manage.py collectstatic --no-input && python manage.py migrate
     Start Command: gunicorn pollution_project.wsgi:application
     ```

3. **Set Environment Variables**
   ```
   PYTHON_VERSION=3.13.0
   DJANGO_SETTINGS_MODULE=pollution_project.settings_production
   SECRET_KEY=[auto-generate-this]
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=[paste-internal-database-url]
   ```

## Troubleshooting Build Errors

### Error: "KeyError: '__version__'"
**Solution:** Use `requirements-render.txt` instead of `requirements.txt` or `requirements-prod.txt`

This minimal requirements file avoids problematic packages that fail to build on Python 3.13.

### Error: "Package compilation failed"
**Cause:** Some packages don't support Python 3.13 yet.

**Solutions:**
1. Use `requirements-render.txt` (already configured with compatible versions)
2. If you need to add packages, ensure they support Python 3.13:
   ```bash
   # Check package compatibility
   pip index versions <package-name>
   ```

3. Pin versions that work:
   ```
   numpy>=2.0.0  # Python 3.13 compatible
   pandas>=2.2.0  # Python 3.13 compatible
   scipy>=1.13.0  # Python 3.13 compatible
   ```

### Error: "ModuleNotFoundError"
Make sure all required packages are in `requirements-render.txt`:
```bash
pip freeze > requirements-check.txt
# Compare with requirements-render.txt
```

### Database Connection Issues
1. Check `DATABASE_URL` is set correctly
2. Ensure `dj-database-url` is in requirements
3. Verify database service is running

### Static Files Not Loading
1. Ensure `whitenoise` is installed
2. Check `STATIC_ROOT` is set in settings
3. Run `python manage.py collectstatic --no-input` in build command

## Post-Deployment

### Create Superuser
```bash
# In Render Shell (Dashboard → Shell tab)
python manage.py createsuperuser
```

### Check Logs
- Go to Render Dashboard
- Click on your service
- View "Logs" tab

### Update Code
```bash
git add .
git commit -m "Update message"
git push origin main
# Render auto-deploys on push
```

## Production Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Database connected (PostgreSQL)
- [ ] Static files collected and served via Whitenoise
- [ ] HTTPS enabled (automatic on Render)
- [ ] Environment variables configured
- [ ] CORS settings updated for frontend domain
- [ ] Database migrations run
- [ ] Superuser created

## Frontend Deployment (React)

### Deploy on Render
1. Create "Static Site"
2. Build Command: `cd air-aware-app && npm install && npm run build`
3. Publish Directory: `air-aware-app/build`

### Or Deploy on Vercel/Netlify
```bash
cd air-aware-app
npm install
npm run build
# Deploy 'build' folder
```

## Architecture on Render

```
┌─────────────────────────────────────┐
│         Render Services             │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────┐      │
│  │   Django Backend         │      │
│  │   (Web Service)          │      │
│  │   - Python 3.13          │      │
│  │   - Gunicorn             │◄─────┼─── HTTPS
│  │   - Port: Auto           │      │
│  └────────┬─────────────────┘      │
│           │                         │
│           ▼                         │
│  ┌──────────────────────────┐      │
│  │   PostgreSQL Database    │      │
│  │   (Free Tier)            │      │
│  └──────────────────────────┘      │
│                                     │
│  ┌──────────────────────────┐      │
│  │   React Frontend         │      │
│  │   (Static Site)          │◄─────┼─── HTTPS
│  │   - Node.js Build        │      │
│  └──────────────────────────┘      │
└─────────────────────────────────────┘
```

## Cost

- **Free Tier Includes:**
  - 750 hours/month Web Service
  - PostgreSQL 1GB storage
  - Static site (unlimited)
  - SSL/HTTPS (included)

## Support

- [Render Documentation](https://render.com/docs)
- [Django on Render Guide](https://render.com/docs/deploy-django)
- Check Render Community for issues

## Quick Commands Reference

```bash
# Local Testing
python manage.py runserver
python manage.py collectstatic
python manage.py migrate

# Check Requirements
pip list
pip check

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Git Deployment
git status
git add .
git commit -m "Message"
git push origin main
```
