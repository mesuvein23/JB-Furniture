import client from './client';

export const login = (credentials) =>
  client.post('/auth/login/', credentials).then((r) => r.data);

export const register = (data) =>
  client.post('/auth/register/', data).then((r) => r.data);

export const getProfile = () =>
  client.get('/auth/profile/').then((r) => r.data);