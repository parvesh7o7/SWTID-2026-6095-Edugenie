# EduGenie - AI-Powered Educational Assistant

EduGenie is a lightweight AI-powered educational assistant designed to simplify and enhance the learning experience through the power of Generative AI.

## Features

- **Intelligent Question Answering** (`/qa`)
- **Simplified Concept Explanations** (`/explain`)
- **AI-Powered Quiz Generation** (`/quiz`)
- **Educational Text Summarization** (`/summarize`)
- **Personalized Learning Path Recommendations** (`/learn/recommendations`)

## Tech Stack

- **Backend:** FastAPI + Uvicorn + Jinja2
- **AI Models:** Google Gemini 1.5 Pro (Cloud) + LaMini-Flan-T5-248M (Local)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Validation:** Pydantic
- **Config:** python-dotenv

## Project Structure

```
EduGenie/
├── main.py                  # FastAPI app entry point with all routes
├── qna.py                   # Question Answering module (Gemini)
├── explanation_module.py    # Concept Explanation module (LaMini-Flan-T5)
├── quiz_module.py           # Quiz Generation module (Gemini)
├── summary_module.py        # Summarization module (Gemini)
├── learning_path.py         # Learning Path Recommendations module (Gemini)
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment blueprint
├── .env.example             # Environment variable template
├── .gitignore
├── static/
│   ├── index.html           # Frontend UI (Jinja2 Template)
│   └── style.css            # Stylesheet
└── README.md
```

## Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BhavyaAICE/EduGenie.git
   cd EduGenie
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your Google Generative AI API key to .env
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:8000
   ```

## Deploy to Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo (`BhavyaAICE/EduGenie`)
4. Render will auto-detect `render.yaml` and configure everything
5. Add your `GOOGLE_API_KEY` in the **Environment** tab
6. Click **Deploy** 🚀

## API Endpoints

| Endpoint               | Method | Description                        |
|------------------------|--------|------------------------------------| 
| `/qa`                  | POST   | Answer educational questions       |
| `/explain`             | POST   | Explain a concept in simple terms  |
| `/quiz`                | POST   | Generate a quiz on a given topic   |
| `/summarize`           | POST   | Summarize educational text         |
| `/learn/recommendations` | POST | Get personalized learning path     |

## Team

- Built for educational projects and personal learning.
