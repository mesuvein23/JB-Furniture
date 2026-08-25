import client from './client';

export const getProducts = (params) =>
  client.get('/products/', { params }).then((r) => r.data);

export const getProduct = (slug) =>
  client.get(`/products/${slug}/`).then((r) => r.data);

export const getCategories = () =>
  client.get('/categories/').then((r) => r.data);