# Air Quality Models for AirAware Backend

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class AirQualityStation(models.Model):
    """Model for air quality monitoring stations"""
    
    STATION_TYPES = [
        ('CPCB', 'Central Pollution Control Board'),
        ('DPCC', 'Delhi Pollution Control Committee'),
        ('NASA', 'NASA Satellite Data'),
        ('IOT', 'IoT Community Sensor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    station_type = models.CharField(max_length=10, choices=STATION_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Delhi')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'air_quality_stations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.station_type})"


class AirQualityReading(models.Model):
    """Model for storing air quality measurements"""
    
    AQI_CATEGORIES = [
        ('GOOD', 'Good (0-50)'),
        ('MODERATE', 'Moderate (51-100)'),
        ('UNHEALTHY_SENSITIVE', 'Unhealthy for Sensitive Groups (101-150)'),
        ('UNHEALTHY', 'Unhealthy (151-200)'),
        ('VERY_UNHEALTHY', 'Very Unhealthy (201-300)'),
        ('HAZARDOUS', 'Hazardous (301+)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station = models.ForeignKey(AirQualityStation, on_delete=models.CASCADE, related_name='readings')
    
    # AQI and Overall Values
    aqi = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    aqi_category = models.CharField(max_length=20, choices=AQI_CATEGORIES)
    
    # Pollutant Concentrations (μg/m³)
    pm25 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # PM2.5
    pm10 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # PM10
    no2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)   # Nitrogen Dioxide
    so2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)   # Sulfur Dioxide
    co = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)    # Carbon Monoxide
    o3 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)    # Ozone
    
    # Weather Data
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_direction = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pressure = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Metadata
    measured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    data_source = models.CharField(max_length=50, default='API')
    
    class Meta:
        db_table = 'air_quality_readings'
        ordering = ['-measured_at']
        indexes = [
            models.Index(fields=['-measured_at']),
            models.Index(fields=['station', '-measured_at']),
            models.Index(fields=['aqi_category']),
        ]
    
    def __str__(self):
        return f"AQI {self.aqi} - {self.station.name} at {self.measured_at}"


class UserHealthProfile(models.Model):
    """Model for user health profiles and preferences"""
    
    HEALTH_CONDITIONS = [
        ('NONE', 'No Health Issues'),
        ('ASTHMA', 'Asthma'),
        ('COPD', 'COPD'),
        ('HEART_DISEASE', 'Heart Disease'),
        ('PREGNANCY', 'Pregnancy'),
        ('ELDERLY', 'Elderly (65+)'),
        ('CHILD', 'Child (Under 12)'),
    ]
    
    ACTIVITY_LEVELS = [
        ('LOW', 'Low Activity'),
        ('MODERATE', 'Moderate Activity'),
        ('HIGH', 'High Activity'),
        ('ATHLETE', 'Athlete'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    health_conditions = models.JSONField(default=list)  # List of health conditions
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS, default='MODERATE')
    age = models.IntegerField(null=True, blank=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    notifications_enabled = models.BooleanField(default=True)
    alert_threshold = models.IntegerField(default=100)  # AQI threshold for alerts
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_health_profiles'
    
    def __str__(self):
        return f"Health Profile - {self.user.username}"


class AirQualityAlert(models.Model):
    """Model for air quality alerts and notifications"""
    
    ALERT_TYPES = [
        ('AQI_THRESHOLD', 'AQI Threshold Exceeded'),
        ('HEALTH_WARNING', 'Health Warning'),
        ('POLLUTION_SPIKE', 'Pollution Spike Detected'),
        ('WEATHER_IMPACT', 'Weather Impact Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='air_quality_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    message = models.TextField()
    aqi_value = models.IntegerField(null=True, blank=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'air_quality_alerts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type} - {self.title}"


class AirQualityForecast(models.Model):
    """Model for AQI predictions and forecasts"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station = models.ForeignKey(AirQualityStation, on_delete=models.CASCADE, related_name='forecasts')
    forecast_for = models.DateTimeField()  # Future datetime for prediction
    predicted_aqi = models.IntegerField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100%
    predicted_category = models.CharField(max_length=20, choices=AirQualityReading.AQI_CATEGORIES)
    
    # Predicted pollutant levels
    predicted_pm25 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    predicted_pm10 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Model metadata
    model_version = models.CharField(max_length=50, default='v1.0')
    model_type = models.CharField(max_length=50, default='ML_ENSEMBLE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'air_quality_forecasts'
        ordering = ['forecast_for']
        indexes = [
            models.Index(fields=['station', 'forecast_for']),
        ]
    
    def __str__(self):
        return f"Forecast AQI {self.predicted_aqi} for {self.station.name} at {self.forecast_for}"