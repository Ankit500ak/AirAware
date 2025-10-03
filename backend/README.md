# 🌬️ AirAware Backend - Django REST API

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

**🚀 Comprehensive Air Quality Management Backend**

RESTful API backend for Delhi-NCR air quality monitoring, health recommendations, and policy analytics.

</div>

---

## 📋 Overview

The AirAware Backend provides a robust, scalable API for air quality data management. Built with Django and Django REST Framework, it handles real-time air quality monitoring, health analytics, forecasting, and policy management for the Delhi-NCR region.

### 🎯 Key Features
- **Real-time AQI Data** - Live air quality readings from 47+ monitoring stations
- **Health Recommendations** - Personalized health advice based on user profiles and AQI
- **Forecasting Engine** - 72-hour AQI predictions using ML models
- **Policy Analytics** - Government-grade data analysis and intervention tools
- **Geospatial Services** - Location-based air quality and route optimization

---

## 🏗️ Architecture

### 📱 Django Apps Structure
```
backend/
├── airaware_backend/          # Main project configuration
├── air_quality/              # Core air quality management
├── users/                    # User authentication & profiles
├── policy_hub/               # Government analytics & policy tools
├── safe_routes/              # Route optimization & navigation
└── requirements.txt          # Python dependencies
```

### 🗄️ Core Models
- **AirQualityStation** - Monitoring station information
- **AirQualityReading** - Real-time AQI and pollutant data
- **UserHealthProfile** - Personalized health conditions and preferences
- **AirQualityAlert** - Health and pollution alerts
- **AirQualityForecast** - ML-based AQI predictions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Django 5.2+
- PostgreSQL (recommended) or SQLite for development
- Redis (for caching and background tasks)

### Installation

1. **Clone and Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the API**
   - API Root: `http://localhost:8000/api/`
   - Admin Panel: `http://localhost:8000/admin/`
   - Health Check: `http://localhost:8000/health/`

---

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=airaware_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# API Keys
NASA_API_KEY=your_nasa_api_key
CPCB_API_KEY=your_cpcb_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 📡 API Endpoints

### 🌬️ Air Quality Endpoints

#### Stations
```http
GET /api/air-quality/stations/                    # List all stations
GET /api/air-quality/stations/nearby/             # Nearby stations
GET /api/air-quality/stations/{id}/               # Station details
GET /api/air-quality/stations/{id}/current_reading/ # Latest reading
```

#### Readings
```http
GET /api/air-quality/readings/                    # List readings
GET /api/air-quality/readings/current_delhi_aqi/  # Current Delhi AQI
GET /api/air-quality/readings/historical_trends/  # Historical data
```

#### Health Profiles
```http
GET /api/air-quality/health-profiles/             # User health profiles
POST /api/air-quality/health-profiles/            # Create profile
GET /api/air-quality/health-profiles/recommendations/ # Personalized recommendations
```

#### Alerts & Forecasts
```http
GET /api/air-quality/alerts/                      # Air quality alerts
GET /api/air-quality/alerts/active_alerts/        # Active user alerts
GET /api/air-quality/forecasts/                   # AQI forecasts
GET /api/air-quality/forecasts/delhi_forecast/    # Delhi 24h forecast
```

---

## 🏥 Health Recommendation System

### Risk Assessment Algorithm
```python
risk_score = base_aqi_risk * health_condition_multiplier * age_factor

Categories:
- LOW (1-1.5): Minimal health risk
- MODERATE (1.5-2.5): Some risk for sensitive individuals  
- HIGH (2.5-3.5): Increased health risk, take precautions
- VERY_HIGH (3.5-4.5): Significant health risk, limit exposure
- EXTREME (4.5+): Extreme health risk, avoid outdoor exposure
```

### Health Conditions Support
- Asthma & Respiratory conditions
- Heart disease & Cardiovascular conditions
- Pregnancy considerations
- Elderly (65+) and Children (≤12) adjustments
- Activity level personalization

---

## 🛰️ Data Sources Integration

### Supported APIs
- **CPCB (Central Pollution Control Board)** - Official Indian government data
- **NASA MODIS** - Satellite atmospheric monitoring
- **OpenWeatherMap** - Weather data correlation
- **IoT Sensor Networks** - Community-contributed data

### Data Processing Pipeline
1. **Collection** - Automated API polling every 30 minutes
2. **Validation** - Data quality checks and anomaly detection
3. **Storage** - Structured database storage with indexing
4. **Analysis** - Real-time calculations and trend analysis
5. **Forecasting** - ML model predictions for future AQI

