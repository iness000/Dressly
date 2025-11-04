import { useEffect, useState } from "react";
import api from "../lib/api";

type Product = {
  code: string;
  name: string;
  price?: string;
  image?: string;
};

export default function ProductGrid() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await api.get("/hm/products/simple?categories=men_trousers");
        setProducts(res.data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  if (loading) return <p className="p-6">Loading...</p>;
  if (error) return <p className="p-6 text-red-500">{error}</p>;

  return (
    <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-6 bg-gray-50 min-h-screen">
      {products.map((p) => (
        <div key={p.code} className="border rounded-xl bg-white shadow-sm p-3">
          <img
            src={p.image}
            alt={p.name}
            className="w-full h-64 object-cover rounded-lg"
          />
          <h3 className="mt-3 font-semibold text-gray-800 text-sm">{p.name}</h3>
          <p className="text-gray-600 text-sm">{p.price}</p>
        </div>
      ))}
    </div>
  );
}

