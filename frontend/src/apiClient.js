// src/apiClient.js
import axios from 'axios';
import store from './store';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = store.state.auth.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if error response exists to prevent runtime errors
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      store.state.auth.refreshToken
    ) {
      originalRequest._retry = true;
      try {
        // Use apiClient instead of axios to ensure baseURL is set
        const response = await apiClient.post('/auth/refresh', null, {
          params: { token: store.state.auth.refreshToken },
        });

        // Commit tokens to the auth module
        store.commit('auth/SET_TOKENS', response.data);
        originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;

        // Retry the original request with new token
        return apiClient(originalRequest);
      } catch (err) {
        // Clear authentication state on failure
        store.commit('auth/CLEAR_AUTH');
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
