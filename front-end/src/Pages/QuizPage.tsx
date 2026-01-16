import { useNavigate } from "react-router-dom"
import QuizForm from "../components/QuizForm"

export default function QuizPage() {
  const navigate = useNavigate()

  const handleQuizComplete = (answers: Record<string, any>) => {
    // Save answers for later steps
    sessionStorage.setItem("quizAnswers", JSON.stringify(answers))

    // Go to login (or results later if already logged in)
    navigate("/Results", { state: { from: "quiz" } })
  }

  return (
    <div className="min-h-screen">
      <QuizForm onComplete={handleQuizComplete} />
    </div>
  )
}
