import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getProducts, getCategories } from '../api/products';
import ProductCard from '../components/ProductCard';

export default function Home() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  });

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['products', search, category],
    queryFn: () => getProducts({ search, category }),
  });

  if (isLoading) return <p>Loading products…</p>;
  if (isError) return <p style={{ color: '#c00' }}>Error: {error.message}</p>;

  return (
    <div>
      <div style={{ display: 'flex', gap: 10, marginBottom: 20 }}>
        <input
          placeholder="Search products…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flex: 1, padding: 8 }}
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All categories</option>
          {categories?.results?.map((c) => (
            <option key={c.id} value={c.slug}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <p style={{ color: '#666', fontSize: 14 }}>{data.count} products</p>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
          gap: 16,
        }}
      >
        {data.results.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}