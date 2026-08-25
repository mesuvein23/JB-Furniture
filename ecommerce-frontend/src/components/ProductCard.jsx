import { Link } from 'react-router-dom';

export default function ProductCard({ product }) {
  return (
    <Link
      to={`/products/${product.slug}`}
      style={{
        border: '1px solid #e5e5e5',
        borderRadius: 8,
        padding: 12,
        textDecoration: 'none',
        color: 'inherit',
        display: 'block',
      }}
    >
      {product.primary_image ? (
        <img
          src={product.primary_image}
          alt={product.name}
          style={{ width: '100%', height: 180, objectFit: 'cover', borderRadius: 4 }}
        />
      ) : (
        <div style={{ height: 180, background: '#f2f2f2', borderRadius: 4 }} />
      )}
      <h3 style={{ fontSize: 15, margin: '10px 0 4px' }}>{product.name}</h3>
      <p style={{ margin: 0, fontWeight: 600 }}>${product.price}</p>
      {!product.in_stock && (
        <p style={{ color: '#c00', fontSize: 13, margin: '4px 0 0' }}>
          Out of stock
        </p>
      )}
    </Link>
  );
}