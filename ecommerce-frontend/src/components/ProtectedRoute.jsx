import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function ProtectedRoute() {
  const access = useAuthStore((s) => s.access);
  const location = useLocation();

  if (!access) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return <Outlet />;
}