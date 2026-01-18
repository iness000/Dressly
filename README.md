# 👗 Dressly — AI-Driven Personal Styling Platform

Dressly is a full-stack web application that helps users discover clothing items that genuinely match their **style, preferences, and budget** through a personalized quiz and an intelligent recommendation system.


---

## 🌟 Why Dressly?

Shopping online is overwhelming:
- thousands of items
- little personalization
- unclear style direction

Dressly solves this by combining:
- a short style quiz
- real clothing data 
- a ranking-based recommendation engine
- a smooth, modern user experience

The goal is to simulate how **real AI-driven consumer products** are built in production.

### 🧠 Recommendation Engine (Hybrid AI System)

Dressly uses a hybrid recommendation architecture inspired by real-world production systems.

1. User quiz answers are processed by the backend
2. Products are filtered and pre-ranked using deterministic rules
3. A reduced, relevant subset is sent to Gemini
4. Gemini performs semantic and stylistic reasoning to select the best matches
5. The final recommendations are returned with human-readable explanations

This approach combines:
- scalability and control (rule-based logic)
- creativity and reasoning (LLM)
- explainability for users

## ✨ Key Features

### 📝 Style Quiz
- Collects user preferences (style, gender, budget, colors, occasion)
- Designed to be short, intuitive, and extensible
- Answers persist across login

### 🔐 Authentication
- Secure signup & login using JWT
- Results protected behind authentication
- Backend-verified access for all sensitive routes



### 👚 Real Clothing Data
- Uses H&M data via RapidAPI
- External APIs accessed **only from the backend**
- Async, scalable HTTP client

### 🧠 Recommendation Engine (AI Logic v1)
- Rule-based, explainable ranking system
- Each clothing item is scored based on user preferences
- Items are ranked from **best → worst match**
- Designed to evolve toward ML / LLM-based ranking

### 🎨 Modern Frontend
- React + TypeScript
- Tailwind CSS
- Smooth animations with Framer Motion
- Clean navigation and UX-focused layout

---




