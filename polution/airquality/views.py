from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

def index(request):
    """Main page view for air quality information"""
    return render(request, 'airquality/index.html', {
        'title': 'Air Quality Monitor',
        'message': 'Welcome to the Air Quality Monitoring System'
    })

def about(request):
    """About page view"""
    return render(request, 'airquality/about.html', {
        'title': 'About Air Quality Monitor'
    })

@login_required
def data(request):
    """Data page view with sample pollution data - requires login"""
    sample_data = [
        {'city': 'New York', 'aqi': 85, 'status': 'Moderate'},
        {'city': 'Los Angeles', 'aqi': 120, 'status': 'Unhealthy for Sensitive Groups'},
        {'city': 'Chicago', 'aqi': 45, 'status': 'Good'},
        {'city': 'Houston', 'aqi': 95, 'status': 'Moderate'},
    ]
    return render(request, 'airquality/data.html', {
        'title': 'Air Quality Data',
        'pollution_data': sample_data
    })

@login_required
def dashboard(request):
    """User dashboard view - requires login"""
    return render(request, 'airquality/dashboard.html', {
        'title': 'Dashboard - AirAware'
    })

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        
        # Try to find user by email if @ is in the input
        username = username_or_email
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'airquality/login.html', {
                    'title': 'Login - Air Quality Monitor'
                })
        
        # Authenticate with username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'airquality:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'airquality/login.html', {
        'title': 'Login - Air Quality Monitor'
    })

def user_signup(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            # Auto-login after signup
            login(request, user)
            messages.success(request, f'Welcome to AirAware, {user.first_name}! Your account has been created successfully.')
            return redirect('airquality:dashboard')
    
    return render(request, 'airquality/signup.html', {
        'title': 'Sign Up - Air Quality Monitor'
    })

def user_logout(request):
    """User logout view"""
    if request.user.is_authenticated:
        username = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f'Goodbye, {username}! You have been logged out.')
    return redirect('airquality:index')

# API Views for AJAX requests
@require_http_methods(["POST"])
def api_register(request):
    """API endpoint for user registration"""
    try:
        data = json.loads(request.body)
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        # Validation
        if not all([username, email, password, confirm_password]):
            return JsonResponse({
                'error': 'All fields are required'
            }, status=400)
        
        if password != confirm_password:
            return JsonResponse({
                'password': ['Passwords do not match']
            }, status=400)
        
        if len(password) < 8:
            return JsonResponse({
                'password': ['Password must be at least 8 characters long']
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username': ['Username already exists']
            }, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email': ['Email already exists']
            }, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Auto login after registration
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Account created successfully',
            'redirect_url': '/dashboard/',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["POST"])
def api_login(request):
    """API endpoint for user login"""
    try:
        data = json.loads(request.body)
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return JsonResponse({
                'error': 'Email and password are required'
            }, status=400)
        
        # Try to find user by email first
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'Invalid email or password'
            }, status=401)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'redirect_url': '/dashboard/',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=200)
        else:
            return JsonResponse({
                'error': 'Invalid email or password'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["POST", "GET"])
def api_logout(request):
    """API endpoint for user logout"""
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logout successful'
        }, status=200)
    return JsonResponse({
        'error': 'Not authenticated'
    }, status=401)

@require_http_methods(["GET"])
def api_check_auth(request):
    """API endpoint to check if user is authenticated"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            }
        }, status=200)
    return JsonResponse({
        'authenticated': False
    }, status=200)
