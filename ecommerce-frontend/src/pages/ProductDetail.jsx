import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getProduct } from '../api/products';
import { addToCart } from '../api/cart';
import { useAuthStore } from '../store/authStore';

export default function ProductDetail() {
  const { slug } = useParams();
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState('');

  const access = useAuthStore((s) => s.access);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: product, isLoading, isError } = useQuery({
    queryKey: ['product', slug],
    queryFn: () => getProduct(slug),
  });

  const mutation = useMutation({
    mutationFn: () => addToCart(product.id, quantity),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
      setMessage('Added to cart.');
    },
    onError: (err) => {
      setMessage(err.response?.data?.quantity || 'Could not add to cart.');
    },
  });

  if (isLoading) return <p>Loading…</p>;
  if (isError) return <p style={{ color: '#c00' }}>Product not found.</p>;

  const handleAdd = () => {
    if (!access) return navigate('/login');
    setMessage('');
    mutation.mutate();
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
      <div>
        {product.images?.[0] ? (
          <img
            src={product.images[0].image}
            alt={product.name}
            style={{ width: '100%', borderRadius: 8 }}
          />
        ) : (
          <div style={{ height: 320, background: '#f2f2f2', borderRadius: 8 }} />
        )}
      </div>

      <div>
        <p style={{ color: '#666', fontSize: 13, margin: 0 }}>
          {product.category?.name}
        </p>
        <h1 style={{ marginTop: 4 }}>{product.name}</h1>
        <p style={{ fontSize: 24, fontWeight: 600 }}>${product.price}</p>
        <p style={{ lineHeight: 1.6 }}>{product.description}</p>

        {product.in_stock ? (
          <>
            <div style={{ display: 'flex', gap: 10, alignItems: 'center', margin: '16px 0' }}>
              <input
                type="number"
                min="1"
                max={product.stock}
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value))}
                style={{ width: 70, padding: 8 }}
              />
              <span style={{ color: '#666', fontSize: 13 }}>
                {product.stock} available
              </span>
            </div>
            <button
              onClick={handleAdd}
              disabled={mutation.isPending}
              style={{ padding: '10px 24px' }}
            >
              {mutation.isPending ? 'Adding…' : 'Add to cart'}
            </button>
          </>
        ) : (
          <p style={{ color: '#c00' }}>Out of stock</p>
        )}

        {message && <p style={{ fontSize: 14, marginTop: 10 }}>{message}</p>}
      </div>
    </div>
  );
}