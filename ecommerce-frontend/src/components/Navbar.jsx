import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  return (
    <nav
      style={{
        display: 'flex',
        gap: 16,
        alignItems: 'center',
        padding: '12px 24px',
        borderBottom: '1px solid #e5e5e5',
      }}
    >
      <Link to="/" style={{ fontWeight: 700, textDecoration: 'none', color: 'inherit' }}>
        Shop
      </Link>
      <div style={{ flex: 1 }} />
      {user ? (
        <>
          <Link to="/cart">Cart</Link>
          <Link to="/orders">Orders</Link>
          <span style={{ color: '#666', fontSize: 14 }}>{user.email}</span>
          <button onClick={() => { logout(); navigate('/'); }}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
}