import { Link } from "react-router-dom"

export default function SignInGate() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-100 via-pink-50 to-lavender-100 flex items-center justify-center">
      <div className="max-w-2xl w-full">
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-10 md:p-12 text-center space-y-6 border border-rose-100">

          <img
            src="https://media2.giphy.com/media/OFcP2ojNIAkec/giphy.gif"
            alt="sparkle gif"
            className="mx-auto pointer-events-none"
          />

          <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
            Your results just dropped ✨
          </h2>

          <p className="text-lg text-gray-600">
            Your personalized style recommendations are ready.
            Sign in to unlock your full results and saved looks.
          </p>

          <Link
            to="/login"
            className="inline-flex items-center justify-center px-6 py-4 bg-gradient-to-r from-rose-500 to-pink-500 text-white font-semibold rounded-full shadow-lg hover:scale-105 transition"
          >
            Go to Sign In
          </Link>

        </div>
      </div>
    </div>
  )
}
