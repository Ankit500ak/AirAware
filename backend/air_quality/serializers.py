# Air Quality Serializers for AirAware Backend

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    AirQualityStation,
    AirQualityReading,
    UserHealthProfile,
    AirQualityAlert,
    AirQualityForecast
)


class AirQualityStationSerializer(serializers.ModelSerializer):
    """Serializer for air quality monitoring stations"""
    
    latest_reading = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = AirQualityStation
        fields = [
            'id', 'name', 'station_type', 'latitude', 'longitude',
            'address', 'city', 'state', 'is_active', 'created_at',
            'latest_reading', 'distance'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_latest_reading(self, obj):
        """Get the latest air quality reading for this station"""
        latest_reading = obj.readings.first()
        if latest_reading:
            return {
                'aqi': latest_reading.aqi,
                'category': latest_reading.aqi_category,
                'pm25': float(latest_reading.pm25) if latest_reading.pm25 else None,
                'pm10': float(latest_reading.pm10) if latest_reading.pm10 else None,
                'measured_at': latest_reading.measured_at,
            }
        return None
    
    def get_distance(self, obj):
        """Calculate distance from user location (if provided in context)"""
        # This would require user location in context
        # Implementation depends on frontend requirements
        return None


class AirQualityReadingSerializer(serializers.ModelSerializer):
    """Serializer for air quality readings"""
    
    station_name = serializers.CharField(source='station.name', read_only=True)
    station_location = serializers.SerializerMethodField()
    health_impact = serializers.SerializerMethodField()
    
    class Meta:
        model = AirQualityReading
        fields = [
            'id', 'station', 'station_name', 'station_location',
            'aqi', 'aqi_category', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3',
            'temperature', 'humidity', 'wind_speed', 'wind_direction', 'pressure',
            'measured_at', 'created_at', 'data_source', 'health_impact'
        ]
        read_only_fields = ['id', 'created_at', 'station_name', 'station_location', 'health_impact']
    
    def get_station_location(self, obj):
        """Get station location details"""
        return {
            'latitude': float(obj.station.latitude),
            'longitude': float(obj.station.longitude),
            'address': obj.station.address,
            'city': obj.station.city
        }
    
    def get_health_impact(self, obj):
        """Get health impact information based on AQI"""
        health_messages = {
            'GOOD': {
                'message': 'Air quality is good for outdoor activities.',
                'color': '#00C851',
                'icon': '😊'
            },
            'MODERATE': {
                'message': 'Moderate air quality. Sensitive individuals should limit prolonged outdoor exertion.',
                'color': '#FFBB33',
                'icon': '😐'
            },
            'UNHEALTHY_SENSITIVE': {
                'message': 'Unhealthy for sensitive groups. Children, elderly, and people with lung/heart conditions should reduce outdoor activities.',
                'color': '#FF8800',
                'icon': '😷'
            },
            'UNHEALTHY': {
                'message': 'Unhealthy air quality. Everyone should limit outdoor activities.',
                'color': '#FF4444',
                'icon': '😨'
            },
            'VERY_UNHEALTHY': {
                'message': 'Very unhealthy. Everyone should avoid outdoor activities.',
                'color': '#CC0000',
                'icon': '🚨'
            },
            'HAZARDOUS': {
                'message': 'Hazardous air quality. Stay indoors and keep windows closed.',
                'color': '#8E24AA',
                'icon': '☠️'
            },
        }
        
        return health_messages.get(obj.aqi_category, {
            'message': 'Unknown air quality level.',
            'color': '#999999',
            'icon': '❓'
        })


class UserHealthProfileSerializer(serializers.ModelSerializer):
    """Serializer for user health profiles"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    risk_level = serializers.SerializerMethodField()
    
    class Meta:
        model = UserHealthProfile
        fields = [
            'user', 'username', 'email', 'health_conditions', 'activity_level',
            'age', 'location_lat', 'location_lng', 'location_name',
            'notifications_enabled', 'alert_threshold', 'risk_level',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'username', 'email', 'created_at', 'updated_at', 'risk_level']
    
    def get_risk_level(self, obj):
        """Calculate risk level based on health conditions and age"""
        risk_score = 0
        
        # Age-based risk
        if obj.age:
            if obj.age >= 65:
                risk_score += 2
            elif obj.age <= 12:
                risk_score += 1.5
        
        # Health condition risk
        high_risk_conditions = ['ASTHMA', 'COPD', 'HEART_DISEASE', 'PREGNANCY']
        for condition in obj.health_conditions:
            if condition in high_risk_conditions:
                risk_score += 2
            elif condition == 'ELDERLY':
                risk_score += 1.5
            elif condition == 'CHILD':
                risk_score += 1
        
        # Activity level adjustment
        if obj.activity_level in ['HIGH', 'ATHLETE']:
            risk_score += 0.5
        
        # Determine risk level
        if risk_score >= 4:
            return 'HIGH'
        elif risk_score >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def validate_health_conditions(self, value):
        """Validate health conditions list"""
        valid_conditions = [choice[0] for choice in UserHealthProfile.HEALTH_CONDITIONS]
        for condition in value:
            if condition not in valid_conditions:
                raise serializers.ValidationError(f"'{condition}' is not a valid health condition.")
        return value


class AirQualityAlertSerializer(serializers.ModelSerializer):
    """Serializer for air quality alerts"""
    
    affected_users_count = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = AirQualityAlert
        fields = [
            'id', 'alert_type', 'severity', 'title', 'message',
            'aqi_value', 'location_lat', 'location_lng', 'location_name',
            'is_active', 'expires_at', 'created_at',
            'affected_users_count', 'time_remaining'
        ]
        read_only_fields = ['id', 'created_at', 'affected_users_count', 'time_remaining']
    
    def get_affected_users_count(self, obj):
        """Get count of users affected by this alert"""
        return obj.users.count()
    
    def get_time_remaining(self, obj):
        """Get time remaining until alert expires"""
        if obj.expires_at:
            from django.utils import timezone
            remaining = obj.expires_at - timezone.now()
            if remaining.total_seconds() > 0:
                hours = remaining.total_seconds() // 3600
                minutes = (remaining.total_seconds() % 3600) // 60
                return f"{int(hours)}h {int(minutes)}m"
            else:
                return "Expired"
        return "No expiration"


class AirQualityForecastSerializer(serializers.ModelSerializer):
    """Serializer for air quality forecasts"""
    
    station_name = serializers.CharField(source='station.name', read_only=True)
    hours_ahead = serializers.SerializerMethodField()
    accuracy_indicator = serializers.SerializerMethodField()
    
    class Meta:
        model = AirQualityForecast
        fields = [
            'id', 'station', 'station_name', 'forecast_for', 'predicted_aqi',
            'confidence_score', 'predicted_category', 'predicted_pm25', 'predicted_pm10',
            'model_version', 'model_type', 'created_at',
            'hours_ahead', 'accuracy_indicator'
        ]
        read_only_fields = ['id', 'created_at', 'station_name', 'hours_ahead', 'accuracy_indicator']
    
    def get_hours_ahead(self, obj):
        """Calculate how many hours ahead this forecast is"""
        from django.utils import timezone
        time_diff = obj.forecast_for - timezone.now()
        return round(time_diff.total_seconds() / 3600, 1)
    
    def get_accuracy_indicator(self, obj):
        """Get accuracy indicator based on confidence score"""
        confidence = float(obj.confidence_score)
        
        if confidence >= 90:
            return {'level': 'HIGH', 'description': 'Very reliable forecast'}
        elif confidence >= 70:
            return {'level': 'MEDIUM', 'description': 'Moderately reliable forecast'}
        elif confidence >= 50:
            return {'level': 'LOW', 'description': 'Less reliable forecast'}
        else:
            return {'level': 'VERY_LOW', 'description': 'Highly uncertain forecast'}


class AirQualityDashboardSerializer(serializers.Serializer):
    """Serializer for dashboard overview data"""
    
    current_aqi = serializers.IntegerField()
    category = serializers.CharField()
    health_message = serializers.CharField()
    dominant_pollutant = serializers.CharField()
    
    # Trend data
    trend_direction = serializers.CharField()  # 'improving', 'worsening', 'stable'
    change_percentage = serializers.FloatField()
    
    # Statistics
    stations_reporting = serializers.IntegerField()
    last_updated = serializers.DateTimeField()
    
    # Forecast
    next_hour_aqi = serializers.IntegerField(allow_null=True)
    forecast_trend = serializers.CharField(allow_null=True)
    
    # Regional breakdown
    area_breakdown = serializers.ListField(
        child=serializers.DictField(), 
        allow_empty=True
    )
    
    def to_representation(self, instance):
        """Custom representation for dashboard data"""
        data = super().to_representation(instance)
        
        # Add color coding based on AQI
        aqi = data.get('current_aqi', 0)
        if aqi <= 50:
            data['color'] = '#00C851'
            data['text_color'] = '#ffffff'
        elif aqi <= 100:
            data['color'] = '#FFBB33'
            data['text_color'] = '#000000'
        elif aqi <= 150:
            data['color'] = '#FF8800'
            data['text_color'] = '#ffffff'
        elif aqi <= 200:
            data['color'] = '#FF4444'
            data['text_color'] = '#ffffff'
        elif aqi <= 300:
            data['color'] = '#CC0000'
            data['text_color'] = '#ffffff'
        else:
            data['color'] = '#8E24AA'
            data['text_color'] = '#ffffff'
        
        return data