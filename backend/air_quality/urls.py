# Air Quality App URLs

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'stations', views.AirQualityStationViewSet, basename='stations')
router.register(r'readings', views.AirQualityReadingViewSet, basename='readings')
router.register(r'health-profiles', views.UserHealthProfileViewSet, basename='health-profiles')
router.register(r'alerts', views.AirQualityAlertViewSet, basename='alerts')
router.register(r'forecasts', views.AirQualityForecastViewSet, basename='forecasts')

app_name = 'air_quality'

urlpatterns = [
    path('', include(router.urls)),
]