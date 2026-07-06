import axios from 'axios';

// region API Configuration
const api = axios.create({
  // it will be used to set the base URL for the API
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  // it will be used to set the headers for the API
  headers: {
    'Content-Type': 'application/json',
  },
});

// it will be used to set the authorization token for the API
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  // if the token is found, it will be used to set the authorization token for the API
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  // it will return the config i.e. the request configuration
  return config;
});

// it will be used to export the API instance
export default api;

// endregion API Configuration