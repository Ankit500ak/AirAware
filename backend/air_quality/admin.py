# Air Quality Admin Configuration

from django.contrib import admin
from .models import (
    AirQualityStation,
    AirQualityReading,
    UserHealthProfile,
    AirQualityAlert,
    AirQualityForecast
)


@admin.register(AirQualityStation)
class AirQualityStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'station_type', 'city', 'is_active', 'created_at']
    list_filter = ['station_type', 'city', 'is_active', 'created_at']
    search_fields = ['name', 'address', 'city']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'station_type', 'is_active')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'address', 'city', 'state')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AirQualityReading)
class AirQualityReadingAdmin(admin.ModelAdmin):
    list_display = ['station', 'aqi', 'aqi_category', 'pm25', 'pm10', 'measured_at']
    list_filter = ['aqi_category', 'station__station_type', 'measured_at', 'data_source']
    search_fields = ['station__name', 'station__city']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'measured_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('station', 'measured_at', 'data_source')
        }),
        ('Air Quality Index', {
            'fields': ('aqi', 'aqi_category')
        }),
        ('Pollutants (μg/m³)', {
            'fields': ('pm25', 'pm10', 'no2', 'so2', 'co', 'o3')
        }),
        ('Weather Data', {
            'fields': ('temperature', 'humidity', 'wind_speed', 'wind_direction', 'pressure'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserHealthProfile)
class UserHealthProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_level', 'age', 'location_name', 'notifications_enabled']
    list_filter = ['activity_level', 'notifications_enabled', 'created_at']
    search_fields = ['user__username', 'user__email', 'location_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Health Profile', {
            'fields': ('health_conditions', 'activity_level', 'age')
        }),
        ('Location', {
            'fields': ('location_lat', 'location_lng', 'location_name')
        }),
        ('Notifications', {
            'fields': ('notifications_enabled', 'alert_threshold')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AirQualityAlert)
class AirQualityAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'alert_type', 'severity', 'is_active', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_active', 'created_at']
    search_fields = ['title', 'message', 'location_name']
    readonly_fields = ['id', 'created_at']
    filter_horizontal = ['users']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('alert_type', 'severity', 'title', 'message')
        }),
        ('Air Quality Data', {
            'fields': ('aqi_value',)
        }),
        ('Location', {
            'fields': ('location_lat', 'location_lng', 'location_name')
        }),
        ('Status', {
            'fields': ('is_active', 'expires_at')
        }),
        ('Recipients', {
            'fields': ('users',)
        }),
    )


@admin.register(AirQualityForecast)
class AirQualityForecastAdmin(admin.ModelAdmin):
    list_display = ['station', 'forecast_for', 'predicted_aqi', 'predicted_category', 'confidence_score']
    list_filter = ['predicted_category', 'model_type', 'created_at']
    search_fields = ['station__name', 'station__city']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'forecast_for'
    
    fieldsets = (
        ('Forecast Information', {
            'fields': ('station', 'forecast_for')
        }),
        ('Predictions', {
            'fields': ('predicted_aqi', 'predicted_category', 'confidence_score')
        }),
        ('Pollutant Predictions', {
            'fields': ('predicted_pm25', 'predicted_pm10'),
            'classes': ('collapse',)
        }),
        ('Model Information', {
            'fields': ('model_version', 'model_type'),
            'classes': ('collapse',)
        }),
    )