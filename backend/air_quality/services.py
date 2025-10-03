# Air Quality Data Services for AirAware Backend

import requests
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from decimal import Decimal
import json

from .models import AirQualityStation, AirQualityReading, UserHealthProfile

logger = logging.getLogger(__name__)


class AirQualityDataService:
    """Service for fetching and processing air quality data from external APIs"""
    
    # API endpoints
    CPCB_API_BASE = "https://api.cpcb.gov.in/air-quality"
    NASA_MODIS_API = "https://modis.gsfc.nasa.gov/data"
    OPENWEATHER_API = "https://api.openweathermap.org/data/2.5"
    
    @classmethod
    def fetch_cpcb_data(cls) -> List[Dict]:
        """Fetch air quality data from CPCB API"""
        try:
            api_key = getattr(settings, 'CPCB_API_KEY', None)
            if not api_key:
                logger.warning("CPCB API key not configured")
                return []
            
            url = f"{cls.CPCB_API_BASE}/current"
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Fetched {len(data.get('stations', []))} CPCB stations data")
            
            return data.get('stations', [])
            
        except requests.RequestException as e:
            logger.error(f"Error fetching CPCB data: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in CPCB data fetch: {str(e)}")
            return []
    
    @classmethod
    def fetch_nasa_modis_data(cls, lat: float, lng: float, date: str = None) -> Optional[Dict]:
        """Fetch satellite data from NASA MODIS API"""
        try:
            api_key = getattr(settings, 'NASA_API_KEY', None)
            if not api_key:
                logger.warning("NASA API key not configured")
                return None
            
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            
            url = f"{cls.NASA_MODIS_API}/aerosol"
            params = {
                'lat': lat,
                'lng': lng,
                'date': date,
                'api_key': api_key
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Fetched NASA MODIS data for location ({lat}, {lng})")
            
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching NASA MODIS data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in NASA MODIS data fetch: {str(e)}")
            return None
    
    @classmethod
    def fetch_weather_data(cls, lat: float, lng: float) -> Optional[Dict]:
        """Fetch weather data from OpenWeatherMap API"""
        try:
            api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
            if not api_key:
                logger.warning("OpenWeatherMap API key not configured")
                return None
            
            url = f"{cls.OPENWEATHER_API}/weather"
            params = {
                'lat': lat,
                'lon': lng,
                'appid': api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Fetched weather data for location ({lat}, {lng})")
            
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in weather data fetch: {str(e)}")
            return None
    
    @classmethod
    def process_and_store_readings(cls, station_data: List[Dict]) -> int:
        """Process and store air quality readings from API data"""
        stored_count = 0
        
        for station_info in station_data:
            try:
                # Get or create station
                station, created = AirQualityStation.objects.get_or_create(
                    name=station_info.get('name', ''),
                    station_type=station_info.get('type', 'CPCB'),
                    defaults={
                        'latitude': Decimal(str(station_info.get('latitude', 0))),
                        'longitude': Decimal(str(station_info.get('longitude', 0))),
                        'address': station_info.get('address', ''),
                        'city': station_info.get('city', 'Delhi'),
                        'state': station_info.get('state', 'Delhi'),
                    }
                )
                
                if created:
                    logger.info(f"Created new station: {station.name}")
                
                # Process readings
                for reading_data in station_info.get('readings', []):
                    aqi = reading_data.get('aqi', 0)
                    category = cls._calculate_aqi_category(aqi)
                    
                    # Create reading
                    reading = AirQualityReading.objects.create(
                        station=station,
                        aqi=aqi,
                        aqi_category=category,
                        pm25=reading_data.get('pm25'),
                        pm10=reading_data.get('pm10'),
                        no2=reading_data.get('no2'),
                        so2=reading_data.get('so2'),
                        co=reading_data.get('co'),
                        o3=reading_data.get('o3'),
                        temperature=reading_data.get('temperature'),
                        humidity=reading_data.get('humidity'),
                        wind_speed=reading_data.get('wind_speed'),
                        wind_direction=reading_data.get('wind_direction'),
                        pressure=reading_data.get('pressure'),
                        measured_at=timezone.make_aware(
                            datetime.fromisoformat(reading_data.get('timestamp'))
                        ) if reading_data.get('timestamp') else timezone.now(),
                        data_source=reading_data.get('source', 'API')
                    )
                    
                    stored_count += 1
                    
            except Exception as e:
                logger.error(f"Error processing station data: {str(e)}")
                continue
        
        logger.info(f"Stored {stored_count} new readings")
        return stored_count
    
    @classmethod
    def get_current_aqi_for_location(cls, lat: float, lng: float, radius_km: float = 10) -> Optional[int]:
        """Get current AQI for a specific location"""
        try:
            # Use cache to avoid repeated calculations
            cache_key = f"aqi_location_{lat}_{lng}_{radius_km}"
            cached_aqi = cache.get(cache_key)
            
            if cached_aqi is not None:
                return cached_aqi
            
            # Find nearby stations
            lat_range = radius_km / 111  # Rough conversion km to degrees
            lng_range = radius_km / 111
            
            nearby_stations = AirQualityStation.objects.filter(
                latitude__range=(lat - lat_range, lat + lat_range),
                longitude__range=(lng - lng_range, lng + lng_range),
                is_active=True
            )
            
            if not nearby_stations.exists():
                logger.warning(f"No stations found near location ({lat}, {lng})")
                return None
            
            # Get recent readings from nearby stations
            one_hour_ago = timezone.now() - timedelta(hours=1)
            recent_readings = AirQualityReading.objects.filter(
                station__in=nearby_stations,
                measured_at__gte=one_hour_ago
            ).order_by('-measured_at')
            
            if not recent_readings.exists():
                logger.warning(f"No recent readings found for location ({lat}, {lng})")
                return None
            
            # Calculate weighted average (closer stations have more weight)
            total_weight = 0
            weighted_aqi = 0
            
            for reading in recent_readings[:10]:  # Limit to 10 closest readings
                # Simple distance calculation (for more accuracy, use Haversine formula)
                distance = ((float(reading.station.latitude) - lat) ** 2 + 
                           (float(reading.station.longitude) - lng) ** 2) ** 0.5
                
                weight = 1 / (1 + distance)  # Inverse distance weighting
                weighted_aqi += reading.aqi * weight
                total_weight += weight
            
            if total_weight > 0:
                current_aqi = int(weighted_aqi / total_weight)
                
                # Cache for 15 minutes
                cache.set(cache_key, current_aqi, 900)
                
                return current_aqi
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting current AQI for location: {str(e)}")
            return None
    
    @classmethod
    def _calculate_aqi_category(cls, aqi: int) -> str:
        """Calculate AQI category from AQI value"""
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


class HealthRecommendationService:
    """Service for generating personalized health recommendations"""
    
    @classmethod
    def generate_recommendations(cls, profile: UserHealthProfile, current_aqi: int) -> Dict:
        """Generate personalized health recommendations based on user profile and current AQI"""
        
        recommendations = {
            'outdoor_activities': cls._get_outdoor_activity_recommendations(profile, current_aqi),
            'indoor_activities': cls._get_indoor_activity_recommendations(profile, current_aqi),
            'health_precautions': cls._get_health_precautions(profile, current_aqi),
            'protective_measures': cls._get_protective_measures(profile, current_aqi),
            'optimal_times': cls._get_optimal_activity_times(current_aqi),
            'risk_level': cls._calculate_personal_risk_level(profile, current_aqi),
        }
        
        return recommendations
    
    @classmethod
    def _get_outdoor_activity_recommendations(cls, profile: UserHealthProfile, aqi: int) -> List[str]:
        """Get outdoor activity recommendations"""
        recommendations = []
        
        # Base recommendations by AQI
        if aqi <= 50:
            recommendations.append("Great day for all outdoor activities!")
            recommendations.append("Perfect time for jogging, cycling, or sports")
            recommendations.append("Consider spending more time outdoors")
        elif aqi <= 100:
            recommendations.append("Good day for most outdoor activities")
            recommendations.append("Light to moderate exercise is fine")
        elif aqi <= 150:
            recommendations.append("Limit prolonged outdoor activities")
            recommendations.append("Avoid intense outdoor exercise")
        elif aqi <= 200:
            recommendations.append("Minimize outdoor activities")
            recommendations.append("Postpone outdoor sports and exercise")
        else:
            recommendations.append("Avoid all outdoor activities")
            recommendations.append("Stay indoors with windows closed")
        
        # Adjust for health conditions
        high_risk_conditions = ['ASTHMA', 'COPD', 'HEART_DISEASE', 'PREGNANCY']
        if any(condition in profile.health_conditions for condition in high_risk_conditions):
            if aqi > 100:
                recommendations.append("⚠️ Due to your health condition, extra caution advised")
            if aqi > 150:
                recommendations.append("🚫 Avoid outdoor activities due to respiratory/heart condition")
        
        # Age-specific adjustments
        if profile.age and (profile.age >= 65 or profile.age <= 12):
            if aqi > 100:
                recommendations.append("👵👶 Age-sensitive: Limit outdoor time")
        
        return recommendations
    
    @classmethod
    def _get_indoor_activity_recommendations(cls, profile: UserHealthProfile, aqi: int) -> List[str]:
        """Get indoor activity recommendations"""
        recommendations = []
        
        if aqi <= 100:
            recommendations.append("Keep windows open for fresh air")
            recommendations.append("Indoor air quality should be good")
        elif aqi <= 150:
            recommendations.append("Consider closing windows during peak pollution hours")
            recommendations.append("Use air purifiers if available")
        else:
            recommendations.append("Keep all windows closed")
            recommendations.append("Use air purifiers or create a clean air room")
            recommendations.append("Consider indoor exercises instead of outdoor activities")
        
        # Activity level specific
        if profile.activity_level in ['HIGH', 'ATHLETE']:
            if aqi > 150:
                recommendations.append("🏃‍♂️ High-intensity indoor workouts recommended")
                recommendations.append("Use gym or indoor sports facilities")
        
        return recommendations
    
    @classmethod
    def _get_health_precautions(cls, profile: UserHealthProfile, aqi: int) -> List[str]:
        """Get health precautions based on conditions"""
        precautions = []
        
        if aqi > 150:
            precautions.append("Wear N95 or P2.5 mask when going outside")
            precautions.append("Keep rescue medications handy")
        
        # Condition-specific precautions
        if 'ASTHMA' in profile.health_conditions:
            if aqi > 100:
                precautions.append("🫁 Keep inhaler readily available")
                precautions.append("Monitor breathing more closely")
            if aqi > 200:
                precautions.append("⚠️ Consider staying indoors due to asthma risk")
        
        if 'HEART_DISEASE' in profile.health_conditions:
            if aqi > 100:
                precautions.append("❤️ Monitor heart rate during any activity")
                precautions.append("Avoid stress and strenuous activities")
        
        if 'PREGNANCY' in profile.health_conditions:
            if aqi > 100:
                precautions.append("🤰 Extra caution advised during pregnancy")
                precautions.append("Consider prenatal consultation for high AQI days")
        
        return precautions
    
    @classmethod
    def _get_protective_measures(cls, profile: UserHealthProfile, aqi: int) -> List[str]:
        """Get protective measures recommendations"""
        measures = []
        
        if aqi > 100:
            measures.append("Stay hydrated to help body process pollutants")
            measures.append("Eat antioxidant-rich foods (fruits, vegetables)")
        
        if aqi > 150:
            measures.append("Use air purifiers indoors")
            measures.append("Shower after returning from outdoors")
            measures.append("Wash clothes exposed to outdoor air")
        
        if aqi > 200:
            measures.append("Create a 'clean air' room in your home")
            measures.append("Consider temporary relocation if possible")
            measures.append("Use HEPA filters in air conditioning")
        
        return measures
    
    @classmethod
    def _get_optimal_activity_times(cls, aqi: int) -> List[str]:
        """Get optimal times for outdoor activities"""
        times = []
        
        if aqi <= 150:
            times.append("Early morning (6-8 AM) typically has cleaner air")
            times.append("Late evening (after 7 PM) may have lower pollution")
            times.append("Avoid peak traffic hours (8-10 AM, 6-8 PM)")
        else:
            times.append("No optimal outdoor times today - stay indoors")
            times.append("Check forecast for better air quality days")
        
        return times
    
    @classmethod
    def _calculate_personal_risk_level(cls, profile: UserHealthProfile, aqi: int) -> Dict:
        """Calculate personalized risk level"""
        base_risk = 0
        
        # AQI-based risk
        if aqi <= 50:
            base_risk = 1
        elif aqi <= 100:
            base_risk = 2
        elif aqi <= 150:
            base_risk = 3
        elif aqi <= 200:
            base_risk = 4
        else:
            base_risk = 5
        
        # Health condition multiplier
        risk_multiplier = 1.0
        high_risk_conditions = ['ASTHMA', 'COPD', 'HEART_DISEASE', 'PREGNANCY']
        
        for condition in profile.health_conditions:
            if condition in high_risk_conditions:
                risk_multiplier += 0.5
            elif condition in ['ELDERLY', 'CHILD']:
                risk_multiplier += 0.3
        
        # Age adjustment
        if profile.age:
            if profile.age >= 65 or profile.age <= 12:
                risk_multiplier += 0.2
        
        final_risk = min(base_risk * risk_multiplier, 5)  # Cap at 5
        
        # Risk level categories
        if final_risk <= 1.5:
            level = 'LOW'
            color = '#00C851'
            description = 'Minimal health risk from current air quality'
        elif final_risk <= 2.5:
            level = 'MODERATE'
            color = '#FFBB33'
            description = 'Some risk for sensitive individuals'
        elif final_risk <= 3.5:
            level = 'HIGH'
            color = '#FF8800'
            description = 'Increased health risk, take precautions'
        elif final_risk <= 4.5:
            level = 'VERY_HIGH'
            color = '#FF4444'
            description = 'Significant health risk, limit exposure'
        else:
            level = 'EXTREME'
            color = '#CC0000'
            description = 'Extreme health risk, avoid outdoor exposure'
        
        return {
            'level': level,
            'score': round(final_risk, 1),
            'color': color,
            'description': description
        }