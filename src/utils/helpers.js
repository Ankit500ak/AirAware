// Utility functions for the Air Aware application

// Format date for display
export const formatDate = (date) => {
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(date).toLocaleDateString('en-US', options);
};

// Validate email format
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Debounce function for search inputs
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Generate unique ID
export const generateId = () => {
  return '_' + Math.random().toString(36).substr(2, 9);
};

// Air Quality Index (AQI) color coding
export const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#00e400'; // Green (Good)
  if (aqi <= 100) return '#ffff00'; // Yellow (Moderate)
  if (aqi <= 150) return '#ff7e00'; // Orange (Unhealthy for Sensitive Groups)
  if (aqi <= 200) return '#ff0000'; // Red (Unhealthy)
  if (aqi <= 300) return '#8f3f97'; // Purple (Very Unhealthy)
  return '#7e0023'; // Maroon (Hazardous)
};

// Get AQI description
export const getAQIDescription = (aqi) => {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Moderate';
  if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
  if (aqi <= 200) return 'Unhealthy';
  if (aqi <= 300) return 'Very Unhealthy';
  return 'Hazardous';
};

// Format numbers with commas
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

// Calculate percentage
export const calculatePercentage = (value, total) => {
  if (total === 0) return 0;
  return Math.round((value / total) * 100);
};

// Convert temperature between units
export const convertTemperature = (temp, fromUnit, toUnit) => {
  if (fromUnit === toUnit) return temp;
  
  if (fromUnit === 'C' && toUnit === 'F') {
    return (temp * 9/5) + 32;
  }
  
  if (fromUnit === 'F' && toUnit === 'C') {
    return (temp - 32) * 5/9;
  }
  
  return temp;
};

// Local storage helpers
export const storage = {
  get: (key) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error('Error getting item from localStorage:', error);
      return null;
    }
  },
  
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error('Error setting item in localStorage:', error);
      return false;
    }
  },
  
  remove: (key) => {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error('Error removing item from localStorage:', error);
      return false;
    }
  }
};

// API error handler
export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error status
    console.error('API Error:', error.response.status, error.response.data);
    return {
      message: error.response.data.message || 'Server error occurred',
      status: error.response.status
    };
  } else if (error.request) {
    // Network error
    console.error('Network Error:', error.request);
    return {
      message: 'Network error. Please check your connection.',
      status: 'network_error'
    };
  } else {
    // Other error
    console.error('Error:', error.message);
    return {
      message: error.message || 'An unexpected error occurred',
      status: 'unknown_error'
    };
  }
};