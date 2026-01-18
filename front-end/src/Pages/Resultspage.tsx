import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import SignInGate from "../components/SignInGate"
import NavBar from "../components/NavBar"
import { API_URL } from "../services/authService"
import { motion } from "framer-motion"
import {
  Sparkles,
  ShoppingBag,
  Heart,
  ExternalLink,
  ArrowLeft,
} from "lucide-react"





export default function ResultsPage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [favorites, setFavorites] = useState<number[]>([])

  const quizAnswers = sessionStorage.getItem("quizAnswers")
  const token = localStorage.getItem("token")
  const isLoggedIn = Boolean(token)

  useEffect(() => {
    if (!isLoggedIn || !quizAnswers) return

    const sendQuizToBackend = async () => {
      try {
        setLoading(true)

        const response = await fetch(`${API_URL}/quiz/submit`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: quizAnswers,
        })

        if (!response.ok) {
          throw new Error("Failed to fetch AI results")
        }

        const data = await response.json()
        setResults(data)

        // optional: clear quiz answers after success
        sessionStorage.removeItem("quizAnswers")

      } catch (err: any) {
        setError(err.message || "Something went wrong")
      } finally {
        setLoading(false)
      }
    }

    sendQuizToBackend()
  }, [isLoggedIn, quizAnswers, token])

  const toggleFavorite = (itemId: number) => {
    setFavorites((prev) =>
      prev.includes(itemId)
        ? prev.filter((id) => id !== itemId)
        : [...prev, itemId]
    )
  }

  if (!quizAnswers) {
    return <p className="p-8">No quiz data found.</p>
  }

  if (!isLoggedIn) {
    return <SignInGate />
  }

  if (loading) {
    return <p className="p-8">Generating your outfits… ✨</p>
  }

  if (error) {
    return <p className="p-8 text-red-500">{error}</p>
  }

  if (!results) {
    return null
  }

  //RESULTS 
  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-white to-pink-50">
      <NavBar />

      <main className="pt-28 pb-20 px-6 max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <button
            onClick={() => navigate("/")}
            className="mb-6 inline-flex items-center text-gray-500 hover:text-black"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </button>

          <div className="inline-flex items-center gap-2 px-6 py-3 bg-white rounded-full shadow mb-6">
            <Sparkles className="w-4 h-4 text-rose-500" />
            <span>Your Style Profile: {results.styleProfile}</span>
          </div>

          <h1 className="text-4xl font-black mb-3">
            Your <span className="text-rose-500">Perfect Picks</span>
          </h1>
          <p className="text-gray-500">
            Based on your quiz answers, here’s what we recommend
          </p>
        </div>

        {/* Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.items.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              className="bg-white rounded-2xl shadow hover:shadow-lg transition"
            >
              <div className="relative aspect-[3/4] overflow-hidden rounded-t-2xl">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-full object-cover hover:scale-105 transition-transform"
                />

                <div className="absolute top-4 left-4 bg-white px-3 py-1 rounded-full text-sm font-bold">
                  {item.match}% Match
                </div>

                <button
                  onClick={() => toggleFavorite(item.id)}
                  className="absolute top-4 right-4 w-10 h-10 rounded-full bg-white flex items-center justify-center"
                >
                  <Heart
                    className={`w-5 h-5 ${
                      favorites.includes(item.id)
                        ? "fill-rose-500 text-rose-500"
                        : "text-gray-400"
                    }`}
                  />
                </button>
              </div>

              <div className="p-5">
                <p className="text-sm text-gray-500">{item.brand}</p>
                <h3 className="font-bold text-lg">{item.name}</h3>
                <p className="text-xl font-black text-rose-500 mt-2">
                  {item.price}
                </p>

                <button className="mt-4 w-full bg-gradient-to-r from-rose-500 to-pink-500 text-white py-3 rounded-xl flex items-center justify-center gap-2 hover:scale-105 transition">
                  <ShoppingBag className="w-4 h-4" />
                  Shop Now
                  <ExternalLink className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  )
}