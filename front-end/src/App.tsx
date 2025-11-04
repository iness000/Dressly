
import "tailwindcss"
import { Sparkles } from 'lucide-react'
import QuizForm from "./components/QuizForm"
import { useState } from "react"
import ProductGrid from "./components/ProductGrid"


type Answers = Record<string,any>
function App() {
  const [view,setView]=useState("")
  const [answers,setAnswers]=useState<Answers | null>(null)
  const handleStartQuiz =() =>{
    setView('quiz');
  }
  const handleBackHome=()=>{
    setView("");
  }
  const handleQuizComplete=(finalAnswers:Answers)=>{
    setAnswers(finalAnswers)
    setView("")
  }

  return (
  /*   <div className="min-h-screen bg-gradient-to-br from-rose-100 via-pink-50 to-lavender-100 flex items-center justify-center text- text-3xl font-bol">
      {view === 'quiz' ? (
        <QuizForm onComplete={handleQuizComplete}/>
      ) : (
        <div className="max-w-4xl w-full text-center space-y-8 py-12">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 px-6 py-3 bg-white/80 backdrop-blur-sm rounded-full text-rose-600 text-base font-semibold shadow-lg mb-6 border border-rose-200">
              <span>AI-Powered Personal Styling</span>
            </div>

            <div className="space-y-4">
              <h1 className="text-8xl md:text-9xl font-black text-transparent bg-clip-text bg-gradient-to-r from-rose-600 via-pink-500 to-orange-400 tracking-tight drop-shadow-sm">
                Dressly
              </h1>

              <div className="flex items-center justify-center gap-3 text-2xl md:text-3xl font-bold text-gray-800">
                <span>Your AI Stylist Awaits</span>
                <Sparkles className="w-8 h-8 text-amber-500" />
              </div>
            </div>

            <p className="text-xl md:text-2xl text-gray-700 max-w-3xl mx-auto leading-relaxed font-medium">
              Discover perfectly curated outfits that match your unique style, body type, and budget.
              <span className="text-rose-600"> Let AI transform your wardrobe.</span>
            </p>
          </div>

          <div className="space-y-6 pt-8">
            <button
              className="group relative inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-rose-500 to-pink-500 text-white text-lg font-semibold rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
              onClick={handleStartQuiz}
            >
              <span>Start Your Style Quiz</span>
              <Sparkles className="w-5 h-5 group-hover:rotate-12 transition-transform" />
            </button>

            <p className="text-sm text-gray-500">Takes only 2 minutes</p>
          </div>
        </div>
      )}
        
    </div> */
    <ProductGrid />
  )
}

export default App
