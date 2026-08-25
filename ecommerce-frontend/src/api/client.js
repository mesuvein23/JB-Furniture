import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Attach the access token to every request
client.interceptors.request.use((config) => {
  const { access } = useAuthStore.getState();
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

// On 401, try refreshing once, then replay the original request
let refreshing = null;

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status !== 401 || original._retried) {
      return Promise.reject(error);
    }
    original._retried = true;

    const { refresh, setAccess, logout } = useAuthStore.getState();
    if (!refresh) {
      logout();
      return Promise.reject(error);
    }

    try {
      refreshing =
        refreshing ||
        axios.post(`${import.meta.env.VITE_API_URL}/auth/refresh/`, { refresh });

      const { data } = await refreshing;
      refreshing = null;

      setAccess(data.access);
      original.headers.Authorization = `Bearer ${data.access}`;
      return client(original);
    } catch (err) {
      refreshing = null;
      logout();
      window.location.href = '/login';
      return Promise.reject(err);
    }
  }
);

export default client;