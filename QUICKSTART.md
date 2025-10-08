# 🚀 AirAware Quick Start Guide

## One-Command Setup

```bash
# Clone, setup, and run (Unix/Linux/macOS)
git clone https://github.com/Ankit500ak/AirAware.git && cd AirAware && python -m venv .venv && source .venv/bin/activate && pip install -r requirements-minimal.txt && python manage.py migrate && python manage.py runserver
```

```powershell
# For Windows PowerShell
git clone https://github.com/Ankit500ak/AirAware.git; cd AirAware; python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements-minimal.txt; python manage.py migrate; python manage.py runserver
```

## Manual Setup (Step by Step)

### 1️⃣ Get the Code
```bash
git clone https://github.com/Ankit500ak/AirAware.git
cd AirAware
```

### 2️⃣ Setup Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies

**Choose one:**
```bash
pip install -r requirements-minimal.txt    # Quick start (5 packages)
pip install -r requirements.txt            # Full features (40+ packages)
pip install -r requirements-dev.txt        # Development (50+ packages)
pip install -r requirements-prod.txt       # Production (45+ packages)
```

### 4️⃣ Setup Database
```bash
python manage.py migrate
```

### 5️⃣ Run Server
```bash
python manage.py runserver
```

### 6️⃣ Access Application
```
🌐 Main Site:  http://localhost:8000
🔧 Admin:      http://localhost:8000/admin
📊 API:        http://localhost:8000/api/
```

## Optional: Frontend Setup

```bash
npm install                # Install dependencies
npm start                  # Run React dev server (port 3000)
```

## Create Admin User

```bash
python manage.py createsuperuser
# Enter username, email, and password
```

## Package Comparison

| File | Packages | Install Time | Use Case |
|------|----------|--------------|----------|
| `requirements-minimal.txt` | 6 | ~30 sec | Quick testing |
| `requirements.txt` | 40+ | ~2 min | Standard development |
| `requirements-dev.txt` | 50+ | ~3 min | Full development |
| `requirements-prod.txt` | 45+ | ~2.5 min | Production deployment |

## Common Commands

```bash
# Virtual Environment
python -m venv .venv              # Create
source .venv/bin/activate         # Activate (Unix)
.venv\Scripts\activate            # Activate (Windows)
deactivate                        # Deactivate

# Django Management
python manage.py migrate          # Apply database changes
python manage.py makemigrations   # Create migrations
python manage.py createsuperuser  # Create admin user
python manage.py runserver        # Start dev server
python manage.py collectstatic    # Collect static files
python manage.py test             # Run tests

# Package Management
pip install -r requirements.txt   # Install packages
pip freeze > requirements.txt     # Save current packages
pip list                          # List installed packages
pip install --upgrade pip         # Update pip

# Frontend
npm install                       # Install dependencies
npm start                         # Start dev server
npm build                         # Build for production
npm test                          # Run tests
```

## Troubleshooting Quick Fixes

```bash
# Port in use
python manage.py runserver 8080   # Use different port

# Module not found
pip install -r requirements.txt   # Reinstall packages

# Database locked
rm db.sqlite3                     # Delete database
python manage.py migrate          # Recreate

# Permission denied (Unix/Linux)
chmod +x manage.py                # Make executable

# Virtual environment issues
deactivate                        # Deactivate
rm -rf .venv                      # Delete venv
python -m venv .venv              # Recreate
source .venv/bin/activate         # Activate
pip install -r requirements.txt   # Reinstall
```

## Requirements File Breakdown

### requirements-minimal.txt (Essential Only)
```
Django                    # Web framework
djangorestframework       # REST API
django-cors-headers       # CORS support
requests                  # HTTP library
python-dotenv            # Environment variables
gunicorn                 # Production server
```

### requirements.txt (Full Stack)
- All minimal packages +
- Database drivers (PostgreSQL)
- Authentication (JWT, AllAuth)
- Caching (Redis)
- Testing (pytest, coverage)
- Data processing (pandas, numpy)
- API documentation
- Code quality tools

### requirements-dev.txt (Development Tools)
- All standard packages +
- Debug toolbar
- iPython shell
- Advanced testing tools
- Code linters
- Documentation generators

### requirements-prod.txt (Production Optimized)
- All standard packages +
- Production database drivers
- Monitoring tools (Sentry)
- Security packages
- Performance optimization
- Task queue (Celery)

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.9 | 3.11+ |
| **RAM** | 2 GB | 4 GB+ |
| **Disk Space** | 500 MB | 1 GB+ |
| **Node.js** | 16.0 | 18.0+ LTS |
| **OS** | Any | Ubuntu 22.04 LTS |

## Quick Health Check

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check virtual environment
which python  # Should show .venv path

# Check installed packages
pip list

# Test Django installation
python -c "import django; print(django.VERSION)"

# Test server (should return HTML)
curl http://localhost:8000
```

## Environment Variables (.env)

```bash
# Create .env file
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
```

## Next Steps

1. ✅ Server running at http://localhost:8000
2. 📖 Read full [Installation Guide](INSTALLATION.md)
3. 🔧 Create admin user: `python manage.py createsuperuser`
4. 📊 Access admin panel: http://localhost:8000/admin
5. 🚀 Start building!

## Support

- 📖 [Full Installation Guide](INSTALLATION.md)
- 📚 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/Ankit500ak/AirAware/issues)
- 💬 [Discussions](https://github.com/Ankit500ak/AirAware/discussions)

---

**Need Help?** Open an issue on GitHub or check the full [INSTALLATION.md](INSTALLATION.md) guide.
