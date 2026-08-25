import { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { login } from '../api/auth';
import { useAuthStore } from '../store/authStore';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/';

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await login(form);
      setAuth({ user: data.user, access: data.access, refresh: data.refresh });
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Check your details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 380, margin: '2rem auto' }}>
      <h2>Log in</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: 8, marginBottom: 10 }}
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: 8, marginBottom: 10 }}
        />
        {error && <p style={{ color: '#c00', fontSize: 14 }}>{error}</p>}
        <button type="submit" disabled={loading} style={{ width: '100%', padding: 10 }}>
          {loading ? 'Logging in…' : 'Log in'}
        </button>
      </form>
      <p style={{ fontSize: 14 }}>
        No account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}