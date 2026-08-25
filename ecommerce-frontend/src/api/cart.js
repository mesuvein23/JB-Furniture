import client from './client';

export const getCart = () => client.get('/cart/').then((r) => r.data);

export const addToCart = (product_id, quantity = 1) =>
  client.post('/cart/items/', { product_id, quantity }).then((r) => r.data);

export const updateCartItem = (itemId, quantity) =>
  client.patch(`/cart/items/${itemId}/`, { quantity }).then((r) => r.data);

export const removeCartItem = (itemId) =>
  client.delete(`/cart/items/${itemId}/`).then((r) => r.data);

export const checkout = (address_id) =>
  client.post('/orders/checkout/', { address_id }).then((r) => r.data);