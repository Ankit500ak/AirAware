# Django Authentication Integration Guide

## Overview
Successfully integrated Django backend authentication with the existing AirAware frontend. The system now supports both traditional form-based and AJAX-based authentication.

## What Was Implemented

### 1. Backend API Endpoints (views.py)
Created RESTful API endpoints for authentication:

- **POST `/api/auth/register/`** - User registration
  - Accepts: username, email, password, confirm_password, first_name, last_name
  - Returns: user object and success message
  - Auto-login after successful registration

- **POST `/api/auth/login/`** - User login
  - Accepts: email, password
  - Returns: user object and success message
  - Creates session for authenticated user

- **POST/GET `/api/auth/logout/`** - User logout
  - Clears user session
  - Returns success message

- **GET `/api/auth/check/`** - Check authentication status
  - Returns user info if authenticated
  - Returns authentication status

### 2. URL Routing (urls.py)
Added API routes:
```python
path('api/auth/register/', views.api_register, name='api_register'),
path('api/auth/login/', views.api_login, name='api_login'),
path('api/auth/logout/', views.api_logout, name='api_logout'),
path('api/auth/check/', views.api_check_auth, name='api_check_auth'),
```

### 3. Frontend Integration (index.html)
Updated JavaScript to connect with Django:

- **CSRF Token Handling**: Added `getCookie()` helper function
- **Registration Forms**: Updated all signup forms to POST to `/api/auth/register/`
- **Login Forms**: Updated all login forms to POST to `/api/auth/login/`
- **Error Handling**: Proper display of validation errors from backend
- **Success Handling**: Store user info and reload page on success

### 4. Traditional Login/Signup Pages
Created separate template pages:

- **login.html** - Traditional login form
- **signup.html** - Traditional signup form
- Both styled with Tailwind CSS to match the site design

## Features

### Security Features
✅ CSRF protection on all POST requests
✅ Password validation (minimum 8 characters)
✅ Email validation
✅ Username/email uniqueness checks
✅ Django session-based authentication

### User Experience Features
✅ Real-time validation
✅ Clear error messages
✅ Auto-login after registration
✅ Smooth page reload after authentication
✅ LocalStorage for user data persistence
✅ Responsive design for all screen sizes

### Backend Features
✅ JSON API responses
✅ Proper HTTP status codes
✅ Comprehensive error handling
✅ User data returned on success
✅ Django authentication system integration

## API Response Format

### Success Response (201/200)
```json
{
  "success": true,
  "message": "Account created successfully",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Error Response (400/401/500)
```json
{
  "error": "Error message",
  // OR specific field errors
  "username": ["Username already exists"],
  "email": ["Email already exists"],
  "password": ["Password must be at least 8 characters"]
}
```

## Usage

### For End Users

1. **Sign Up** - Click any "Get Started" or "Sign Up" button
   - Fill in name, email, password
   - Account created and auto-logged in
   - Page reloads to show authenticated state

2. **Sign In** - Click "Sign In" or visit `/login/`
   - Enter email and password
   - Redirected to homepage on success

3. **Sign Out** - Visit `/logout/`
   - Session cleared
   - Redirected to homepage

### For Developers

#### Testing the API
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "username": "test@example.com",
    "email": "test@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Check auth status
curl http://localhost:8000/api/auth/check/
```

## Files Modified

1. **airquality/views.py**
   - Added JSON API views
   - Added authentication logic
   - Added validation

2. **airquality/urls.py**
   - Added API URL patterns

3. **airquality/templates/airquality/index.html**
   - Added CSRF token helper
   - Updated signup handlers
   - Updated login handlers
   - Changed API endpoints from hardcoded URLs to relative paths

4. **airquality/templates/airquality/login.html** (NEW)
   - Traditional login page

5. **airquality/templates/airquality/signup.html** (NEW)
   - Traditional signup page

## Database

Users are stored in Django's default `auth_user` table with fields:
- id (auto-generated)
- username (unique)
- email (unique)
- password (hashed)
- first_name
- last_name
- is_active
- is_staff
- is_superuser
- date_joined
- last_login

## Testing Checklist

✅ User can register with valid data
✅ Duplicate username/email is rejected
✅ Password mismatch is caught
✅ Short passwords are rejected
✅ User can login with email
✅ Wrong password is rejected
✅ User session persists across pages
✅ User can logout
✅ CSRF protection works
✅ Error messages display correctly
✅ Success messages display correctly

## Next Steps (Optional Enhancements)

1. **Email Verification**
   - Send verification email on signup
   - Verify email before allowing login

2. **Password Reset**
   - "Forgot Password" functionality
   - Email-based password reset

3. **Social Authentication**
   - Google Sign-In
   - GitHub Sign-In

4. **Profile Management**
   - Edit profile page
   - Change password
   - Upload avatar

5. **Enhanced Security**
   - Two-factor authentication
   - Rate limiting on login attempts
   - Password strength meter

6. **User Dashboard**
   - Personalized AQI tracking
   - Saved locations
   - Alert preferences

## Troubleshooting

### CSRF Token Issues
If you get "CSRF token missing" errors:
```javascript
// Make sure you're including the CSRF token in headers
const csrftoken = getCookie('csrftoken');
headers: {
  'X-CSRFToken': csrftoken,
}
```

### Session Issues
If user stays logged out after login:
- Check `credentials: 'same-origin'` is set in fetch
- Verify Django session middleware is enabled
- Check browser cookies are enabled

### CORS Issues
If testing from different domain:
```python
# Add to settings.py
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

## Support

For issues or questions:
1. Check Django logs: `python manage.py runserver`
2. Check browser console for JavaScript errors
3. Verify database migrations: `python manage.py migrate`
4. Test API directly with curl or Postman

---

**Status**: ✅ Fully Implemented and Tested
**Last Updated**: October 7, 2025
