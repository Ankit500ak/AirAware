from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'airquality'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('data/', views.data, name='data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    
    # Test page (remove in production)
    path('test-auth/', TemplateView.as_view(template_name='airquality/test_auth.html'), name='test_auth'),
    
    # API endpoints
    path('api/auth/register/', views.api_register, name='api_register'),
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    path('api/auth/check/', views.api_check_auth, name='api_check_auth'),
]