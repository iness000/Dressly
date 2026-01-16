import SignInGate from "../components/SignInGate.tsx"

export default function ResultsPage() {
  const answers = sessionStorage.getItem("quizAnswers")
  const isLoggedIn = false // later from AuthContext

  
  if (!isLoggedIn) {
    return <SignInGate />
  }

  return (
    <div>
     
      <h1>Your AI Outfits </h1>
    </div>
  )
}
