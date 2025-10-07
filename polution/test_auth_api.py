"""
Test script for authentication API endpoints
Run this after starting the Django server
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_csrf_token():
    """Get CSRF token from Django"""
    response = requests.get(f"{BASE_URL}/")
    return response.cookies.get('csrftoken')

def test_register():
    """Test user registration"""
    print("\n" + "="*50)
    print("Testing Registration API")
    print("="*50)
    
    csrf_token = get_csrf_token()
    
    data = {
        "username": "testuser@example.com",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Referer": BASE_URL
    }
    
    cookies = {"csrftoken": csrf_token}
    
    response = requests.post(
        f"{BASE_URL}/api/auth/register/",
        json=data,
        headers=headers,
        cookies=cookies
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.cookies

def test_login(session_cookies=None):
    """Test user login"""
    print("\n" + "="*50)
    print("Testing Login API")
    print("="*50)
    
    csrf_token = get_csrf_token()
    
    data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Referer": BASE_URL
    }
    
    cookies = {"csrftoken": csrf_token}
    if session_cookies:
        cookies.update(session_cookies)
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login/",
        json=data,
        headers=headers,
        cookies=cookies
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.cookies

def test_check_auth(session_cookies):
    """Test authentication check"""
    print("\n" + "="*50)
    print("Testing Auth Check API")
    print("="*50)
    
    response = requests.get(
        f"{BASE_URL}/api/auth/check/",
        cookies=session_cookies
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_logout(session_cookies):
    """Test user logout"""
    print("\n" + "="*50)
    print("Testing Logout API")
    print("="*50)
    
    csrf_token = get_csrf_token()
    
    headers = {
        "X-CSRFToken": csrf_token,
        "Referer": BASE_URL
    }
    
    cookies = dict(session_cookies)
    cookies["csrftoken"] = csrf_token
    
    response = requests.post(
        f"{BASE_URL}/api/auth/logout/",
        headers=headers,
        cookies=cookies
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def main():
    print("\n" + "="*50)
    print("AirAware Authentication API Test Suite")
    print("="*50)
    print(f"Testing server at: {BASE_URL}")
    
    try:
        # Test 1: Register a new user
        session_cookies = test_register()
        
        # Test 2: Check if authenticated after registration
        test_check_auth(session_cookies)
        
        # Test 3: Logout
        test_logout(session_cookies)
        
        # Test 4: Login again
        session_cookies = test_login()
        
        # Test 5: Check if authenticated after login
        test_check_auth(session_cookies)
        
        print("\n" + "="*50)
        print("✅ All tests completed!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to Django server")
        print("Make sure the server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
