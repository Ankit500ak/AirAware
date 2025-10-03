import axios from 'axios';
import { handleAPIError } from '../utils/helpers';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'https://api.airaware.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const errorInfo = handleAPIError(error);
    return Promise.reject(errorInfo);
  }
);

// API service methods
export const apiService = {
  // Air quality data
  getAirQuality: async (location) => {
    try {
      const response = await api.get(`/air-quality/${location}`);
      return response;
    } catch (error) {
      throw error;
    }
  },

  getAirQualityHistory: async (location, startDate, endDate) => {
    try {
      const response = await api.get(`/air-quality/${location}/history`, {
        params: { startDate, endDate }
      });
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Sensor management
  getSensors: async () => {
    try {
      const response = await api.get('/sensors');
      return response;
    } catch (error) {
      throw error;
    }
  },

  getSensorDetails: async (sensorId) => {
    try {
      const response = await api.get(`/sensors/${sensorId}`);
      return response;
    } catch (error) {
      throw error;
    }
  },

  // User management
  registerUser: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response;
    } catch (error) {
      throw error;
    }
  },

  loginUser: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      return response;
    } catch (error) {
      throw error;
    }
  },

  getUserProfile: async () => {
    try {
      const response = await api.get('/user/profile');
      return response;
    } catch (error) {
      throw error;
    }
  },

  updateUserProfile: async (userData) => {
    try {
      const response = await api.put('/user/profile', userData);
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Alerts and notifications
  getAlerts: async () => {
    try {
      const response = await api.get('/alerts');
      return response;
    } catch (error) {
      throw error;
    }
  },

  createAlert: async (alertData) => {
    try {
      const response = await api.post('/alerts', alertData);
      return response;
    } catch (error) {
      throw error;
    }
  },

  updateAlert: async (alertId, alertData) => {
    try {
      const response = await api.put(`/alerts/${alertId}`, alertData);
      return response;
    } catch (error) {
      throw error;
    }
  },

  deleteAlert: async (alertId) => {
    try {
      const response = await api.delete(`/alerts/${alertId}`);
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Contact form
  submitContactForm: async (formData) => {
    try {
      const response = await api.post('/contact', formData);
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Reports
  generateReport: async (reportParams) => {
    try {
      const response = await api.post('/reports/generate', reportParams);
      return response;
    } catch (error) {
      throw error;
    }
  },

  downloadReport: async (reportId) => {
    try {
      const response = await api.get(`/reports/${reportId}/download`, {
        responseType: 'blob'
      });
      return response;
    } catch (error) {
      throw error;
    }
  }
};

export default api;