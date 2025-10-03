# Air Quality Views for AirAware Backend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Max, Min, Q
from datetime import timedelta, datetime
import logging

from .models import (
    AirQualityStation, 
    AirQualityReading, 
    UserHealthProfile, 
    AirQualityAlert, 
    AirQualityForecast
)
from .serializers import (
    AirQualityStationSerializer,
    AirQualityReadingSerializer,
    UserHealthProfileSerializer,
    AirQualityAlertSerializer,
    AirQualityForecastSerializer,
)
from .services import AirQualityDataService, HealthRecommendationService

logger = logging.getLogger(__name__)


class AirQualityStationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for air quality monitoring stations"""
    
    queryset = AirQualityStation.objects.filter(is_active=True)
    serializer_class = AirQualityStationSerializer
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get stations near a specific location"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 10))  # Default 10km
        
        if not lat or not lng:
            return Response(
                {'error': 'Latitude and longitude are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simple distance calculation (for more accuracy, use PostGIS)
        nearby_stations = self.queryset.filter(
            latitude__range=(float(lat) - radius/111, float(lat) + radius/111),
            longitude__range=(float(lng) - radius/111, float(lng) + radius/111)
        )
        
        serializer = self.get_serializer(nearby_stations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def current_reading(self, request, pk=None):
        """Get the latest reading for a station"""
        station = self.get_object()
        latest_reading = station.readings.first()
        
        if not latest_reading:
            return Response(
                {'error': 'No readings available for this station'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AirQualityReadingSerializer(latest_reading)
        return Response(serializer.data)


class AirQualityReadingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for air quality readings"""
    
    queryset = AirQualityReading.objects.all()
    serializer_class = AirQualityReadingSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by station
        station_id = self.request.query_params.get('station_id')
        if station_id:
            queryset = queryset.filter(station_id=station_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(measured_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(measured_at__lte=end_date)
        
        # Filter by AQI category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(aqi_category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def current_delhi_aqi(self, request):
        """Get current average AQI for Delhi-NCR"""
        # Get readings from last hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        
        current_readings = self.queryset.filter(
            measured_at__gte=one_hour_ago,
            station__city__icontains='delhi'
        )
        
        if not current_readings.exists():
            return Response(
                {'error': 'No recent data available'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate averages
        avg_data = current_readings.aggregate(
            avg_aqi=Avg('aqi'),
            max_aqi=Max('aqi'),
            min_aqi=Min('aqi'),
            avg_pm25=Avg('pm25'),
            avg_pm10=Avg('pm10')
        )
        
        # Determine overall category
        avg_aqi = int(avg_data['avg_aqi'] or 0)
        category = self._get_aqi_category(avg_aqi)
        
        response_data = {
            'current_aqi': avg_aqi,
            'category': category,
            'max_aqi': avg_data['max_aqi'],
            'min_aqi': avg_data['min_aqi'],
            'avg_pm25': avg_data['avg_pm25'],
            'avg_pm10': avg_data['avg_pm10'],
            'total_stations': current_readings.values('station').distinct().count(),
            'last_updated': timezone.now(),
            'health_message': self._get_health_message(category),
        }
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'])
    def historical_trends(self, request):
        """Get historical AQI trends for analysis"""
        days = int(request.query_params.get('days', 7))
        station_id = request.query_params.get('station_id')
        
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = self.queryset.filter(measured_at__gte=start_date)
        if station_id:
            queryset = queryset.filter(station_id=station_id)
        
        # Group by day and calculate averages
        trends = []
        for i in range(days):
            day_start = start_date + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            day_readings = queryset.filter(
                measured_at__gte=day_start,
                measured_at__lt=day_end
            )
            
            if day_readings.exists():
                day_avg = day_readings.aggregate(
                    avg_aqi=Avg('aqi'),
                    avg_pm25=Avg('pm25'),
                    avg_pm10=Avg('pm10')
                )
                
                trends.append({
                    'date': day_start.date(),
                    'avg_aqi': int(day_avg['avg_aqi'] or 0),
                    'avg_pm25': float(day_avg['avg_pm25'] or 0),
                    'avg_pm10': float(day_avg['avg_pm10'] or 0),
                })
        
        return Response({'trends': trends})
    
    def _get_aqi_category(self, aqi):
        """Helper method to determine AQI category"""
        if aqi <= 50:
            return 'GOOD'
        elif aqi <= 100:
            return 'MODERATE'
        elif aqi <= 150:
            return 'UNHEALTHY_SENSITIVE'
        elif aqi <= 200:
            return 'UNHEALTHY'
        elif aqi <= 300:
            return 'VERY_UNHEALTHY'
        else:
            return 'HAZARDOUS'
    
    def _get_health_message(self, category):
        """Helper method to get health message for AQI category"""
        messages = {
            'GOOD': 'Air quality is good. Great day for outdoor activities!',
            'MODERATE': 'Air quality is moderate. Sensitive individuals should limit outdoor activities.',
            'UNHEALTHY_SENSITIVE': 'Unhealthy for sensitive groups. Children, elderly, and people with respiratory conditions should avoid outdoor activities.',
            'UNHEALTHY': 'Unhealthy air quality. Everyone should limit outdoor activities.',
            'VERY_UNHEALTHY': 'Very unhealthy air quality. Avoid all outdoor activities.',
            'HAZARDOUS': 'Hazardous air quality. Stay indoors and keep windows closed.',
        }
        return messages.get(category, 'Unknown air quality condition.')


class UserHealthProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user health profiles"""
    
    serializer_class = UserHealthProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserHealthProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Get personalized health recommendations"""
        try:
            profile = UserHealthProfile.objects.get(user=request.user)
            
            # Get current AQI for user's location
            current_aqi = AirQualityDataService.get_current_aqi_for_location(
                profile.location_lat, 
                profile.location_lng
            )
            
            # Generate recommendations
            recommendations = HealthRecommendationService.generate_recommendations(
                profile, current_aqi
            )
            
            return Response({
                'current_aqi': current_aqi,
                'recommendations': recommendations,
                'user_profile': self.get_serializer(profile).data
            })
            
        except UserHealthProfile.DoesNotExist:
            return Response(
                {'error': 'Health profile not found. Please create one first.'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class AirQualityAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for air quality alerts"""
    
    serializer_class = AirQualityAlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AirQualityAlert.objects.filter(
            users=self.request.user,
            is_active=True
        )
    
    @action(detail=False, methods=['get'])
    def active_alerts(self, request):
        """Get all active alerts for the user"""
        active_alerts = self.get_queryset().filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
        )
        
        serializer = self.get_serializer(active_alerts, many=True)
        return Response(serializer.data)


class AirQualityForecastViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AQI forecasts"""
    
    queryset = AirQualityForecast.objects.all()
    serializer_class = AirQualityForecastSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by station
        station_id = self.request.query_params.get('station_id')
        if station_id:
            queryset = queryset.filter(station_id=station_id)
        
        # Only return future forecasts
        queryset = queryset.filter(forecast_for__gt=timezone.now())
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def delhi_forecast(self, request):
        """Get 24-hour forecast for Delhi-NCR"""
        hours = int(request.query_params.get('hours', 24))
        
        end_time = timezone.now() + timedelta(hours=hours)
        
        forecasts = self.queryset.filter(
            forecast_for__lte=end_time,
            station__city__icontains='delhi'
        ).select_related('station')
        
        # Group forecasts by hour
        forecast_data = {}
        for forecast in forecasts:
            hour_key = forecast.forecast_for.strftime('%Y-%m-%d %H:00')
            
            if hour_key not in forecast_data:
                forecast_data[hour_key] = []
            
            forecast_data[hour_key].append({
                'station': forecast.station.name,
                'predicted_aqi': forecast.predicted_aqi,
                'confidence': forecast.confidence_score,
                'category': forecast.predicted_category,
            })
        
        # Calculate hourly averages
        hourly_forecast = []
        for hour, station_forecasts in sorted(forecast_data.items()):
            avg_aqi = sum(f['predicted_aqi'] for f in station_forecasts) / len(station_forecasts)
            avg_confidence = sum(f['confidence'] for f in station_forecasts) / len(station_forecasts)
            
            hourly_forecast.append({
                'datetime': hour,
                'predicted_aqi': int(avg_aqi),
                'confidence': round(float(avg_confidence), 1),
                'category': self._get_aqi_category(int(avg_aqi)),
                'stations_count': len(station_forecasts),
            })
        
        return Response({'forecast': hourly_forecast})
    
    def _get_aqi_category(self, aqi):
        """Helper method to determine AQI category"""
        if aqi <= 50:
            return 'GOOD'
        elif aqi <= 100:
            return 'MODERATE'
        elif aqi <= 150:
            return 'UNHEALTHY_SENSITIVE'
        elif aqi <= 200:
            return 'UNHEALTHY'
        elif aqi <= 300:
            return 'VERY_UNHEALTHY'
        else:
            return 'HAZARDOUS'