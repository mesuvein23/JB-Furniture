import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

export default function Orders() {
  const { data, isLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: () => client.get('/orders/').then((r) => r.data),
  });

  if (isLoading) return <p>Loading orders…</p>;

  const orders = data?.results || [];

  if (orders.length === 0) return <p>You have no orders yet.</p>;

  return (
    <div>
      <h2>Your orders</h2>
      {orders.map((order) => (
        <div
          key={order.id}
          style={{ border: '1px solid #e5e5e5', borderRadius: 8, padding: 16, marginBottom: 12 }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong>Order #{order.id}</strong>
            <span
              style={{
                padding: '2px 10px',
                borderRadius: 12,
                background: '#f2f2f2',
                fontSize: 13,
              }}
            >
              {order.status_display}
            </span>
          </div>
          <p style={{ color: '#666', fontSize: 13 }}>
            {new Date(order.created_at).toLocaleDateString()}
          </p>
          <ul style={{ paddingLeft: 18, fontSize: 14 }}>
            {order.items.map((i) => (
              <li key={i.id}>
                {i.product_name} × {i.quantity} — ${i.subtotal}
              </li>
            ))}
          </ul>
          <p style={{ textAlign: 'right', fontWeight: 600 }}>
            Total: ${order.total_amount}
          </p>
        </div>
      ))}
    </div>
  );
}