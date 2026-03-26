import axios from 'axios';

// Get the API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

console.log('[API Client] Initializing with baseURL:', API_URL);

// Create an axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 second timeout (increased for AI chat endpoints)
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('[API Client] Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('[API Client] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    console.log('[API Client] Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('[API Client] Error details:', {
      message: error.message,
      code: error.code,
      status: error.response?.status,
      data: error.response?.data,
      request: error.request ? 'exists' : 'none',
      config: error.config ? {
        url: error.config.url,
        baseURL: error.config.baseURL,
        method: error.config.method,
      } : 'none'
    });

    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;