---

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app tests
python manage.py test air_quality

# Coverage report
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Structure
```
air_quality/
├── tests/
│   ├── test_models.py        # Model tests
│   ├── test_views.py         # API endpoint tests
│   ├── test_services.py      # Business logic tests
│   └── test_serializers.py   # Data serialization tests
```

---

## 📊 Database Schema

### Core Tables
```sql
-- Air Quality Stations
air_quality_station
├── id, name, station_type
├── latitude, longitude, address
├── city, state, is_active
└── created_at, updated_at

-- Air Quality Readings
air_quality_reading
├── station_id (FK), measured_at
├── aqi, aqi_category
├── pm25, pm10, no2, so2, co, o3
├── temperature, humidity, wind_speed
└── data_source, created_at

-- User Health Profiles  
user_health_profile
├── user_id (FK), health_conditions
├── activity_level, age
├── location_lat, location_lng
├── notifications_enabled, alert_threshold
└── created_at, updated_at
```

---

## 🔒 Security Features

### Authentication & Authorization
- **JWT Authentication** - Secure token-based auth
- **Permission Classes** - Role-based access control
- **Rate Limiting** - API throttling for abuse prevention
- **CORS Configuration** - Cross-origin request security

### Data Protection
- **Environment Variables** - Secure credential management
- **Input Validation** - Comprehensive data sanitization
- **SQL Injection Prevention** - Django ORM protection
- **XSS Protection** - Built-in Django security middleware

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure PostgreSQL database
- [ ] Set up Redis for caching
- [ ] Configure static file serving
- [ ] Set up SSL certificates
- [ ] Configure logging and monitoring

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "airaware_backend.wsgi:application"]
```

### Environment-Specific Settings
```bash
# Development
python manage.py runserver 0.0.0.0:8000

# Production
gunicorn airaware_backend.wsgi:application --bind 0.0.0.0:8000
```

---

## 📈 Performance Optimization

### Caching Strategy
- **Redis Caching** - API response caching (15-minute TTL)
- **Database Indexing** - Optimized queries for large datasets
- **Pagination** - Efficient data retrieval with pagination
- **Query Optimization** - select_related and prefetch_related usage

### Monitoring & Logging
- **Structured Logging** - JSON-formatted logs for analysis
- **Performance Metrics** - Response time and database query tracking
- **Error Tracking** - Comprehensive error reporting and alerts

---

## 🤝 Contributing

### Development Workflow
1. **Fork & Clone** the repository
2. **Create Feature Branch** (`git checkout -b feature/amazing-feature`)
3. **Install Dependencies** (`pip install -r requirements.txt`)
4. **Run Tests** (`python manage.py test`)
5. **Make Changes** with proper testing
6. **Submit Pull Request** with detailed description

### Code Standards
- **PEP 8** - Python style guide compliance
- **Type Hints** - Use Python type annotations
- **Documentation** - Comprehensive docstrings
- **Testing** - Minimum 80% code coverage

---

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI** - `/api/docs/` (when configured)
- **ReDoc** - `/api/redoc/` (alternative documentation)
- **Postman Collection** - Available in `/docs/api/`

### Response Formats
```json
{
  "success": true,
  "data": {
    "current_aqi": 294,
    "category": "VERY_UNHEALTHY",
    "health_message": "Very unhealthy. Everyone should avoid outdoor activities.",
    "recommendations": ["Stay indoors", "Use air purifiers"]
  },
  "timestamp": "2024-10-03T10:30:00Z"
}
```

---

## 🔧 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check PostgreSQL service
sudo service postgresql status

# Reset database
python manage.py flush
python manage.py migrate
```

**API Key Issues**
```bash
# Verify environment variables
python manage.py shell
from django.conf import settings
print(settings.NASA_API_KEY)
```

**CORS Issues**
```python
# Update CORS_ALLOWED_ORIGINS in settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 📞 Support

For backend-specific issues:
- 🐛 **Issues**: [GitHub Issues](https://github.com/Ankit500ak/AirAware/issues)
- 📧 **Backend Support**: [backend@airaware.in](mailto:backend@airaware.in)
- 💬 **Technical Discussions**: [GitHub Discussions](https://github.com/Ankit500ak/AirAware/discussions)

---

<div align="center">

**🌬️ Building Clean Air Intelligence for Delhi-NCR 🏙️**

*Backend infrastructure powering the AirAware platform*

</div>