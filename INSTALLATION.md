# 📦 AirAware Installation Guide

Complete installation guide for setting up the AirAware platform in different environments.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [Environment-Specific Setup](#environment-specific-setup)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Recommended Version |
|----------|----------------|---------------------|
| Python | 3.9+ | 3.11+ |
| Node.js | 16+ | 18+ LTS |
| pip | 21+ | Latest |
| npm | 8+ | Latest |
| Git | 2.30+ | Latest |

### Optional Software (for production)

| Software | Purpose |
|----------|---------|
| PostgreSQL 13+ | Production database |
| Redis 6+ | Caching layer |
| Nginx | Reverse proxy |
| Supervisor | Process management |

---

## Quick Installation

### Minimal Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/Ankit500ak/AirAware.git
cd AirAware

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install minimal dependencies
pip install -r requirements-minimal.txt

# 4. Setup database
python manage.py migrate

# 5. Run server
python manage.py runserver
```

Access at: `http://localhost:8000`

---

## Detailed Installation

### Step 1: System Preparation

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm git
```

#### On macOS:
```bash
brew install python@3.11 node git
```

#### On Windows:
Download and install:
- [Python 3.11+](https://python.org)
- [Node.js 18+ LTS](https://nodejs.org)
- [Git](https://git-scm.com)

### Step 2: Clone Repository

```bash
git clone https://github.com/Ankit500ak/AirAware.git
cd AirAware
```

### Step 3: Backend Setup

#### Create Virtual Environment
```bash
# Create
python -m venv .venv

# Activate
# Linux/macOS:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Windows (CMD):
.venv\Scripts\activate.bat
```

#### Install Python Dependencies

**Option A: Full Installation (Recommended)**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Option B: Minimal Installation**
```bash
pip install -r requirements-minimal.txt
```

**Option C: Development Installation**
```bash
pip install -r requirements-dev.txt
```

**Option D: Production Installation**
```bash
pip install -r requirements-prod.txt
```

#### Configure Environment Variables

Create `.env` file in project root:
```bash
# .env file
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# External API Keys (optional)
WEATHER_API_KEY=your-weather-api-key
AIR_QUALITY_API_KEY=your-air-quality-api-key

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Setup Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

#### Collect Static Files (for production)
```bash
python manage.py collectstatic --noinput
```

### Step 4: Frontend Setup

#### Install Node Dependencies
```bash
npm install
```

#### Configure TailwindCSS
```bash
# Already configured in tailwind.config.js
# No additional setup needed
```

### Step 5: Start Development Servers

#### Terminal 1 - Backend Server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Terminal 2 - Frontend Server (if using React build)
```bash
npm start
```

### Step 6: Verify Installation

Open your browser and navigate to:
- **Main Platform**: http://localhost:8000
- **Dashboard**: http://localhost:3000/dashboard
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

---

## Environment-Specific Setup

### Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Enable debug toolbar
# Add to settings.py:
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Run with auto-reload
python manage.py runserver
```

### Testing Environment

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Production Environment

#### Using Gunicorn + Nginx

```bash
# Install production requirements
pip install -r requirements-prod.txt

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn pollution_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Using Docker

```bash
# Build image
docker build -t airaware:latest .

# Run container
docker run -d \
    -p 8000:8000 \
    -e DEBUG=False \
    -e DATABASE_URL=postgresql://user:pass@host/db \
    --name airaware \
    airaware:latest
```

---

## Database Setup

### SQLite (Development)
Default configuration - no additional setup needed.

### PostgreSQL (Production)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE airaware_db;
CREATE USER airaware_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE airaware_db TO airaware_user;
\q

# Update .env
DATABASE_URL=postgresql://airaware_user:strong_password@localhost/airaware_db
```

### MySQL (Alternative)

```bash
# Install MySQL
sudo apt install mysql-server

# Create database
mysql -u root -p
CREATE DATABASE airaware_db;
CREATE USER 'airaware_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON airaware_db.* TO 'airaware_user'@'localhost';
FLUSH PRIVILEGES;

# Install Python MySQL client
pip install mysqlclient

# Update .env
DATABASE_URL=mysql://airaware_user:strong_password@localhost/airaware_db
```

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'django'

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### 2. Port 8000 already in use

**Solution:**
```bash
# Find process using port 8000
# Linux/macOS:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8080
```

#### 3. Database migrations error

**Solution:**
```bash
# Reset migrations (development only!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

#### 4. Static files not loading

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Ensure STATIC_ROOT is configured in settings.py
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

#### 5. CORS errors in frontend

**Solution:**
```python
# Add to settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Or for development
CORS_ALLOW_ALL_ORIGINS = True
```

#### 6. npm install fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Getting Help

If you encounter issues not covered here:

1. **Check Documentation**: Review README.md and code comments
2. **Search Issues**: Look through [GitHub Issues](https://github.com/Ankit500ak/AirAware/issues)
3. **Create Issue**: Open a new issue with detailed error information
4. **Community Support**: Ask in discussions or contact the team

---

## Verification Checklist

After installation, verify:

- [ ] Backend server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Admin panel loads at http://localhost:8000/admin
- [ ] API responds at http://localhost:8000/api/
- [ ] Frontend dashboard loads (if applicable)
- [ ] Database migrations applied successfully
- [ ] Static files serving correctly
- [ ] Authentication system works (login/signup)
- [ ] No console errors in browser developer tools

---

## Next Steps

After successful installation:

1. **Configure External APIs**: Add API keys for weather and air quality services
2. **Create Test Data**: Use Django admin or management commands
3. **Customize Settings**: Adjust settings.py for your environment
4. **Set Up Monitoring**: Configure logging and error tracking
5. **Read Documentation**: Explore API endpoints and features

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [TailwindCSS Guide](https://tailwindcss.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Deployment Guide](DEPLOYMENT.md)

---

**Last Updated**: October 2025  
**Version**: 1.0.0
