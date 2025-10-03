"""
URL configuration for airaware_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# API Root View
def api_root(request):
    """API root endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Welcome to AirAware API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'air_quality': '/api/air-quality/',
        },
        'status': 'active',
        'description': 'Air Quality Management Platform for Delhi-NCR'
    })

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API root
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root-v1'),
    
    # App URLs
    path('api/air-quality/', include('air_quality.urls')),
    
    # Health check endpoint
    path('health/', lambda request: JsonResponse({'status': 'healthy'}), name='health-check'),
]

# Admin customization
admin.site.site_header = 'AirAware Admin'
admin.site.site_title = 'AirAware Admin Portal'
admin.site.index_title = 'Welcome to AirAware Administration'

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
