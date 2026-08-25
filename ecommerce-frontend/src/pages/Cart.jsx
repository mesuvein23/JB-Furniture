import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { getCart, updateCartItem, removeCartItem, checkout } from '../api/cart';
import client from '../api/client';
import { useState } from 'react';

function AddressForm({ onCreated }) {
  const [form, setForm] = useState({
    full_name: '',
    line1: '',
    line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
  });
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const labels = {
    full_name: 'Full name',
    line1: 'Address line 1',
    line2: 'Address line 2 (optional)',
    city: 'City',
    state: 'State',
    postal_code: 'Postal code',
    country: 'Country',
  };

  const submit = async (e) => {
    e.preventDefault();
    setErrors({});
    setSaving(true);
    try {
      await client.post('/addresses/', form);
      onCreated();
    } catch (err) {
      setErrors(err.response?.data || { detail: 'Could not save address.' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={submit} style={{ display: 'grid', gap: 8, maxWidth: 400 }}>
      {Object.keys(form).map((k) => (
        <div key={k}>
          <input
            placeholder={labels[k]}
            value={form[k]}
            onChange={(e) => setForm({ ...form, [k]: e.target.value })}
            required={k !== 'line2'}
            style={{ width: '100%', padding: 8 }}
          />
          {errors[k] && (
            <p style={{ color: '#c00', fontSize: 13, margin: '2px 0 0' }}>
              {Array.isArray(errors[k]) ? errors[k].join(' ') : errors[k]}
            </p>
          )}
        </div>
      ))}
      {errors.detail && <p style={{ color: '#c00', fontSize: 14 }}>{errors.detail}</p>}
      <button type="submit" disabled={saving} style={{ padding: 10 }}>
        {saving ? 'Saving…' : 'Save address'}
      </button>
    </form>
  );
}

export default function Cart() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const { data: cart, isLoading } = useQuery({
    queryKey: ['cart'],
    queryFn: getCart,
  });

  const { data: addresses } = useQuery({
    queryKey: ['addresses'],
    queryFn: () => client.get('/addresses/').then((r) => r.data),
  });

  const refresh = () => queryClient.invalidateQueries({ queryKey: ['cart'] });

  const updateMutation = useMutation({
    mutationFn: ({ id, quantity }) => updateCartItem(id, quantity),
    onSuccess: refresh,
    onError: (err) => setError(err.response?.data?.quantity || 'Update failed.'),
  });

  const removeMutation = useMutation({
    mutationFn: (id) => removeCartItem(id),
    onSuccess: refresh,
  });

  const checkoutMutation = useMutation({
    mutationFn: (addressId) => checkout(addressId),
    onSuccess: () => {
      refresh();
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      navigate('/orders');
    },
    onError: (err) => setError(err.response?.data?.detail || 'Checkout failed.'),
  });

  if (isLoading) return <p>Loading cart…</p>;

  const items = cart?.items || [];
  const addressList = addresses?.results || addresses || [];

  if (items.length === 0) {
    return (
      <div>
        <h2>Your cart is empty</h2>
        <Link to="/">Browse products</Link>
      </div>
    );
  }

  return (
    <div>
      <h2>Your cart</h2>

      {items.map((item) => (
        <div
          key={item.id}
          style={{
            display: 'flex',
            gap: 16,
            alignItems: 'center',
            padding: '12px 0',
            borderBottom: '1px solid #eee',
          }}
        >
          {item.product.primary_image && (
            <img
              src={item.product.primary_image}
              alt={item.product.name}
              style={{ width: 70, height: 70, objectFit: 'cover', borderRadius: 4 }}
            />
          )}
          <div style={{ flex: 1 }}>
            <Link to={`/products/${item.product.slug}`}>{item.product.name}</Link>
            <p style={{ margin: '4px 0', color: '#666', fontSize: 14 }}>
              ${item.product.price} each
            </p>
          </div>
          <input
            type="number"
            min="1"
            value={item.quantity}
            onChange={(e) => {
              const q = Number(e.target.value);
              if (q >= 1) {
                setError('');
                updateMutation.mutate({ id: item.id, quantity: q });
              }
            }}
            style={{ width: 60, padding: 6 }}
          />
          <strong style={{ width: 80, textAlign: 'right' }}>${item.subtotal}</strong>
          <button onClick={() => removeMutation.mutate(item.id)}>Remove</button>
        </div>
      ))}

      <div style={{ textAlign: 'right', marginTop: 16 }}>
        <p style={{ fontSize: 20 }}>
          Total: <strong>${cart.total}</strong>
        </p>
      </div>

      {error && <p style={{ color: '#c00' }}>{error}</p>}

      <div style={{ marginTop: 20 }}>
        <h3>Ship to</h3>
        {addressList.length === 0 ? (
          <>
            <p style={{ color: '#666', fontSize: 14 }}>
              Add a delivery address to place your order.
            </p>
            <AddressForm
              onCreated={() =>
                queryClient.invalidateQueries({ queryKey: ['addresses'] })
              }
            />
          </>
        ) : (
          addressList.map((a) => (
            <button
              key={a.id}
              onClick={() => {
                setError('');
                checkoutMutation.mutate(a.id);
              }}
              disabled={checkoutMutation.isPending}
              style={{
                display: 'block',
                padding: 10,
                marginBottom: 8,
                width: '100%',
                textAlign: 'left',
              }}
            >
              {a.full_name} — {a.line1}, {a.city} {a.postal_code}
              <span style={{ float: 'right' }}>
                {checkoutMutation.isPending ? 'Placing…' : 'Place order →'}
              </span>
            </button>
          ))
        )}
      </div>
    </div>
  );
}