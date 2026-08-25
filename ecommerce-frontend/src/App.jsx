import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Login from './pages/Login';
import Register from './pages/Register';
import Orders from './pages/Orders';

export default function App() {
  return (
    <>
      <Navbar />
      <main style={{ maxWidth: 1100, margin: '0 auto', padding: '1.5rem' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products/:slug" element={<ProductDetail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/cart" element={<Cart />} />
            <Route path="/orders" element={<Orders />} />
          </Route>
        </Routes>
      </main>
    </>
  );
}