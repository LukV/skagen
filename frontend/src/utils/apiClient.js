import axios from 'axios';
import store from '@/store';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = store.state.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response.status === 401 &&
      !originalRequest._retry &&
      store.state.refreshToken
    ) {
      originalRequest._retry = true;
      try {
        const response = await axios.post('/auth/refresh', null, {
          params: { token: store.state.refreshToken },
        });
        store.commit('SET_TOKENS', response.data);
        originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
        return apiClient(originalRequest);
      } catch (err) {
        store.commit('CLEAR_AUTH');
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
