import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../api/auth';
import { useAuthStore } from '../store/authStore';

export default function Register() {
  const [form, setForm] = useState({
    email: '', username: '', password: '', password2: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);
    try {
      const data = await register(form);
      setAuth({ user: data.user, access: data.access, refresh: data.refresh });
      navigate('/');
    } catch (err) {
      setErrors(err.response?.data || { detail: 'Registration failed.' });
    } finally {
      setLoading(false);
    }
  };

  const fieldError = (name) =>
    errors[name] && (
      <p style={{ color: '#c00', fontSize: 13, margin: '0 0 8px' }}>
        {Array.isArray(errors[name]) ? errors[name].join(' ') : errors[name]}
      </p>
    );

  return (
    <div style={{ maxWidth: 380, margin: '2rem auto' }}>
      <h2>Create account</h2>
      <form onSubmit={handleSubmit}>
        {['email', 'username', 'password', 'password2'].map((name) => (
          <div key={name}>
            <input
              name={name}
              type={name.startsWith('password') ? 'password' : name === 'email' ? 'email' : 'text'}
              placeholder={name === 'password2' ? 'Confirm password' : name}
              value={form[name]}
              onChange={handleChange}
              required
              style={{ width: '100%', padding: 8, marginBottom: 6 }}
            />
            {fieldError(name)}
          </div>
        ))}
        {errors.detail && <p style={{ color: '#c00', fontSize: 14 }}>{errors.detail}</p>}
        <button type="submit" disabled={loading} style={{ width: '100%', padding: 10 }}>
          {loading ? 'Creating…' : 'Register'}
        </button>
      </form>
      <p style={{ fontSize: 14 }}>
        Already have one? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
}